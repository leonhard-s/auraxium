import asyncio
import contextlib
import json
import logging
from typing import (Any, Callable, Coroutine, Iterator, List, Optional, Union)

import websockets

from ..client import Client
from ..models import Event
from ..types import CensusData
from ..utils import expo_scaled

from ._trigger import Trigger

__all__ = [
    'EventClient'
]

_ESS_ENDPOINT = 'wss://push.planetside2.com/streaming'

_Callback = Callable[[Event], Union[Coroutine[Any, Any, None], None]]
_log = logging.getLogger('auraxium.ess')


class EventClient(Client):
    """Advanced client with event streaming capability.

    This subclass of :class:`Client` extends the interface to also
    provide access to the websocket endpoint at
    ``wss://push.planetside2.com/streaming``.

    To use the websocket endpoint, you have to define a
    :class:`Trigger` and register it using the
    :meth:`EventClient.add_trigger()` method. This will automatically
    open a websocket connection is there is not already one running.
    Likewise, removing all event triggers from the client will cause
    the underlying websocket connection to close.

    Refer to the :class:`Trigger` class's documentation for details on
    how to use triggers and respond to events.

    Attributes:
        triggers: The list of :class:`Triggers <Trigger>` registered
            for the client.
        websocket: The websocket client used for the real-time event
            stream. This will be automatically opened and closed by the
            client as event triggers are added and removed.

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.triggers: List[Trigger] = []
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self._connect_lock = asyncio.Lock()
        self._connected: bool = False
        self._reconnect_backoff = self._reset_backoff()
        self._send_queue: List[str] = []

    def add_trigger(self, trigger: Trigger) -> None:
        """Add a new event trigger to the client.

        If there is currently no active websocket connection to the
        event streaming service, one will be created for this trigger.

        .. note::
            As this is a synchronous method, the websocket will not be
            active by the time this method returns.
            Use :meth:`EventClient.wait_ready()` to wait for the
            websocket being ready.

        Arguments:
            trigger: The trigger to add.

        """
        _log.debug('Adding trigger %s', trigger)
        self.triggers.append(trigger)
        subscription = trigger.generate_subscription()
        self._send_queue.append(subscription)
        # Only queue the connect() method if it is not already running
        if self.websocket is None and not self._connect_lock.locked():
            _log.debug('Websocket not connected, scheduling connection')
            self.loop.create_task(self.connect())

    def get_trigger(self, name: str) -> Trigger:
        """Retrieve a registered event trigger by name.

        If the trigger cannot be found, a :class:`KeyError` is raised.

        Arguments:
            name: The name of the trigger to return.

        Raises:
            KeyError: Raised if no trigger with the given name is
                registered for the client.

        """
        for trigger in self.triggers:
            if trigger.name == name:
                return trigger
        raise KeyError(f'No trigger with name "{name}" found')

    def remove_trigger(self, trigger: Union[Trigger, str], *,
                       keep_websocket_alive: bool = False) -> None:
        """Remove an existing event trigger.

        You can either provide the trigger instance to remove, or
        specify the name of the trigger instead.

        By default, the underlying websocket connection will be closed
        if this was the only trigger registered. Use the
        ``keep_websocket_alive`` flag to prevent this.

        Arguments:
            trigger: The trigger to remove, or its unique name.
            keep_websocket_alive (optional): If True, the websocket
                connection will be kept open even if the client has
                zero triggers remaining. Defaults to ``False``.

        Raises:
            KeyError: Raised if a trigger name was passed and no
                trigger of this name exists for the client.
            ValueError: Raised if no trigger of the given name is
                currently registered for this client.

        """
        if not isinstance(trigger, Trigger):
            trigger = self.get_trigger(trigger)
        _log.debug('Removing trigger %s', trigger)
        try:
            self.triggers.remove(trigger)
        except ValueError as err:
            raise RuntimeError('The given trigger is not registered for '
                               'this client') from err
        # If this was the only trigger registered, close the websocket
        if not keep_websocket_alive and not self.triggers:
            _log.info('All triggers have been removed, closing websocket')
            self.loop.create_task(self.close())

    async def close(self) -> None:
        """Shut down the client.

        This will close the websocket connection and end any ongoing
        HTTP sessions used for requests to the REST API.

        Call this to clean up before the client object is destroyed.

        """
        await self.disconnect()
        await super().close()

    async def connect(self) -> None:
        """Connect to the websocket endpoint and process responses.

        This will continuously loop until :meth:`EventClient.close()`
        is called.
        If the websocket connection encounters and error, it will be
        automatically restarted.

        Add payloads to :attr`EventClient._send_queue` to schedule
        their transmission.

        Any event payloads received will be passed to
        :meth:`EventClient.dispatch()` for filtering and event
        dispatch.

        """
        # NOTE: When multiple triggers are added to the bot without an active
        # websocket connection, this function may be scheduled multiple times.
        if self._connect_lock.locked():
            _log.debug('Websocket already running')
            return
        await self._connect_lock.acquire()

        _log.info('Connecting to websocket endpoint...')
        url = f'{_ESS_ENDPOINT}?environment=ps2&service-id={self.service_id}'
        async with websockets.connect(url) as websocket:
            self.websocket = websocket
            _log.info(
                'Connected to %s?environment=ps2&service-id=XXX', _ESS_ENDPOINT)
            self._connected = True

            # Reset the backoff generator as the connection attempt was
            # successful
            self._reconnect_backoff = self._reset_backoff()

            # Keep processing websocket events until the connection dies or is
            # closed by the user or trigger system.
            while self._connect_lock.locked():
                try:
                    await self._handle_websocket()
                except websockets.exceptions.ConnectionClosed as err:
                    _log.info('Websocket connection closed (%d, %s)',
                              err.code, err.reason)  # type: ignore
                    await self.disconnect()
                    # NOTE: This will increment the reconnect delay each time,
                    # until one connection attempt is successful.
                    delay = next(self._reconnect_backoff)
                    _log.info(
                        'Next reconnection attempt in %.2f seconds', delay)
                    await asyncio.sleep(delay)
                    _log.info('Attempting to reconnect...')
                    self.loop.create_task(self.connect())

    async def disconnect(self) -> None:
        """Disconnect the websocket.

        Unlike :meth:`EventClient.close()`, this does not affect the
        HTTP session used by regular REST requests.

        """
        if self.websocket is None:
            return
        _log.info('Closing websocket connection')
        if self.websocket.open:
            await self.websocket.close()
        with contextlib.suppress(RuntimeError):
            self._connect_lock.release()
        self.websocket = None
        self._connected = False

    def dispatch(self, event: Event) -> None:
        """Dispatch an event to the appropriate event triggers.

        This goes through the list of triggers registered for this
        client and checks if the passed event matches the trigger's
        requirements using :meth:`Trigger.check()`.

        The call-backs for the matching triggers will be scheduled for
        execution in the current event loop using
        :meth:`asyncio.AbstractEventLoop.create_task()`.

        If a trigger's :attr:`Trigger.single_shot` attribute is set to
        True, the trigger will be removed from the client as soon as
        its call-back has been scheduled for execution. This means that
        when the action associated with a single-shot trigger runs, the
        associated trigger will no longer be registered for the client.

        Arguments:
            event: An event received through the event stream.

        """
        # Check for appropriate triggers
        for trigger in self.triggers:
            _log.debug('Checking trigger %s', trigger)
            if trigger.check(event):
                _log.debug('Scheduling trigger %s', trigger)
                self.loop.create_task(trigger.run(event))
                # Single-shot triggers self-unload as soon as their call-back
                # is scheduled
                if trigger.single_shot:
                    _log.info('Removing single-shot trigger %s', trigger)
                    self.remove_trigger(trigger)

    async def _handle_websocket(self, timeout: float = 0.1) -> None:
        """Main loop handling the websocket connection.

        This method processes event payloads, adds automatic reconnect
        capabilities and sends messages added to
        :attr:`EventClient._send_queue`.
        """
        if self.websocket is None:
            return
        try:
            response = str(await asyncio.wait_for(
                self.websocket.recv(), timeout=timeout))
        except asyncio.TimeoutError:
            # NOTE: This inner timeout try block is used to ensure
            # the websocket will regularly check for messages in
            # the client's _send_queue even when no messages are
            # being received.
            # Without this, awaiting self.websocket.recv() would
            # block events from being sent if no responses are
            # received.
            pass
        else:
            _log.debug('Received response: %s', response)
            self._process_payload(response)
        finally:
            if self._send_queue:
                msg = self._send_queue.pop(0)
                _log.info('Sending message: %s', msg)
                await self.websocket.send(msg)

    def trigger(self, event: Union[str, Event],
                *args: Union[str, Event], name: Optional[str] = None,
                **kwargs: Any) -> Callable[[_Callback], None]:
        """Create and add a trigger for the given action.

        If no name is specified, the call-back function's name will be
        used as the trigger name.

        Keep in mind that a trigger's name must be unique. A
        :class:`KeyError` will be raised if a trigger with this name
        already exists.

        Arguments:
            event: The event to trigger on.
            *args: Additional events that also trigger the action.
            name (optional): The name to assign to the trigger. If not
                specified, the call-back function's name will be used.
                Defaults to ``None``.

        Raises:
            KeyError: Raised if a trigger with the given name already
                exists.

        """
        trigger = Trigger(event, *args, name=name, **kwargs)

        def wrapper(func: _Callback) -> None:
            trigger.action = func
            # If the trigger name has not been specified, use the call-back
            # function's name instead
            if trigger.name is None:
                trigger.name = func.__name__
            # Ensure the trigger name is unique before adding the trigger
            if any(t.name == trigger.name for t in self.triggers):
                raise KeyError(f'The trigger "{trigger.name}" already exists')
            # If the name is unique, register the trigger to the client
            self.add_trigger(trigger)

        return wrapper

    def _process_payload(self, response: str) -> None:
        """Process a response payload received through the websocket.

        This method filters out any non-event messages (such as service
        messages, connection heartbeats or subscription echoes) before
        passing any event payloads on to :meth:`EventClient.dispatch()`.

        Arguments:
            response: The plain text response received through the ESS.

        """
        data: CensusData = json.loads(response)
        service = data.get('service')
        # Event messages
        if service == 'event':
            if data['type'] == 'serviceMessage':
                event = _event_factory(data['payload'])
                _log.debug('%s event received, dispatching...',
                           event.event_name)
                self.dispatch(event)
            elif data['type'] == 'heartbeat':
                _log.debug('Heartbeat received: %s', data)
        # Subscription echo
        elif 'subscription' in data:
            _log.debug('Subscription echo: %s', data)
        # Service state
        elif data.get('type') == 'serviceStateChange':
            _log.info('Service state change: %s', data)
        # Push service
        elif service == 'push':
            _log.debug('Ignoring push message: %s', data)
        # Help message
        elif 'send this for help' in data:
            _log.info('ESS welcome message: %s', data)
        # Other
        else:
            _log.warning('Unhandled message: %s', data)

    @staticmethod
    def _reset_backoff() -> Iterator[float]:
        """Reset the reconnect backoff generator."""
        return expo_scaled(factor=0.1, max_=30.0)()

    async def wait_for(self, trigger: Trigger, *args: Trigger,
                       timeout: Optional[float] = None) -> Event:
        """Wait for one or more triggers to fire.

        This method will wait until any of the given triggers have
        fired, or until the timeout has been exceeded.

        By default, any triggers passed will be automatically removed
        once the first has been triggered, regardless of the triggers'
        :attr:`Trigger.single_shot` setting.

        Arguments:
            trigger: A trigger to wait for.
            *args: Additional triggers that will also resume execution.
            timeout (optional): The maximum number of seconds to wait
                for; never expires if set to ``None``. Defaults to
                ``None``.

        Raises:
            TimeoutError: Raised if the given timeout is exceeded.

        Returns:
            The first event matching the given trigger(s).

        """
        # The following asyncio Event will pause this method until the trigger
        # fires or expires. Think of it as an asynchronous flag.
        async_flag = asyncio.Event()
        # Used to store the event received
        received_event: Optional[Event] = None

        triggers: List[Trigger] = [trigger]
        triggers.extend(args)

        def callback(event: Event) -> None:
            # Store the received event
            nonlocal received_event
            received_event = event
            # Remove the triggers. This suppresses any ValueErrors raised if
            # the trigger that fired was set to single shot mode.
            for trig in triggers:
                # NOTE: Due to Client.dispatch method being a normal method and
                # not a coroutine, it will always remove the trigger itself
                # before this call-back has any chance to fire (even through
                # the call-back itself is synchronous, it is wrapped in the
                # asynchronous Trigger.run method, causing this delay).
                #
                # This means that by the time this code is executed, the
                # trigger will already be removed, meaning that the ValueError
                # will always be raised here and not in Client.dispatch.
                with contextlib.suppress(ValueError):
                    self.remove_trigger(trig)
            # Set the flag to resume execution of the wait_for_event method
            async_flag.set()

        for trig in triggers:
            trig.action = callback
            self.add_trigger(trig)

        # Wait for the triggers to fire, or for the timeout to expire
        if timeout is not None and timeout <= 0.0:
            timeout = None
        try:
            await asyncio.wait_for(async_flag.wait(), timeout=timeout)
        except asyncio.TimeoutError as err:
            raise TimeoutError from err

        assert received_event is not None
        return received_event

    async def wait_ready(self, interval: float = 0.05) -> None:
        """Wait for the websocket connection to be ready.

        This will return once the websocket connection is open and
        active. This condition will be checked regularly as set by the
        ``interval`` argument.

        If the websocket is already active at the time this method is
        called, this will return without delay.

        Arguments:
            interval (optional): The interval at which to check the
                websocket connection's status. Defaults to ``0.05``.

        """
        if self._connected:
            return
        while not self._connected:
            await asyncio.sleep(interval)


def _event_factory(data: CensusData) -> Event:
    """Return the appropriate event type for the given payload.

    This will return the appropriate :class:`Event` subclass, or the
    base class itself if no matching subclass could be found. This can
    happen if new event types are introduced but not yet supported by
    the object model.

    Arguments:
        data: The "payload" sub-key of an event stream message.

    Returns:
        A dataclass representing the given event.

    """
    # TODO: Check for bad `data` passed
    for subclass in Event.__subclasses__():
        if subclass.event_name == data['event_name']:
            return subclass(**data)
    return Event(**data)

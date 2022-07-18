import asyncio
import contextlib
import json
import logging
from typing import (Any, Callable, Coroutine, Dict, List, Optional, Type,
                    TypeVar, Union, cast, overload)

import pydantic
import websockets
import websockets.client
import websockets.exceptions

from .._client import Client
from .._log import RedactingFilter
from ..models import Event
from ..types import CensusData
from ._trigger import Trigger

__all__ = [
    'EventClient'
]

_ESS_ENDPOINT = 'wss://push.planetside2.com/streaming'

_EventT = TypeVar('_EventT', bound=Event)
_EventT2 = TypeVar('_EventT2', bound=Event)
_CallbackT = Union[Callable[[_EventT], None],
                   Callable[[_EventT], Coroutine[Any, Any, None]]]
_CallableT = TypeVar('_CallableT', bound=Callable[..., Any])
_Decorator = Callable[[_CallableT], _CallableT]

_log = logging.getLogger('auraxium.ess')


class EventClient(Client):
    """Advanced client with event streaming capability.

    This subclass of :class:`auraxium.Client` extends the interface to
    also provide access to the WebSocket endpoint at
    ``wss://push.planetside2.com/streaming``.

    To use the websocket endpoint, you have to define a
    :class:`~auraxium.event.Trigger` and register it using the
    :meth:`add_trigger` method. This will automatically open a
    WebSocket connection is there is not already one running. Likewise,
    removing all event triggers from the client will cause the
    underlying websocket connection to close.

    Refer to the :class:`~auraxium.event.Trigger` class's documentation
    for details on how to use triggers and respond to events.

    .. attribute:: triggers
       :type: list[auraxium.event.Trigger]

       The list of :class:`Triggers <auraxium.event.Trigger>`
       registered for the client.

    .. attribute:: websocket
       :type: websockets.client.legacy.WebSocketClientProtocol | None

       The websocket client used for the real-time event stream. This
       will be automatically opened and closed by the client as event
       triggers are added and removed.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.triggers: List[Trigger] = []
        self.websocket: Optional[websockets.client.WebSocketClientProtocol] = None
        self._endpoint_status: Dict[str, bool] = {}
        self._send_queue: List[str] = []
        self._open: bool = False
        _log.addFilter(RedactingFilter(self.service_id))

    @property
    def endpoint_status(self) -> Dict[str, bool]:
        """Return endpoint status info.

        This returns a dictionary mapping API event server endpoints to
        their last reported status. This generally refreshes every 30
        seconds as part of the WebSocket heartbeat messages.
        """
        return self._endpoint_status

    def add_trigger(self, trigger: Trigger) -> None:
        """Add a new event trigger to the client.

        If there is currently no active websocket connection to the
        event streaming service, one will be created for this trigger.

        .. note::

           As this is a synchronous method, the WebSocket will not be
           active by the time this method returns.
           You can use :meth:`EventClient.wait_ready` to wait for the
           WebSocket being ready to process subscriptions.

        :param Trigger trigger: The trigger to add.
        """
        _log.debug('Adding trigger %s', trigger)
        self.triggers.append(trigger)
        subscription = trigger.generate_subscription()
        self._send_queue.append(subscription)
        # Only queue the connect() method if it is not already running
        if not self._open:
            _log.debug('Websocket not connected, scheduling connection')
            self.loop.create_task(self.connect())

    def get_trigger(self, name: str) -> Trigger:
        """Retrieve a registered event trigger by name.

        If the trigger cannot be found, a :exc:`KeyError` is raised.

        :param str name: The name of the trigger to return.
        :raises KeyError: Raised if no trigger with the given name is
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
        `keep_websocket_alive` flag to prevent this, for example if you
        intend to immediately add another trigger.

        :param trigger: The trigger to remove, or its unique name.
        :type trigger: Trigger or str
        :param bool keep_websocket_alive: If true, the websocket
           connection will be kept open even if the client has zero
           triggers remaining.
        :raises KeyError: Raised if a trigger name was passed and no
           trigger of this name exists for the client.
        :raises ValueError: Raised if no trigger of the given name is
           currently registered for this client.
        """
        if not isinstance(trigger, Trigger):
            trigger = self.get_trigger(trigger)
        _log.debug('Removing trigger %s', trigger)
        try:
            self.triggers.remove(trigger)
        except ValueError as err:  # pragma: no cover
            raise RuntimeError('The given trigger is not registered for '
                               'this client') from err
        # If this was the only trigger registered, close the websocket
        if not keep_websocket_alive and not self.triggers:
            _log.info('All triggers have been removed, closing websocket')
            self.loop.create_task(self.close())

    async def close(self) -> None:
        """Gracefully shut down the client.

        This will close the WebSocket connection and end any ongoing
        HTTP sessions used for requests to the REST API.

        Call this to clean up before the client object is destroyed.
        """
        await self.disconnect()
        await super().close()

    async def connect(self) -> None:
        """Connect to the websocket endpoint and process responses.

        This will continuously loop until :meth:`EventClient.close` is
        called.
        If the WebSocket connection encounters and error, it will be
        automatically restarted.

        Any event payloads received will be passed to
        :meth:`EventClient.dispatch` for filtering and event dispatch.
        """
        # NOTE: When multiple triggers are added to the bot without an active
        # websocket connection, this function may be scheduled multiple times.
        if self._open:  # pragma: no cover
            _log.debug('Websocket already running')
            return
        self._open = True
        await self._connection_handler()

    async def disconnect(self) -> None:
        """Disconnect the WebSocket.

        Unlike :meth:`EventClient.close`, this does not affect the HTTP
        sessions used by regular REST requests.
        """
        if not self._open:
            return
        self._open = False
        _log.info('Closing websocket connection')
        if self.websocket is not None and self.websocket.open:
            await self.websocket.close()

    def dispatch(self, event: Event) -> None:
        """Dispatch an event to the appropriate event triggers.

        This goes through the list of triggers registered for this
        client and checks if the passed event matches the trigger's
        requirements using
        :meth:`Trigger.check <auraxium.event.Trigger.check>`.

        The call-backs for the matching triggers will be scheduled for
        execution in the current event loop using
        :meth:`asyncio.loop.create_task`.

        If a trigger's
        :attr:`single_shot <auraxium.event.Trigger.single_shot>`
        attribute is set to true, the trigger will be removed from the
        client as soon as its call-back has been scheduled for
        execution. This means that when the action associated with a
        single-shot trigger runs, the associated trigger will no longer
        be registered for the client.

        :param auraxium.event.Event event: An event received through
           the event stream.
        """
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

    async def _connection_handler(self) -> None:
        """Internal WebSocket connection handler.

        This worker is designed to fail internally and be restarted by
        the :meth:`connect` method as per its reconnect policy.

        This should therefore only be called through that method.
        """
        _log.info('Connecting to WebSocket endpoint...')
        url = f'{_ESS_ENDPOINT}?environment=ps2&service-id={self.service_id}'

        # NOTE: The following "async for" loop will cleanly restart the
        # connection should it go down. Invoking "continue" manually may be
        # used to manually force a reconnect if needed.

        async for websocket in websockets.client.connect(url):
            _log.info('Connected to %s', url)
            self.websocket = websocket

            try:
                while self._open:
                    await self._handle_websocket()

            except websockets.exceptions.ConnectionClosed:
                _log.info('Connection closed, restarting...')
                continue

            if not self._open:
                break

        self.websocket = None
        _log.info('Disconnected from WebSocket endpoint')

    async def _handle_websocket(self, timeout: float = 0.1) -> None:
        """Main loop handling the WebSocket connection.

        This method processes event payloads and sends messages added
        to :attr:`EventClient._send_queue`.
        """
        if self.websocket is None:  # pragma: no cover
            return
        try:
            response = str(await asyncio.wait_for(
                self.websocket.recv(), timeout=timeout))
        except asyncio.TimeoutError:
            # NOTE: This inner timeout try block is used to ensure the
            # websocket will regularly check for messages in the client's
            # ``_send_queue`` even when no messages are received. Without this,
            # awaiting ``self.websocket.recv()`` would block subscriptions from
            # being sent until a heartbeat message is received, causing random
            # delays.
            pass
        else:
            self._process_payload(response)
        finally:
            if self._send_queue:
                msg = self._send_queue.pop(0)
                _log.info('Sending message: %s', msg)
                await self.websocket.send(msg)

    @overload
    def trigger(self, event: Type[_EventT], *, name: Optional[str] = None,
                **kwargs: Any) -> Callable[[_CallbackT[_EventT]], None]:
        # Single event variant (checks callback argument type)
        ...   # pragma: no cover

    @overload
    def trigger(self, event: Type[_EventT],
                arg1: Type[_EventT], *args: Type[_EventT2],
                name: Optional[str] = None, **kwargs: Any) -> Callable[
                    [_CallbackT[Union[_EventT, _EventT2]]], None]:
        # Two event variant (checks callback argument type)
        ...   # pragma: no cover

    @overload
    def trigger(self, event: Union[str, Type[Event]],
                *args: Union[str, Type[Event]], name: Optional[str] = None,
                **kwargs: Any) -> Callable[[_CallbackT[Event]], None]:
        # Generic fallback variant (callback argument type not checked)
        ...   # pragma: no cover

    def trigger(self, event: Union[str, Type[Event]],
                *args: Union[str, Type[_EventT]], name: Optional[str] = None,
                **kwargs: Any) -> Callable[[_CallbackT[Event]], None]:
        """Create and add a trigger for the given action.

        If no name is specified, the call-back function's name will be
        used as the trigger name.

        Keep in mind that a trigger's name must be unique. A
        :exc:`KeyError` will be raised if a trigger with this name
        already exists.

        :param event: The event to trigger on.
        :type event: str or typing.Type[auraxium.event.Event]
        :param args: Additional events that also trigger the action.
        :type args: str or typing.Type[auraxium.event.Event]
        :param name: The name to assign to the trigger. If not
           specified, the decorated function's name will be used.
        :type name: str or None
        :raises KeyError: Raised if a trigger with the given name
           already exists.
        """
        trigger = Trigger(event, *args, name=name, **kwargs)

        def wrapper(func: _CallbackT[_EventT]) -> None:
            trigger.action = func  # type: ignore
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
        """Process a response payload received through the WebSocket.

        This method filters out any non-event messages (such as service
        messages, connection heartbeats or subscription echoes) before
        passing any event payloads on to :meth:`dispatch`.

        :param str response: The plain text response received through
           the ESS.
        """
        _log.debug('Received response: %s', response)
        data: CensusData = json.loads(response)
        service = data.get('service')
        # Event messages
        if service == 'event':
            if data['type'] == 'serviceMessage':
                try:
                    event = _event_factory(cast(CensusData, data['payload']))
                except pydantic.ValidationError:  # pragma: no cover
                    _log.warning(
                        'Ignoring unsupported payload: %s\n'
                        'This message means that the Auraxium data model must '
                        'be updated. Please ensure you are on the latest '
                        'version of the Auraxium library and report this '
                        'message to the project maintainers.', data['payload'])
                    return
                _log.debug('%s event received, dispatching...',
                           event.event_name)
                self.dispatch(event)
            elif data['type'] == 'heartbeat':  # pragma: no cover
                servers = cast(Dict[str, str], data['online'])
                self._endpoint_status = {
                    k.split('_', maxsplit=2)[1]: v == 'true'
                    for k, v in servers.items()}
                _log.debug('Heartbeat received: %s', data)
        # Subscription echo
        elif 'subscription' in data:
            _log.debug('Subscription echo: %s', data)
        # Service state
        elif data.get('type') == 'serviceStateChange':  # pragma: no cover
            _log.info('Service state change: %s', data)
        # Push service
        elif service == 'push':
            _log.debug('Ignoring push message: %s', data)
        # Help message
        elif 'send this for help' in data:
            _log.info('ESS welcome message: %s', data)
        # Other
        else:  # pragma: no cover
            _log.warning('Unhandled message: %s', data)

    async def wait_for(self, trigger: Trigger, *args: Trigger,
                       timeout: Optional[float] = None) -> Event:
        """Wait for one or more triggers to fire.

        This method will wait until any of the given triggers have
        fired, or until the timeout has been exceeded.

        By default, any triggers passed will be automatically removed
        once the first has been triggered, regardless of the triggers'
        :attr:`~auraxium.event.Trigger.single_shot` setting.

        :param Trigger trigger: A trigger to wait for.
        :param Trigger args: Additional triggers that will also resume
           execution.
        :param timeout: The maximum number of seconds to wait for.
           Never expires if set to :obj:`None`.
        :type timeout: float or None
        :raises TimeoutError: Raised if `timeout` is exceeded.
        :return: The first event matching the given trigger(s).
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
        if timeout is not None and timeout <= 0.0:
            timeout = None
        try:
            await asyncio.wait_for(async_flag.wait(), timeout=timeout)
        except asyncio.TimeoutError as err:
            raise TimeoutError from err
        assert received_event is not None
        return received_event

    async def wait_ready(self, interval: float = 0.05) -> None:
        """Wait for the WebSocket connection to be ready.

        This will return once the WebSocket connection is open and
        active. This condition will be checked regularly as set by the
        `interval` argument.

        If the WebSocket is already active at the time this method is
        called, this will return without delay.

        :param float interval: The interval at which to check the
           WebSocket connection's status.
        """
        while self.websocket is None or not self.websocket.open:
            await asyncio.sleep(interval)


def _event_factory(data: CensusData) -> Event:
    """Return the appropriate event type for the given payload.

    This will return the appropriate :class:`~auraxium.event.Event`
    subclass, or the base class itself if no matching subclass could be
    found. This can happen if new event types are introduced but not
    yet supported by the object model.

    :param data: The "payload" sub-key of an event stream message.
    :type data: float or int or str
    :return: A pydantic model representing the given event.
    """
    if (event_name := data.get('event_name')) is not None:
        for subclass in Event.__subclasses__():
            if subclass.__name__ == event_name:
                return subclass(**cast(Any, data))
    # Fallback if the API ever adds new event types
    return Event(**cast(Any, data))  # pragma: no cover

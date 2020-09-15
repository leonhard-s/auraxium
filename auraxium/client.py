"""Defines the main client for Auraxium.

This includes both the core methods used to interface with the REST
API, as well as the websocket client used to access the real-time event
streaming service (ESS).

"""

import asyncio
import contextlib
import copy
import json
import logging
from typing import (Any, Callable, List, Literal, Optional, Type,
                    TYPE_CHECKING, TypeVar, Union)
from types import TracebackType

import aiohttp
import websockets

from .census import Query
from .event import ESS_ENDPOINT, Event, EventType, Trigger
from .request import run_query
from .types import CensusData

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. This avoids a circular import at runtime.
    from .base import Named, Ps2Object

__all__ = [
    'Client'
]

NamedT = TypeVar('NamedT', bound='Named')
Ps2ObjectT = TypeVar('Ps2ObjectT', bound='Ps2Object')
log = logging.getLogger('auraxium.client')


class Client:
    """The main client used to interface with the PlanetSide 2 API.

    This class handles access to both the REST API at
    ``https://census.daybreakgames.com/``, as well as the websocket
    endpoint at ``wss://push.planetside2.com/streaming``.

    To interface with the REST API, use the methods :meth:`Client.get`,
    :meth:`Client.find()`, or one of the ``Client.get_by_*()`` helpers.

    To use the websocket endpoint, you have to define a
    :class:`Trigger` and register it using the
    :meth:`Client.add_trigger()` method. This will automatically open
    the websocket connection if one does not exist.

    Refer to the :class:`Trigger` class's documentation for details on
    how to use triggers and respond to events.

    Attributes:
        loop: The :mod:`asyncio` event loop used by the client.
        service_id: The service ID identifying your app to the API. You
            can use the default value of ``'s:example'``, but you will
            likely run into rate limits. You can sign up for your own
            service ID at http://census.daybreakgames.com/#devSignup.
        session: The :class:`aiohttp.ClientSession` used for REST API
            requests.
        triggers: The list of :class:`Triggers <Trigger>` registered for
            the client.
        websocket: The websocket client used for the real-time event
            stream. This will be automatically opened and closed by the
            client as event triggers are added and removed.

    """

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None,
                 service_id: str = 's:example', profiling: bool = False
                 ) -> None:
        """Initialise a new Auraxium client.

        If loop is not specified, it will be retrieved is using
        :meth:`asyncio.get_event_loop()`.

        Arguments:
            loop (optional): A pre-existing event loop to use for the
                client. Defaults to ``None``.
            service_id (optional): The unique, private service ID of
                the client. Defaults to ``'s:example'``.
            profiling (optional): Whether to enable query and socket
                profiling.

        """
        self.loop = loop or asyncio.get_event_loop()
        self.profiling = profiling
        self._timing_cache: List[float] = []
        self.service_id = service_id
        self.session = aiohttp.ClientSession()
        self.triggers: List[Trigger] = []
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self._ws_connected: bool = False
        self._ws_lock = asyncio.Lock()
        self._ws_send_queue: List[str] = []

    async def __aenter__(self) -> 'Client':
        """Enter the context manager and return the client."""
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> Literal[False]:
        """Exit the context manager.

        This closes the internal HTTP session before exiting, no error
        handling will be performed.

        Arguments:
            exc_type: The type of exception that was raised.
            exc_value: The exception value that was raised.
            traceback: The traceback type of the exception.

        Returns:
            Always False, i.e. no error suppression.

        """
        await self.close()
        return False  # Do not suppress any exceptions

    @property
    def latency(self) -> float:
        """Return the average request latency for the client.

        This averages up to the last 100 query times. Use the logging
        utility to gain more insight into which queries take the most
        time.

        """
        if not self._timing_cache:
            return -1.0
        return sum(self._timing_cache) / len(self._timing_cache)

    def add_trigger(self, trigger: Trigger) -> None:
        """Add a new event trigger to the client.

        If there is currently no active websocket connection to the
        event streaming service, one will be created for this trigger.

        Note that the event loop will take a few cycles to get started,
        use the :meth:`Client.wait_ready()` method if you need to await
        the trigger being active.

        Arguments:
            trigger: The trigger to add.

        """
        log.debug('Adding trigger %s', trigger)
        self.triggers.append(trigger)
        subscription = trigger.generate_subscription()
        self._ws_send_queue.append(subscription)
        if self.websocket is None:
            log.debug('Websocket not connected, scheduling connection')
            self.loop.create_task(self._ws_connect())

    def find_trigger(self, name: str) -> Trigger:
        """Retrieve a registered event trigger by name.

        If the trigger cannot be found, a :class:`KeyError` is raised.

        Arguments:
            name: [description]

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
            trigger = self.find_trigger(trigger)
        log.debug('Removing trigger %s', trigger)
        try:
            self.triggers.remove(trigger)
        except ValueError as err:
            raise RuntimeError('The given trigger is not registered for '
                               'this client') from err
        # If this was the only trigger registered, close the websocket
        if not keep_websocket_alive and not self.triggers:
            log.info('All triggers have been removed, closing websocket')
            self.loop.create_task(self._ws_close())

    async def close(self) -> None:
        """Shut down the client.

        This will close the websocket connection, as well as end the
        HTTP session used for requests to the REST API.

        Call this to clean up before the client object is destroyed.

        """
        log.info('Shutting down client')
        await self._ws_close()
        await self.session.close()

    async def count(self, type_: Type[Ps2ObjectT], **kwargs: Any) -> int:
        """Return the number of items matching the given terms.

        Arguments:
            type_: The object type to search for.
            **kwargs: Any number of filters to apply.

        Returns:
            The number of entries entries.

        """
        return await type_.count(client=self, **kwargs)

    async def find(self, type_: Type[Ps2ObjectT], results: int = 10,
                   offset: int = 0, promote_exact: bool = False,
                   check_case: bool = True, **kwargs: Any) -> List[Ps2ObjectT]:
        """Return a list of entries matching the given terms.

        This returns up to as many entries as indicated by the results
        argument. Note that it may be fewer.

        Arguments:
            type_: The object type to search for.
            results (optional): The maximum number of results. Defaults
                to ``10``.
            offset (optional): The number of entries to skip. Useful
                for paginated views. Defaults to ``0``.
            promote_exact (optional): If enabled, exact matches to
                non-exact searches will always come first in the return
                list. Defaults to ``False``.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to ``True``.
            **kwargs: Any number of filters to apply.

        Returns:
            A list of matching entries.

        """
        return await type_.find(results=results, offset=offset,
                                promote_exact=promote_exact,
                                check_case=check_case, client=self, **kwargs)

    async def get(self, type_: Type[Ps2ObjectT], check_case: bool = True,
                  **kwargs: Any) -> Optional[Ps2ObjectT]:
        """Return the first entry matching the given terms.

        Like :meth:`Client.find()`, but will only return one item.

        Arguments:
            type_: The object type to search for.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to ``True``.
            **kwargs: Any number of filters to apply.

        Returns:
            The first matching entry, or ``None`` if not found.

        """
        return await type_.get(check_case=check_case, client=self, **kwargs)

    async def get_by_id(self, type_: Type[Ps2ObjectT], id_: int
                        ) -> Optional[Ps2ObjectT]:
        """Retrieve an object by its unique Census ID.

        Like :meth:`Client.get()`, but checks the local cache before
        performing the query.

        Arguments:
            type_: The object type to search for.
            id_: The unique ID of the object.

        Returns:
            The entry with the matching ID, or None if not found.

        """
        return await type_.get_by_id(id_, client=self)

    async def get_by_name(self, type_: Type[NamedT], name: str, *,
                          locale: str = 'en') -> Optional[NamedT]:
        """Retrieve an object by its unique name.

        Depending on the ``type_`` specified, this may retrieve a
        cached object, rather than querying the API.

        Keep in mind that not all :class:`Named` objects have a
        localised name; the ``locale`` argument has no effect in these
        cases.

        This query is always case-insensitive.

        Arguments:
            type_: The object type to search for.
            name: The name to search for.
            locale (optional): The locale of the search key. Defaults
                to ``'en'``.

        Returns:
            The entry with the matching name, or ``None`` if not found.

        """
        return await type_.get_by_name(name, locale=locale, client=self)

    async def request(self, query: Query, verb: str = 'get') -> CensusData:
        """Perform a REST API request.

        This performs the query and performs error checking to ensure
        the query is valid.

        Refer to the :meth:`auraxium.request.raise_for_dict()` method
        for a list of exceptions raised from API errors.

        Arguments:
            query: The query to perform.
            verb (optional): The query verb to utilise.
                Defaults to ``'get'``.

        Returns:
            The API response payload received.

        """
        if self.profiling:
            # Create a copy of the query before modifying it
            query = copy.copy(query)
            query.timing(True)
        data = await run_query(query, verb=verb, session=self.session)
        if self.profiling and verb == 'get':
            timing = data['timing']
            if log.level <= logging.DEBUG:
                url = query.url()
                log.debug('Query times for "%s?%s": %s',
                          '/'.join(url.parts[-2:]), url.query_string,
                          ', '.join([f'{k}: {v}' for k, v in timing.items()]))
            self._timing_cache.append(float(timing['total-ms']))
        return data

    def trigger(self, event: Union[str, EventType],
                *args: Union[str, EventType], name: Optional[str] = None,
                **kwargs: Any) -> Callable[[Callable[[Event], None]], None]:
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

        def wrapper(func: Callable[[Event], None]) -> None:
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
                # NOTE: Due to Client._ws_dispatch method being a normal method
                # and not a coroutine, it will always remove the trigger
                # itself before this call-back has any chance to fire (even
                # through the call-back itself is synchronous, it is wrapped in
                # the asynchronous Trigger.run() method, causing this delay).
                #
                # This means that by the time this code is executed, the
                # trigger will already be removed, meaning that the ValueError
                # will always be raised here and not in Client._ws_dispatch.
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
        if self._ws_connected:
            return
        while not self._ws_connected:
            await asyncio.sleep(interval)

    async def _ws_close(self) -> None:
        """Close the websocket connection."""
        if self._ws_connected:
            self._ws_connected = False
            if self.websocket is not None and self.websocket.open:
                await self.websocket.close()

    async def _ws_connect(self) -> None:
        """Connect to the websocket endpoint and process responses.

        This will continuously loop until :meth:`Client.close()` is
        called.

        Add payloads to :attr`Client._ws_send_queue` to schedule their
        transmission.

        Any payloads received will be passed to
        :meth:`Client._ws_dispatch()` for filtering and event dispatch.

        """
        await self._ws_lock.acquire()
        if self.websocket is not None:
            return
        log.info('Connecting to websocket endpoint...')
        url = f'{ESS_ENDPOINT}?environment=ps2&service-id={self.service_id}'
        async with websockets.connect(url) as websocket:
            log.info(
                'Connected to %s?environment=ps2&service-id=XXX', ESS_ENDPOINT)
            self.websocket = websocket
            self._ws_lock.release()
            # This loop will go on until this flag is unset, which is done by
            # the _ws_close() method.
            self._ws_connected = True
            while self._ws_connected:
                try:
                    try:
                        response = str(await asyncio.wait_for(
                            self.websocket.recv(), timeout=0.25))
                    except asyncio.TimeoutError:
                        # NOTE: This inner timeout try block is used to ensure
                        # the websocket will regularly check for messages in
                        # the client's _ws_send_queue even when no messages are
                        # being received.
                        # Without this, awaiting self.websocket.recv() would
                        # block events from being sent if no responses are
                        # received.
                        pass
                    else:
                        log.debug('Received response: %s', response)
                        self._ws_process(response)
                    finally:
                        if self._ws_send_queue:
                            msg = self._ws_send_queue.pop(0)
                            log.info('Sending message: %s', msg)
                            await self.websocket.send(msg)
                except websockets.exceptions.ConnectionClosed as err:
                    log.warning('Connection was closed, reconnecting: %s', err)
                    await self._ws_close()
                    await self._ws_connect()
                    return

    def _ws_dispatch(self, event: Event) -> None:
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
            log.debug('Checking trigger %s', trigger)
            if trigger.check(event):
                log.debug('Scheduling trigger %s', trigger)
                self.loop.create_task(trigger.run(event))
                # Single-shot triggers self-unload as soon as their call-back
                # is scheduled
                if trigger.single_shot:
                    log.info('Removing single-shot trigger %s', trigger)
                    self.remove_trigger(trigger)

    def _ws_process(self, response: str) -> None:
        """Process a response payload received through the websocket.

        This method filters out any non-event messages (such as service
        messages, connection heartbeats or subscription echoes) before
        passing any event payloads on to :meth:`Client._ws_dispatch()`.

        Arguments:
            response: The plain text response received through the ESS.

        """
        data: CensusData = json.loads(response)
        service = data.get('service')
        # Event messages
        if service == 'event':
            if data['type'] == 'serviceMessage':
                event = Event(data['payload'])
                log.debug('%s event received, dispatching...', event.type)
                self._ws_dispatch(event)
            elif data['type'] == 'heartbeat':
                log.debug('Heartbeat received: %s', data)
        # Subscription echo
        elif 'subscription' in data:
            log.debug('Subscription echo: %s', data)
        # Service state
        elif data.get('type') == 'serviceStateChange':
            log.info('Service state change: %s', data)
        # Push service
        elif service == 'push':
            log.debug('Ignoring push message: %s', data)
        # Help message
        elif 'send this for help' in data:
            log.info('ESS welcome message: %s', data)
        # Other
        else:
            log.warning('Unhandled message: %s', data)

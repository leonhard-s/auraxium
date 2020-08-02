"""Client object definition."""

import asyncio
import contextlib
import json
import logging
from typing import (Any, Callable, List, Literal, Optional, Type,
                    TYPE_CHECKING, TypeVar, Union)
from types import TracebackType

import aiohttp
import websockets

from .event import ESS_ENDPOINT, Event, EventType, Trigger
from .types import CensusData

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. During runtime, this would cause a circular import.
    from .base import Named, Ps2Object

__all__ = ['Client']

NamedT = TypeVar('NamedT', bound='Named')
Ps2ObjectT = TypeVar('Ps2ObjectT', bound='Ps2Object')
log = logging.getLogger('auraxium.client')


class Client:
    """The top-level interface for navigating the API."""

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None,
                 service_id: str = 's:example') -> None:
        """Initialise a new ARX client.

        If loop is not specified, it will be retrieved is using
        asyncio.get_event_loop().

        Args:
            loop (optional): A pre-existing event loop to use for the
                client. Defaults to None.
            service_id (optional): The unique, private service ID of
                the client. Defaults to 's:example'.

        """
        self._triggers: List[Trigger] = []
        self.locale: Optional[str] = None
        self.loop = loop or asyncio.get_event_loop()
        self.retry_queries = True
        self.service_id = service_id
        self.session = aiohttp.ClientSession()
        self.profiling = False
        self._ws: Optional[websockets.WebSocketClientProtocol] = None
        self._ws_connected = False
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

        Args:
            exc_type: The type of exception that was raised.
            exc_value: The exception value that was raised.
            traceback: The traceback type of the exception.

        Returns:
            Always False, i.e. no error suppression.

        """
        await self.close()
        return False  # Do not suppress any exceptions

    def add_trigger(self, trigger: Trigger) -> None:
        """Add a new trigger to the client.

        Arguments:
            trigger: The trigger to add.

        """
        log.debug('Adding trigger %s', trigger)
        self._triggers.append(trigger)
        subscription = trigger.generate_subscription()
        self._ws_send_queue.append(subscription)
        if self._ws is None:
            log.debug('Websocket not connected, scheduling connection')
            self.loop.create_task(self._ws_connect())

    def remove_trigger(self, trigger: Trigger) -> None:
        """Remove an existing trigger.

        Arguments:
            trigger: The trigger to remove.

        """
        log.debug('Removing trigger %s', trigger)
        with contextlib.suppress(ValueError):
            self._triggers.remove(trigger)
        if not self._triggers:
            log.info('All triggers have been removed, closing websocket')
            self.loop.create_task(self._ws_close())

    async def close(self) -> None:
        """Shut down the client."""
        log.info('Shutting down client')
        await self._ws_close()
        await self.session.close()

    async def count(self, type_: Type[Ps2ObjectT], **kwargs: Any) -> int:
        """Return the number of items matching the given terms.

        Args:
            type_: The object type to search for.
            **kwargs: Any number of filters to apply.

        Returns:
            The number of entries entries.

        """
        return await type_.count(client=self, **kwargs)

    async def find(self, type_: Type[Ps2ObjectT], results: int = 10,
                   offset: int = 0,
                   promote_exact: bool = False, check_case: bool = True,
                   **kwargs: Any) -> List[Ps2ObjectT]:
        """Return a list of entries matching the given terms.

        This returns up to as many entries as indicated by the results
        argument. Note that it may be fewer.

        Args:
            type_: The object type to search for.
            results (optional): The maximum number of results. Defaults
                to 10.
            offset (optional): The number of entries to skip. Useful
                for paginated views. Defaults to 0.
            promote_exact (optional): If enabled, exact matches to
                non-exact searches will always come first in the return
                list. Defaults to False.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to True.
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

        Like Ps2Object.get(), but will only return one item.

        Args:
            type_: The object type to search for.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to True.
            **kwargs: Any number of filters to apply.

        Returns:
            A matching entry, or None if not found.

        """
        return await type_.get(check_case=check_case, client=self, **kwargs)

    async def get_by_id(self, type_: Type[Ps2ObjectT], id_: int
                        ) -> Optional[Ps2ObjectT]:
        """Retrieve an object by its unique Census ID.

        Args:
            type_: The object type to search for.
            id_: The unique ID of the object.

        Returns:
            The entry with the matching ID, or None if not found.

        """
        return await type_.get_by_id(id_, client=self)

    async def get_by_name(self, type_: Type[NamedT], name: str, *,
                          locale: str = 'en') -> Optional[NamedT]:
        """Retrieve an object by its unique name.

        This query is always case-insensitive.

        Args:
            type_: The object type to search for.
            name: The name to search for.
            locale (optional): The locale of the search key. Defaults
                to 'en'.

        Returns:
            The entry with the matching name, or None if not found.

        """
        return await type_.get_by_name(name, locale=locale, client=self)

    def trigger(self, event: Union[str, EventType],
                *args: Union[str, EventType],
                name: Optional[str] = None, **kwargs: Any
                ) -> Callable[[Callable[[Event], None]], None]:
        """Create and add a trigger for the given callback.

        If no name is specified, the callback function's name will be
        used as the trigger name.

        Arguments:
            event: The event to trigger on.
            *args: Additional events that also trigger the callback.
            name: The name to assign to the trigger. If not specified,
                the callback function's name will be used.

        """
        trigger = Trigger(event, *args, name=name, **kwargs)

        def wrapper(func: Callable[[Event], None]) -> None:
            trigger.action = func
            if trigger.name is None:
                trigger.name = func.__name__

        self.add_trigger(trigger)
        return wrapper

    async def wait_for(self, trigger: Trigger, *args: Trigger,
                       timeout: float = 0.0) -> Event:
        """Wait for one or more triggers to fire.

        This methods creates any number of single-shot triggers and
        waits for them to complete, or until the timeout is reached.

        Any triggers passed will be set to single shot mode.

        Arguments:
            trigger: A trigger to wait for.
            *args: Additional triggers that will also resume execution.
            timeout (optional): The maximum number of seconds to wait
                for; never expires if set to 0.0. Defaults to ``0.0``.

        Raises:
            TimeoutError: Raised if the timeout is exceeded.

        Returns:
            The first event matching the given trigger(s).
        """
        # The following asyncio Event will pause this method until the trigger
        # fires or expires. Think of it as an asynchronous flag.
        async_flag = asyncio.Event()
        # Create a new, single-shot trigger to detect the given event
        _received_event: Optional[Event] = None

        triggers: List[Trigger] = [trigger]
        triggers.extend(args)

        def callback(event: Event) -> None:
            # Store the received event
            _received_event = event
            for trigger in triggers:
                self.remove_trigger(trigger)
            # Set the flag to resume execution of the wait_for_event method
            async_flag.set()

        for trig in triggers:
            trig.single_shot = True
            trig.callback = callback
            self.add_trigger(trig)

        # Wait for the triggers to fire, or for the timeout to expire
        if timeout <= 0.0:
            timeout = None
        try:
            await asyncio.wait_for(async_flag.wait(), timeout=None)
        except asyncio.TimeoutError as err:
            raise TimeoutError from err
        return _received_event

    async def _ws_close(self) -> None:
        if self._ws_connected:
            self._ws_connected = False
            if self._ws is not None and self._ws.open:
                await self._ws.close()

    async def _ws_connect(self) -> None:
        if self._ws is not None:
            log.warning('A websocket connection is already open, closing...')
            await self._ws.close()
        log.info('Connecting to websocket endpoint...')
        self._ws_connected = True

        url = f'{ESS_ENDPOINT}?environment=ps2&service-id={self.service_id}'
        async with websockets.connect(url) as websocket:
            log.info('Connected')
            self._ws = websocket
            # This loop will go on until the "close" method is called.
            while self._ws_connected:
                try:
                    try:
                        response: str = await asyncio.wait_for(
                            self._ws.recv(), timeout=0.5)
                    except asyncio.TimeoutError:
                        if self._ws_send_queue:
                            msg = self._ws_send_queue.pop(0)
                            log.info('Sending message: %s', msg)
                            await self._ws.send(msg)
                    else:
                        log.debug('Received response: %s', response)
                        self._ws_process_response(response)
                except websockets.exceptions.ConnectionClosed as err:
                    log.warning('Connection was closed, reconnecting: %s', err)
                    await self._ws_close()
                    await self._ws_connect()
                    return

    def _ws_process_response(self, response: str) -> None:
        """Process a response received through the ESS."""
        data: CensusData = json.loads(response)

        # Ignored messages

        # These messages are not relevant to the ESS and will be ignore completely.
        if ('send this for help' in data or data.get('service') == 'push'
                or data.get('type') == 'serviceStateChange'):
            return
        # Subscription echo
        # When the ESS sees a subscription message, it echos it back to confirm the subscription
        # has been registered.
        if 'subscription' in data:
            log.debug('Subscription echo: %s', data)
            return
        # Heartbeat
        # For as long as the connection is alive, the server will broadcast the status for all of
        # the API endpoints. While technically a service message, it is filtered out here to keep
        # things tidy.
        if data['service'] == 'event' and data['type'] == 'heartbeat':
            log.debug('Heartbeat received')
            return

        # Event messages
        if data['service'] == 'event' and data['type'] == 'serviceMessage':
            event = Event(data['payload'])
            # Check for appropriate triggers
            for trigger in self._triggers:
                log.debug('Checking trigger %s', trigger)
                if trigger.check(event):
                    log.info('Scheduling trigger %s', trigger)
                    self.loop.create_task(trigger.run(event))
                    if trigger.single_shot:
                        log.info('Removing single-shot trigger %s', trigger)
                        self.remove_trigger(trigger)

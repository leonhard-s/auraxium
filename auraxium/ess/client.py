"""This module contains the definition for the ESS Client object.

It handles basic operations like connecting or disconnecting and
processes responses received through the websocket connection.
"""

import asyncio
import collections
import json
import logging
import time
from typing import Callable, List, Optional, Union
import websockets

from ..object_models.ps2 import Character, World

from .constants import ESS_ENDPOINT
from .events import Event, arx_name_to_type, Centricity, check_centricity
from .exceptions import UnknownEventTypeError
from .listener import EventListener


# Create a logger
logger = logging.getLogger('auraxium.ess')  # pylint: disable=invalid-name


class Client():
    """The ESS client object.

    This object handles the websocket connection itself and parses any
    responses received, running the applicable `EventListeners`.

    Parameters
    ----------
    `loop` (Optional): The event loop to use.
    """

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self._event_listeners: List[EventListener] = []
        self._is_open: bool = False
        self.loop: asyncio.AbstractEventLoop = (
            loop if loop is not None else asyncio.get_event_loop())
        self._send_queue: List[str] = []
        self._websocket: Optional[websockets.WebSocketClientProtocol] = None

        # The following dictionary keeps basic statistics about the client
        stats = collections.namedtuple('ClientStats', 'endpoint_last_saved endpoint_status '
                                       'latency_last_saved latency_list')
        self._stats = stats(0, [], 0, [])

    async def close(self) -> None:
        """Closes the websocket connection of the client.

        The client can be restarted by running the `Client.connect()`
        method.
        """

        # Only proceed if the client is actually open.
        if not self._is_open:
            return
        if self._websocket is not None and self._websocket.open:
            await self._websocket.close()

    async def connect(self, service_id: str = 's:example', namespace: str = 'ps2') -> None:
        """Connect to the event streaming service.

        Establishes a connection with the ESS. This method will loop
        until the `Client.close()` method is called.

        Parameters
        ----------
        `service_id` (Optional): The service ID to use with the event
        client.

        `namespace` (Optional): The namespace (or game) to connect to.
        Currently, only PS2 namespaces are supported. Defaults to
        "ps2".
        """

        # If the client is already running, close it before restarting
        if self._is_open:
            await self.close()

        # Generate the URL required for connecting
        url = ESS_ENDPOINT + '?environment=' + namespace + '&service-id=' + service_id

        # Mark the conenction as open
        self._is_open = True

        # Open the websocket connection itself
        async with websockets.connect(url) as websocket:
            self._websocket = websocket

            # This loop runs until the flag is being unset by a Client.close() call
            while self._is_open:
                try:
                    # Wait for a new message from the endpoint and process it
                    self._process_response(await self._websocket.recv())

                    # If there are any items in the send queue, pick one and send it off
                    try:
                        await self._websocket.send(self._send_queue.pop(0))
                    except IndexError:
                        pass

                # If the connection is lost, log the incident and try to reconnect immediately
                except websockets.exceptions.ConnectionClosed as err:
                    logger.info('Connection closed. Error:\n%s', err)
                    await self.close()
                    await self.connect(service_id=service_id, namespace=namespace)

    def event(self, *args: str, characters: Optional[List[Union[int, Character]]] = None,
              worlds: Optional[List[Union[int, World]]] = None) -> Callable:
        """Decorator used to create ESS event listeners.

        The decorated function can either be a standard function or an
        asyncio generator.

        Any non-keyword arguments passed will be interpreted as event
        names to listen for. Keep the centricity of an event in mind
        when registering events (e.g. a "ContinentLock" event cannot
        be registered for a character).

        Additionally, if the function name starts with "on_", the rest
        of the function name will be interpreted as an event name to
        register.

        Parameters
        ----------
        `args`: Any non-keyword arguments passed will be treated as
        event names to register.

        `characters` (Optional): A list of Character objects or IDs to
        register events for.

        `worlds` (Optional): A list of World objects or IDs to register
        events for.

        Raises
        ------
        `ValueError`: Raised when no event names have been specified in
        the arguments and none could be inferred from the decorated
        function's name.
        """

        def inner_decorator(func: Callable) -> None:
            """Actual decorator for event creation.

            This function primarily adds the decorated function to the
            event listener for it.
            """

            # Create a list of all event names to register this event listener for
            types_to_register = [arx_name_to_type(e) for e in args]

            # If the function name starts with "on_" and the remainder is a sensible event name,
            # add it to the event names to register.
            if func.__name__.startswith('on_'):
                try:
                    # If this fails, the remaining function name is not a valid event.
                    event_type = arx_name_to_type(arx_name=func.__name__[3:])
                    types_to_register.append(event_type)

                except UnknownEventTypeError as err:
                    # If no arguments have been passed, raise an error
                    if not types_to_register:
                        raise ValueError('No event names specified, unable to infer function '
                                         'name') from err

            # Make sure the event names do not violate centricity
            for event_type in types_to_register:

                if (characters is not None and not check_centricity(
                        event_type, Centricity.CHARACTER)):
                    raise ValueError(
                        'Event type is not character-centric: {}'.format(event_type))
                if worlds is not None and not check_centricity(event_type, Centricity.WORLD):
                    raise ValueError(
                        'Event type is not world-centric: {}'.format(event_type))

            # Create and add a new event listener
            listener = EventListener(
                *types_to_register, function=func, worlds=worlds, characters=characters)

            # Register the event listener
            self._event_listeners.append(listener)

            # Add the event_listeners subscription information to the send queue
            self._send_queue.append(listener.subscribe())

        return inner_decorator

    def _process_response(self, response: str) -> None:
        """Processes a response received through the ESS.

        Depending on the type of message received, this will either
        update the internal statistics of the client or trigger any
        number of matching event listeners to fire.

        Parameters
        ----------
        `response`: The JSON string received by the client.
        """

        data = json.loads(response)

        # Ignored messages
        # ----------------
        # These messages are not relevant to the ESS and will be ignore completely.
        if ('send this for help' in data or data.get('service') == 'push'
                or data.get('type') == 'serviceStateChange'):
            return

        # Subscription echo
        # -----------------
        # When the ESS sees a subscription message, it echos it back to confirm the subscription
        # has been registered.
        if 'subscription' in data:
            # print('Subscription echo: {}'.format(data))
            return

        # Heartbeat
        # ---------
        # For as long as the connection is alive, the server will broadcast the status for all of
        # the API endpoints. While technically a service message, it is filtered out here to keep
        # things tidy.
        if data['service'] == 'event' and data['type'] == 'heartbeat':
            # print('Heartbeat: {}'.format(data))
            return

        # Event service
        # -------------
        # Service messages, i.e. events the client has subscribed to.
        if data['service'] == 'event' and data['type'] == 'serviceMessage':

            # Put the payload into its own dict to increase legibility
            payload: dict = data['payload']

            # Calculate the current latency
            now: int = round(time.time())
            # Only log every five seconds
            if now - self._stats.latency_last_saved > 5:
                latency = now - int(payload['timestamp'])
                # Append the value
                self._stats.latency_list.append(latency)
                # Only store the last 100 datapoints; cut off the excess
                if len(self._stats.latency_list) > 100:
                    self._stats.latency_list.pop(0)

            # Event processing
            event: Event = Event.get(payload)

            # Create a list of all functions that need to be run
            functions_to_run = [
                el.function for el in self._event_listeners if event.type in el.events]

            # Run the functions
            for function in functions_to_run:
                if asyncio.iscoroutinefunction(function):
                    self.loop.create_task(function(event=event))
                else:
                    function(event=event)

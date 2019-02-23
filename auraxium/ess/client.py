import asyncio
import collections
import json
import logging
import time
from typing import Callable, List, Optional
import websockets

from .listener import EventListener
from .events import Centricity, check_centricity, Event, get_event, string_to_event_type
from .typing import CharacterOrID, WorldOrID


# The endpoint used for connecting to the ESS
_ENDPOINT = 'wss://push.planetside2.com/streaming'


# Create a logger
logger = logging.getLogger('auraxium.ess')  # pylint: disable=invalid-name


class Client():
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self._event_listeners: List[EventListener] = []
        self._is_open = False
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self._send_queue: List[str] = []
        self._websocket: Optional[websockets.WebSocketClientProtocol] = None

        # The following dictionary keeps basic statistics about the client
        ClientStats = collections.namedtuple('ClientStats', 'endpoint_last_saved endpoint_status '
                                             'latency_last_saved latency_list')
        self._stats = ClientStats(0, [], 0, [])

    async def close(self):
        """Closes the websocket connection and stops the client."""

        if not self._is_open:
            return
        if self._websocket is not None and self._websocket.open:
            await self._websocket.close()

    async def connect(self, service_id: str = 's:example', namespace: str = 'ps2') -> None:
        """Connects to the ESS using the namespaces given.

        The namespace defaults to 'ps2' if omitted.
        """

        # If the client is already running, restart it
        if self._is_open:
            await self.close()

        # Generate the URL required for connecting to the ESS
        url = _ENDPOINT + '?environment=' + namespace + '&service-id=' + service_id

        # Mark the conenction as open
        self._is_open = True

        # Create the websocket connection itself
        async with websockets.connect(url) as ws:
            self._websocket = ws

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
                except websockets.exceptions.ConnectionClosed as e:
                    logger.info('Connection closed. Error:\n%s', e)
                    await self.close()
                    await self.connect(service_id=service_id, namespace=namespace)

    def event(self, *args: str, characters: Optional[List[CharacterOrID]] = None,
              worlds: Optional[List[WorldOrID]] = None) -> Callable:
        """Decorator used to create ESS event listeners.

        Any non-keyword arguments passed to this decorator will be interpreted as
        event names to register.
        The "characters" and "worlds" keyword arguments are optionally used to filter the events
        by player or server respectively.
        """

        def inner_decorator(func: Callable) -> None:
            event_name_list = [string_to_event_type(e) for e in args]

            # Create and add a new event listener
            event_listener = EventListener(
                *event_name_list, function=func, worlds=worlds, characters=characters)

            # Create a list of all event names to register this event listener for
            if args:
                names_to_register = list(args)

            else:
                function_name = func.__name__

                # See if the function name matches the "on_<event_name>" pattern
                if not function_name.startswith('on_'):
                    raise ValueError('No event name specified, unable to infer from function name')

                # Register the event listener for this function name
                names_to_register = [function_name[3:]]

            # Check centricity of passed events
            for event_name in names_to_register:

                # Retrieve the event type for the given event name to make sure it exists
                event_type = string_to_event_type(event_name)

                # If it does, check centricity
                if characters is not None and not check_centricity(event_type,
                                                                   Centricity.CHARACTER):
                    raise ValueError('Event type is not character-centric: {}'.format(event_name))
                if worlds is not None and not check_centricity(event_type, Centricity.WORLD):
                    raise ValueError('Event type is not world-centric: {}'.format(event_name))

            # Register the event listener
            self._event_listeners.append(event_listener)

            # Add the event_listeners subscription information to the send queue
            self._send_queue.append(event_listener.subscribe())

        return inner_decorator

    def _process_response(self, response: str) -> None:
        """Processes the response received through the ESS.

        Depending on the type of message received, this will cause any
        number of event listeners to fire.
        """

        data = json.loads(response)

        # Ignored messages
        # These messages are not relevant to the ESS and will be ignore completely.
        if ('send this for help' in data or data.get('service') == 'push'
                or data.get('type') == 'serviceStateChange'):
            return

        # Subscription echo
        # When the ESS sees a subscription message, it echos it back to confirm the subscription
        # has been registered.
        if 'subscription' in data:
            # print('Subscription echo: {}'.format(data))
            return

        # Heartbeat
        # For as long as the connection is alive, the server will broadcast the status for all of
        # the API endpoints. While technically a service message, it is filtered out here to keep
        # things tidy.
        if data['service'] == 'event' and data['type'] == 'heartbeat':
            # print('Heartbeat: {}'.format(data))
            return

        # Event service
        # Service messages, i.e. responses for events the client has subscribed to.
        if data['service'] == 'event' and data['type'] == 'serviceMessage':

            # Put the payload into its own dict to increase legibility
            payload: dict = data['payload']

            # Latency
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
            event: Event = get_event(payload)

            # Create a list of all functions that need to be run
            functions_to_run = [
                el.function for el in self._event_listeners if event.type in el.events]

            # Run the functions
            for function in functions_to_run:
                if asyncio.iscoroutinefunction(function):
                    self.loop.create_task(function(event=event))
                else:
                    function(event=event)

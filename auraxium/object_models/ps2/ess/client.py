import asyncio
import json
import logging
from time import time

import websockets

from .event import get_event, EventListener


_ENDPOINT = 'wss://push.planetside2.com/streaming'
_NAMESPACE = 'ps2'


# Create a logger
logger = logging.getLogger('auraxium.ess')


class Client():
    """The client used for connecting the the PS2 Event Streaming Service.

    Use the "add_listener" method to choose events to receive. Any events
    received will be forwarded to any "@event" decorators listening for that
    event type.

    """

    def __init__(self, loop=None):
        self._events = {}
        self._is_open = False
        self._event_listeners = []
        self.latency = []
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self._send_queue = []
        self._websocket = None

    def add_listener(self, event, characters=None, worlds=None):
        """Adds a new event listener.

        Groups one or more events for a set of characters or worlds. If the
        criteria are met, the corresponding event event message is broadcast.

        """

        event_listener = EventListener(events=[event], characters=characters,
                                       worlds=worlds)
        self._send_queue.append(json.dumps(event_listener.subscribe()))
        self._event_listeners.append(event_listener)
        return event_listener

    def event(self, func):
        """Decorator used for defining events.

        After registering an event using this decorator, the corresponding
        method is run every time an event message with its name is broadcast.

        """

        try:
            self._events[func.__name__].append(func)
        except KeyError:
            self._events[func.__name__] = [func]
        return func

    async def close(self):
        """Closes the ESS client.

        Closes the client's websocket connection, thus preventing any new
        events from being received.

        """

        if not self._is_open:
            return
        if self._websocket is not None and self._websocket.open:
            await self._websocket.close()

    async def connect(self):
        """Start the ESS client.

        Initializes the client and opens the websocket connection required to
        receive ESS events.

        """

        # Import the service_id from the core auraxium module
        from .... import service_id

        url = _ENDPOINT + '?environment=' + _NAMESPACE + '&service-id=' + service_id

        # Mark the connection as open
        self._is_open = True

        # Create the websocket connection
        async with websockets.connect(url) as websocket:
            self._websocket = websocket
            # This loop runs until the flag is being unset by a "close()" call
            while self._is_open:
                try:
                    self._process_response(await websocket.recv())
                    try:
                        await self._websocket.send(self._send_queue.pop(0))
                    except IndexError:
                        pass

                # If connection is lost, log the incident and try to reconnect
                except websockets.exceptions.ConnectionClosed as e:
                    logger.info('Connection closed. Error:\n%s', e)
                    await self.close()
                    await self.connect()

    def _process_response(self, data):
        """Processes responses received through the ESS.

        Processes the response and broadcasts any applicable event messages
        to the corresponding event listeners.

        """

        response = json.loads(data)

        # Ignored messages
        if ('send this for help' in response
                or 'subscription' in response
                or response['service'] == 'push'
                or response['type'] == 'serviceStateChanged'):
            return

        # Event streaming service
        if (response['service'] == 'event'
                and response['type'] == 'serviceMessage'):

            # Latency
            self.latency.append(time() - int(response['payload']['timestamp']))
            if len(self.latency) > 100:
                self.latency.pop(0)

            # Event processing
            event = get_event(response['payload'])

            # Create a list of all messages that need to be sent out
            messages = [
                el.message for el in self._event_listeners if el.evaluate(event)]

            # Run/queue the corresponding functions
            functions_to_run = [
                f for m in messages for f in self._events[m]]

            # Run the functions
            for function in functions_to_run:
                if asyncio.iscoroutinefunction(function):
                    self.loop.create_task(function(event=event))
                else:
                    function(event=event)
            return

    def start(self):
        """Shorthand for starting the event client.

        Starts the event client and keeps it open. This method runs asyncio's
        "run_forever()" method and is a blocking call. Run the client's
        "connect()" method manually if you require multitasking capability.

        """

        self.loop.create_task(self.connect())
        self.loop.run_forever()

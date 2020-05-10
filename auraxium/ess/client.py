import asyncio
import json
from typing import Iterable, List, Optional
import websockets
from .constants import ESS_ENDPOINT
from .event import Event
from .trigger import Trigger


class Client():
    """The main client used for interacting with the ESS API.

    This class wraps the underlying websocket connection established
    using the `connect` method, and is responsible for dispensing the
    corresponding events as they are encountered.
    """

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self._is_connected = False
        self._send_queue: List[str] = []
        self._triggers: List[Trigger] = []
        self._websocket: Optional[websockets.WebSocketClientProtocol] = None

    async def connect(self, service_id='s:example', namespace='ps2') -> None:
        """Start the event streaming client.

        Opens the underlying websocket connection to the ESS. This
        method will not return until the `close` method is called.
        """
        # If the client is already running, close it before restarting it
        if self._is_connected:
            await self.close()
        # Generate the URL required for connection
        url = f'{ESS_ENDPOINT}?environment={namespace}&service-id={service_id}'
        # Open the websocket connection
        self._is_connected = True
        async with websockets.connect(url) as websocket:
            self._websocket = websocket
            # This loop repeats until the "close" method is called
            while self._is_connected:
                # The outer try block gives some redundancy against connection
                # drop-outs by automatically reconnecting.
                try:
                    # The inner try block employs a timeout to prevent the
                    # global asyncio event loop from being blocked by a stale
                    # or low-activity ESS connection.
                    try:
                        response: str = await asyncio.wait_for(
                            self._websocket.recv(), timeout=0.5)
                        self._process_response(response)
                    except asyncio.TimeoutError:
                        # If there are any items in the send queue, pick one
                        try:
                            await self._websocket.send(self._send_queue.pop(0))
                        except IndexError:
                            pass
                except websockets.exceptions.ConnectionClosed as err:
                    # Print the error and attempt to reconnect
                    print(err)
                    await self.close()
                    await self.connect(service_id=service_id, namespace=namespace)

    def _process_response(self, response: str) -> None:
        """Process a response received through the ESS."""
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
            # print('(Heartbeat received)')
            return
        # Event messages
        if data['service'] == 'event' and data['type'] == 'serviceMessage':
            event = Event(data['payload'])
            # Run the appropriate callbacks
            for t in self._triggers:
                # Only proceed if the trigger matches
                if not t.evaluate(data['payload']):
                    continue
                self.loop.create_task(t.run(event))
                if t.single_shot:
                    self._remove_trigger(t)

    async def close(self) -> None:
        """Closes the client's underlying websocket connection."""
        # Only proceed if the connection is open
        if not self._is_connected:
            return
        self._is_connected = False
        if self._websocket is not None and self._websocket.open:
            await self._websocket.close()

    def _add_trigger(self, trigger: Trigger) -> None:
        """Add a new trigger to a the client."""
        self._triggers.append(trigger)
        self._send_queue.append(trigger.generate_subscription())

    def _remove_trigger(self, trigger: Trigger) -> None:
        """Removes a trigger from the client.

        Raises:
          * ValueError -- Raised if the given trigger has not been
            added yet
        """
        try:
            self._triggers.remove(trigger)
        except ValueError as err:
            msg = 'The given trigger could not be found'
            raise ValueError(msg) from err
        # TODO: Clean-up code for tidying up orphan subscriptions

    async def wait_for_event(self, event_name: str, *args: str,
                             character_ids: Iterable[int] = [],
                             world_ids: Iterable[int] = [],
                             timeout=0.0) -> Event:
        """Wait for one or more events.

        This method creates a single-shot trigger matching the given
        event name.
        """
        # The following asyncio Event will pause this method until the trigger
        # fires or expires. Think of it as an asynchronous flag.
        async_flag = asyncio.Event()
        # Create a new, single-shot trigger to detect the given event
        trigger = Trigger(event_name, *args, character_ids=character_ids,
                          world_ids=world_ids, single_shot=True)
        _received_event: Optional[Event] = None

        @trigger.set_callback
        def callback(event: Event) -> None:
            # Store the received event
            _received_event = event
            # Set the flag to resume execution of the wait_for_event method
            async_flag.set()

        self._add_trigger(trigger)
        # Wait for the trigger to fire, or for the timeout to expire
        try:
            await asyncio.wait_for(async_flag.wait(), timeout=timeout)
        except TimeoutError as err:
            raise TimeoutError from err
        return _received_event

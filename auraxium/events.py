import asyncio
import json
from enum import Enum

import websockets

_BASE_URL = 'wss://push.planetside2.com/streaming'

# Namespace - available values are "ps2", "ps2ps4us" and "ps2ps4eu"
_NAMESPACE = 'ps2'
_SERVICE_ID = 's:example'


class Event():
    def __init__(self, name, character_centric=False, exp_id=None,
                 world_centric=False):
        self.character_centric = character_centric
        self.exp_id = exp_id
        self.fields = {}
        self.world_centric = world - world_centric
        self.name = name

    def __str__(self):
        return self.name


class Client():
    """A PS2 Streaming event that can be subscribed to."""

    def __init__(self, loop=None):
        self.is_closed = True
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self._listeners = []
        self._send_queue = []
        self._ws = None

    async def close(self):
        """Closes the connection and all that good stuff."""
        if self.is_closed:
            return

        if self._ws is not None and self._ws.open:
            await self._ws.close()

    async def connect(self):
        """Creates a websocket connection."""
        url = _BASE_URL + '?environment=' + _NAMESPACE + '&service-id=' + _SERVICE_ID

        # Mark the connection as open
        self.is_closed = False

        async with websockets.connect(url) as websocket:
            self._ws = websocket

            while not self.is_closed:
                try:
                    str = await websocket.recv()
                    # Process the response
                    self._process_response(str)

                    for item in self._send_queue:
                        await websocket.send(self._send_queue.pop())

                except websocket.ConnectionClosed as e:
                    await self.close()

    def event(self, func):
        """Decorator used for creating events."""

        self._listeners.append(func)
        return func

    def _process_response(self, str):
        """Internal. Runs whenever a message is received."""

        response = json.loads(str)

        # Subscription push echo
        if 'subscription' in response:
            print('[SUBS] {}'.format(response))
            return

        # Help message
        elif "send this for help" in response:
            print('[HELP] {}'.format(response))
            return

        # Login service
        elif response['service'] == "push":
            print('[LOGIN] {}'.format(response))
            return

        # Event streaming service
        elif response['service'] == 'event':

            # Endpoint state change echo
            if response['type'] == 'serviceStateChanged':
                print('[ENDPOINT] {}'.format(response))
                return

            # Heartbeat
            if response['type'] == 'heartbeat':
                print('[HEARTBEAT] {}'.format(response))
                return

            # Event responses
            if response['type'] == 'serviceMessage':
                # print('[EVENT] {}'.format(response))
                listeners_to_run = [l for l in self._listeners if l.__name__ == 'on_{}'.format(
                    response['payload']['event_name'].lower())]
                for listener in listeners_to_run:
                    listener(response['payload'])
                return

        print('[WARNING] Unexpected response: {}'.format(response))

    def sub(self, event, **kwargs):
        """Shorthand for subscribe."""
        self.subscribe(event, kwargs)

    def subscribe(self, event, character_list, **kwargs):
        """Subscribes to a PS2 Event."""

        json_data = json.dumps(
            {'action': 'subscribe',
             'characters': list(character_list),
             'eventNames': [event],
             'service': 'event'})

        print('[EVENTS] Subscribing using command:')
        print(json_data)
        self._send_queue.append(json_data)
        # await self.ws.send(json_data)

    def clear_subs(self):
        """Shorthand for clear_subscriptions."""
        self.clear_subscriptions()

    def clear_subscriptions(self):
        """Clears all subscriptions."""
        data = {'service': 'event',
                'action': 'clearSubscribe',
                'all': 'true'}
        print('[EVENTS] Clearing all subscriptions...')
        # await self.ws.send(json.dumps(data))

    def unsub(self, **kwargs):
        """Shorthand for unsubscribe."""
        self.unsubscribe(kwargs)

    def unsubscribe(self, events, **kwargs):
        """Unsubscribes from a PS2 Event."""
        character_list = [1, 2]
        event_list = []
        world_list = [1, 2]

        data = {'action': 'clearSubscribe',
                'characters': character_list,
                'eventNames': event_list,
                'service': 'event',
                'worlds': world_list}

        json_data = json.dumps(data)
        print('[EVENTS] Subscribing using command:')
        print(json_data)
        # await self.ws.send(json_data)


event_list = ['AchievementEarned',  # Character-centric events
              'BattleRankUp',
              'Death',
              'ItemAdded',
              'SkillAdded',
              'VehicleDestroy',
              'GainExperience',
              'PlayerFacilityCapture',
              'PlayerFacilityDefend',
              'ContinentLock',  # World-centric events
              'ContinentUnlock',
              'FacilityControl',
              'MetagameEvent',
              'PlayerLogin',  # World-centric and character-centric events
              'PlayerLogout']

import asyncio
import json
import logging
from enum import Enum

import websockets

# Create a logger
logger = logging.getLogger('auraxium.events')

_BASE_URL = 'wss://push.planetside2.com/streaming'

# Namespace - available values are "ps2", "ps2ps4us" and "ps2ps4eu"
_NAMESPACE = 'ps2'
_SERVICE_ID = 's:example'


class Event(object):
    def __init__(self, name, character_centric=False, exp_id=None,
                 world_centric=False):
        self.character_centric = character_centric
        self.exp_id = exp_id
        self.fields = {}
        self.world_centric = world_centric
        self.name = name

    def __str__(self):
        return self.name


class Client(object):
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
                # try:
                str = await websocket.recv()
                # Process the response
                await self._process_response(str)

                for item in self._send_queue:
                    await websocket.send(self._send_queue.pop())

                # except:
                #     await self.close()
                #     await self.connect()

    def event(self, func):
        """Decorator used for creating events."""

        self._listeners.append(func)
        return func

    async def _process_response(self, str):
        """Internal. Runs whenever a message is received."""

        response = json.loads(str)
        logger.debug('Processing response: {}'.format(response))

        # Subscription push echo
        if 'subscription' in response:
            logger.info('Subscription: {}'.format(response))
            return

        # Help message
        elif "send this for help" in response:
            logger.info('Help: {}'.format(response))
            return

        # Login service
        elif response['service'] == "push":
            logger.info('Login: {}'.format(response))
            return

        # Event streaming service
        elif response['service'] == 'event':

            # Endpoint state change echo
            if response['type'] == 'serviceStateChanged':
                logger.info('Endpoint: {}'.format(response))
                return

            # Heartbeat
            if response['type'] == 'heartbeat':
                # Process heartbeat information
                log_msg = 'Heartbeat:'
                for endpoint in response['online'].keys():
                    if response['online'][endpoint] == 'true':
                        log_msg += ' {}: online,'.format(endpoint[19:])
                    else:
                        log_msg += ' {}: offline,'.format(endpoint[19:])
                online_endpoints = len(
                    [e for e in response['online'] if response['online'][e] == 'true'])
                logger.info('Heartbeat: Connected to {}/{} event streaming '
                            'endpoints.'.format(online_endpoints, len(response['online'])))
                return

            # Event responses
            if response['type'] == 'serviceMessage':
                listeners_to_run = [l for l in self._listeners if l.__name__ == 'on_{}'.format(
                    response['payload']['event_name'].lower()) or l.__name__ == 'on_event']
                for listener in listeners_to_run:
                    # If is corooutine
                    if asyncio.iscoroutinefunction(listener):
                        await listener(response['payload'])
                    else:
                        listener(response['payload'])
                return

        logger.warning('Ignoring unexpected response: {}'.format(response))

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

        logger.info('Subscribing using: {}'.format(json_data))
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
        logger.info('Clearing all subscriptions...')
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
        logger.info('Unsubscribing using: {}'.format(json_data))
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

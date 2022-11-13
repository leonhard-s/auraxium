"""Tests for the real-time event client module."""

import asyncio
import datetime
import json
import unittest
from typing import Any, Dict, List, Type

# pylint: disable=import-error
import auraxium

from tests.utils import SERVICE_ID


@unittest.skipIf(SERVICE_ID in ['', 's:example'], 'missing service ID')
class EventClientTest(unittest.IsolatedAsyncioTestCase):
    """Live tests for the real-time event client component."""

    client: auraxium.EventClient

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.client = auraxium.EventClient(service_id=SERVICE_ID)

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()
        await self.client.close()

    def test_startup_defensive(self) -> None:
        """Ensure the client does not connect without any triggers."""
        self.assertFalse(self.client.triggers, 'predefined triggers')
        self.assertIsNone(self.client.websocket, 'websocket without triggers')

    async def test_connect_on_trigger(self) -> None:
        """Ensure the client connects as soon as a trigger is added."""
        self.assertFalse(self.client.triggers, 'predefined triggers found')
        self.assertIsNone(self.client.websocket, 'preexisting websocket found')
        # Add trigger and wait for ready
        trigger = auraxium.Trigger(auraxium.event.BattleRankUp)
        self.client.add_trigger(trigger)
        await self.client.wait_ready()
        # Check for websocket activity
        self.assertIsNotNone(self.client.websocket, 'missing websocket')
        self.assertListEqual(
            self.client.triggers, [trigger], 'trigger not found')

    async def test_messages(self) -> None:
        """Test event dispatching."""
        flag = asyncio.Event()

        async def on_death(event: auraxium.event.Event) -> None:
            self.assertIsInstance(event, auraxium.event.Event,
                                  'non-event returned')
            flag.set()

        # pylint: disable=not-callable
        self.client.trigger(auraxium.event.Death)(on_death)
        try:
            await asyncio.wait_for(flag.wait(), 5.0)
        except asyncio.TimeoutError:
            self.skipTest('no game event received after 5 seconds, '
                          'is the game in maintenance?')
        self.assertEqual(len(self.client.triggers), 1)
        self.client.remove_trigger('on_death')
        self.assertEqual(len(self.client.triggers), 0)

    async def test_single_shot(self) -> None:
        """Test a single-shot trigger to ensure it is auto-deleted."""
        trigger = auraxium.Trigger(auraxium.event.Death, single_shot=True)
        flag = asyncio.Event()

        async def wait_for(event: auraxium.event.Event) -> None:
            _ = event
            self.assertGreaterEqual(event.age, 0.0, 'event age is negative')
            flag.set()

        trigger.action = wait_for
        self.client.add_trigger(trigger)
        try:
            await asyncio.wait_for(flag.wait(), 5.0)
        except asyncio.TimeoutError:
            self.skipTest('no game event received after 5 seconds, '
                          'is the game in maintenance?')
        self.assertEqual(len(self.client.triggers), 0)

    async def test_endpoint_status(self) -> None:
        """Test the endpoint status."""
        status = self.client.endpoint_status
        self.assertIsInstance(status, dict)

    async def test_get_trigger(self) -> None:
        """Test the get_trigger method."""
        trigger = auraxium.Trigger(auraxium.event.Death, name='on_death')
        self.client.add_trigger(trigger)
        self.assertEqual(self.client.get_trigger('on_death'), trigger)
        with self.assertRaises(KeyError):
            self.client.get_trigger('on_death2')

    async def test_remove_trigger(self) -> None:
        """Test the remove_trigger method."""
        trigger = auraxium.Trigger(auraxium.event.Death, name='on_death')
        self.client.add_trigger(trigger)
        self.assertEqual(len(self.client.triggers), 1)
        self.client.remove_trigger('on_death')
        self.assertEqual(len(self.client.triggers), 0)
        with self.assertRaises(KeyError):
            self.client.remove_trigger('does_not_exist')

    async def test_trigger_decorator(self) -> None:
        """Test extra overloads of the trigger() decorator helper."""

        def test(_: auraxium.event.Death) -> None:
            pass

        # pylint: disable=not-callable
        self.client.trigger(auraxium.event.Death)(test)
        self.assertEqual(len(self.client.triggers), 1)
        with self.assertRaises(KeyError):
            self.client.trigger(auraxium.event.Death)(test)
        self.assertEqual(len(self.client.triggers), 1)

    async def test_wait_for(self) -> None:
        """Test variations of the wait_for() helper method."""
        trigger = auraxium.Trigger(auraxium.event.Death)

        def do_nothing(_: auraxium.event.Event) -> None:
            pass

        trigger.action = do_nothing

        await self.client.wait_for(trigger, timeout=-1.0)

        with self.assertRaises(TimeoutError):
            await self.client.wait_for(trigger, timeout=0.00001)


class TriggerTest(unittest.TestCase):
    """Test cases for the auraxium.event.Trigger class."""

    time = datetime.datetime.utcnow()

    @classmethod
    def death_evt_factory(cls, attacker: int, victim: int, world: int,
                          is_headshot: bool = False) -> auraxium.event.Death:
        """Create a death event."""
        timestamp: Any = int(cls.time.timestamp())
        return auraxium.event.Death(
            event_name='Death', timestamp=timestamp, world_id=world,
            attacker_character_id=attacker, attacker_fire_mode_id=0,
            attacker_loadout_id=0, attacker_vehicle_id=0, attacker_weapon_id=0,
            character_id=victim, character_loadout_id=0, is_critical=False,
            is_headshot=is_headshot, vehicle_id=0, zone_id=2)

    @staticmethod
    def payload_factory(type_: Type[auraxium.event.Event], *args: Any) -> auraxium.event.Event:
        """Create a payload for the given event type."""
        fields = type_.__fields__
        params: Dict[str, Any] = {
            k: v for k, v in zip(fields, args) if k != 'timestamp'}
        params['timestamp'] = str(int(TriggerTest.time.timestamp()))
        return type_(**params)

    def test_characters_init(self) -> None:
        """Test initializing triggers with a characters filter."""
        trigger = auraxium.Trigger(auraxium.event.Death, characters=[1, 5])
        self.assertListEqual(trigger.characters, [1, 5])

    def test_worlds_init(self) -> None:
        """Test initializing triggers with a worlds filter."""
        trigger = auraxium.Trigger(auraxium.event.Death, worlds=[10, 13])
        self.assertListEqual(trigger.worlds, [10, 13])

    def test_action_via_decorator(self) -> None:
        """Test the Trigger.callback() decorator."""
        trigger = auraxium.Trigger(auraxium.event.Death)

        @trigger.callback
        def do_nothing(_: auraxium.event.Event) -> None:
            pass
        _ = do_nothing

        self.assertIsNone(trigger.action(object()))  # type: ignore

    def test_checks_ok(self) -> None:
        """Correct event, character, and world."""
        trigger = auraxium.Trigger(
            auraxium.event.Death, characters=[5], worlds=[17])
        event = self.death_evt_factory(5, 6, 17)
        self.assertTrue(trigger.check(event))

    def test_checks_wrong_character(self) -> None:
        """Correct event, wrong character target."""
        trigger = auraxium.Trigger(auraxium.event.Death, characters=[1])
        event = self.death_evt_factory(5, 5, 17)
        self.assertFalse(trigger.check(event))

    def test_checks_wrong_world(self) -> None:
        """Correct event, wrong world."""
        trigger = auraxium.Trigger(auraxium.event.Death, worlds=[1])
        event = self.death_evt_factory(1, 2, 10)
        self.assertFalse(trigger.check(event))

    def test_checks_wrong_event(self) -> None:
        """Wrong event type."""
        trigger = auraxium.Trigger(auraxium.event.PlayerLogin)
        event = self.death_evt_factory(1, 2, 3)
        self.assertFalse(trigger.check(event))

    def test_checks_custom_events_ok(self) -> None:
        """Successful filter for a custom GainExperience event."""
        trigger = auraxium.Trigger(
            auraxium.event.GainExperience.filter_experience(15))
        time: Any = int(self.time.timestamp())
        event = auraxium.event.GainExperience(
            event_name='GainExperience', timestamp=time, world_id=1,
            amount=10, character_id=1, experience_id=15, loadout_id=1,
            other_id=0, zone_id=2)
        self.assertTrue(trigger.check(event))

    def test_checks_custom_events_wrong_id(self) -> None:
        """Failed filter for a custom GainExperience event."""
        trigger = auraxium.Trigger(
            auraxium.event.GainExperience.filter_experience(250))
        time: Any = int(self.time.timestamp())
        event = auraxium.event.GainExperience(
            event_name='GainExperience', timestamp=time, world_id=1,
            amount=10, character_id=1, experience_id=15, loadout_id=1,
            other_id=0, zone_id=2)
        self.assertFalse(trigger.check(event))

    def test_custom_condition(self) -> None:
        """Test custom trigger conditions."""
        time: Any = int(self.time.timestamp())
        event = auraxium.event.PlayerLogin(event_name='PlayerLogin',
                                           timestamp=time, world_id=1, character_id=1)

        # Various things to use as conditions
        list_: List[Any] = []

        def callable_false(_: auraxium.event.Event) -> bool:
            return False

        def callable_true(_: auraxium.event.Event) -> bool:
            return True

        # Callable: False
        trigger = auraxium.Trigger(
            auraxium.event.PlayerLogin, conditions=[callable_false])
        self.assertFalse(trigger.check(event))

        # Callable: True
        trigger = auraxium.Trigger(
            auraxium.event.PlayerLogin, conditions=[callable_true])
        self.assertTrue(trigger.check(event))

        # Object: False
        trigger = auraxium.Trigger(
            auraxium.event.PlayerLogin, conditions=[list_])
        self.assertFalse(trigger.check(event))

        # Object: True
        list_.append(1)
        trigger = auraxium.Trigger(
            auraxium.event.PlayerLogin, conditions=[list_])
        self.assertTrue(trigger.check(event))

    def test_subscription_characters(self) -> None:
        """Test the characters list of the subscription generator."""
        trigger = auraxium.Trigger(auraxium.event.Death, characters=[1, 5])
        data = json.loads(trigger.generate_subscription())
        self.assertListEqual(data['characters'], ['1', '5'])

    def test_subscription_worlds(self) -> None:
        """Test the worlds list of the subscription generator."""
        trigger = auraxium.Trigger(auraxium.event.Death, worlds=[10, 13])
        data = json.loads(trigger.generate_subscription())
        self.assertListEqual(data['worlds'], ['10', '13'])

    def test_logical_and(self) -> None:
        """Test the logicalAndCharactersWithWorlds flag is set."""
        trigger = auraxium.Trigger(auraxium.event.Death)
        data = json.loads(trigger.generate_subscription(logical_and=None))
        self.assertNotIn('logicalAndCharactersWithWorlds', data)
        data = json.loads(trigger.generate_subscription(logical_and=True))
        self.assertSequenceEqual(
            data['logicalAndCharactersWithWorlds'], 'true')
        data = json.loads(trigger.generate_subscription(logical_and=False))
        self.assertSequenceEqual(
            data['logicalAndCharactersWithWorlds'], 'false')

"""Tests for the event trigger module."""

import datetime
import json
import unittest
from typing import Any, Dict, List, Type

import auraxium


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
            attacker_team_id=2, character_id=victim, character_loadout_id=0,
            is_critical=False, is_headshot=is_headshot, team_id=1,
            vehicle_id=0, zone_id=2)

    @staticmethod
    def payload_factory(type_: Type[auraxium.event.Event],
                        *args: Any) -> auraxium.event.Event:
        """Create a payload for the given event type."""
        fields = type_.model_fields
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
        event = auraxium.event.PlayerLogin(
            event_name='PlayerLogin', timestamp=time, world_id=1,
            character_id=1)

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

    def test_regression_66_string_event_with_world_filter(self) -> None:
        """https://github.com/leonhard-s/auraxium/issues/66"""
        trigger = auraxium.Trigger('ContinentLock', worlds=[1])
        _ = json.loads(trigger.generate_subscription())

    def test_logical_and_autoselect(self) -> None:
        """Test the auto-insertion of the logicalAnd flag."""
        event_variants = (auraxium.event.Death, "Death",
                          'GainExperience', 'GainExperience_experience_id_1')
        # Character-centric event with no filter -> no logicalAnd
        for event in event_variants:
            trigger = auraxium.Trigger(event)
            data = json.loads(trigger.generate_subscription())
            self.assertNotIn('logicalAndCharactersWithWorlds', data)
        # Character-centric event with world filter -> logicalAnd
        for event in event_variants:
            trigger = auraxium.Trigger(event, worlds=[1])
            data = json.loads(trigger.generate_subscription())
            self.assertSequenceEqual(
                data['logicalAndCharactersWithWorlds'], 'true')
        # Character-centric event with character filter -> no logicalAnd
        for event in event_variants:
            trigger = auraxium.Trigger(event, characters=[1])
            data = json.loads(trigger.generate_subscription())
            self.assertNotIn('logicalAndCharactersWithWorlds', data)

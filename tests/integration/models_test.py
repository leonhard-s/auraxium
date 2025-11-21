"""Test cases for the object representations of PS2 payloads."""

import json
import os
import unittest
from typing import Any, Dict, List, Type

from auraxium.base import Ps2Object
from auraxium.models.base import RESTPayload
from auraxium import ps2
from tests.utils import DATA

PAYLOAD_DIRECTORY = os.path.join(DATA, 'rest')


class TestModels(unittest.TestCase):
    """Test cases for the PS2 object model data classes.

    This test dynamically walks all data in the tests/data/payloads
    directory, determines the associated collection, and attempts to
    instantiate the given pydantic model from it.
    """

    def test_models_datatypes(self) -> None:
        """Try instantiating datatypes from example payloads."""
        directory = os.path.join(PAYLOAD_DIRECTORY, 'datatype_payloads')
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            # Load the payload
            with open(filepath, encoding='utf-8') as payload_file:
                payload: Dict[str, Any] = json.load(payload_file)
            # Extract the collection name
            _ = payload.pop('returned')
            _ = payload.pop('timing', None)
            collection = list(payload.keys())[0][:-5]
            # Find the appropriate class for this collection
            type_: Ps2Object
            cls_: Type[RESTPayload] | None = None
            for name in ps2.__dict__['__all__']:
                type_ = getattr(ps2, name)
                if not hasattr(type_, 'collection'):
                    continue
                if type_.collection == collection:
                    # pylint: disable=protected-access
                    cls_ = type_._model  # type: ignore
            assert cls_ is not None, (
                f'Type for collection "{collection}" not found')
            # Instantiate any payloads found
            for data in payload[f'{collection}_list']:
                instance = cls_(**data)
                self.assertIsInstance(instance, RESTPayload)

    def test_enum_datatypes(self) -> None:
        """Compare the hard-coded enum values to their API counterparts."""
        directory = os.path.join(PAYLOAD_DIRECTORY, 'enum_payloads')
        type_name = 'NULL'

        def get_id(type_: Dict[str, str]) -> int:
            """A helper function to improve test case readability."""
            return int(type_[f'{type_name}_id'])

        # ArmorFacing
        filepath = os.path.join(directory, 'armor_facing.json')
        type_name = 'armor_facing'
        with open(filepath, encoding='utf-8') as payload_file:
            payload: Dict[str, Any] = json.load(payload_file)
        type_list: List[Dict[str, str]] = payload[f'{type_name}_list']
        self.assertEqual(get_id(type_list[0]), ps2.ArmourFacing.FRONT)
        self.assertEqual(get_id(type_list[1]), ps2.ArmourFacing.RIGHT)
        self.assertEqual(get_id(type_list[2]), ps2.ArmourFacing.TOP)
        self.assertEqual(get_id(type_list[3]), ps2.ArmourFacing.REAR)
        self.assertEqual(get_id(type_list[4]), ps2.ArmourFacing.LEFT)
        self.assertEqual(get_id(type_list[5]), ps2.ArmourFacing.BOTTOM)
        self.assertEqual(get_id(type_list[6]), ps2.ArmourFacing.ALL)

        # FireModeType
        filepath = os.path.join(directory, 'fire_mode_type.json')
        type_name = 'fire_mode_type'
        with open(filepath, encoding='utf-8') as payload_file:
            payload: Dict[str, Any] = json.load(payload_file)
        type_list: List[Dict[str, str]] = payload[f'{type_name}_list']
        self.assertEqual(get_id(type_list[0]), ps2.FireModeType.PROJECTILE)
        self.assertEqual(get_id(type_list[1]), ps2.FireModeType.IRON_SIGHT)
        self.assertEqual(get_id(type_list[2]), ps2.FireModeType.MELEE)
        self.assertEqual(get_id(type_list[3]),
                         ps2.FireModeType.TRIGGER_ITEM_ABILITY)
        self.assertEqual(get_id(type_list[4]), ps2.FireModeType.THROWN)

        # MetagameEventState
        filepath = os.path.join(directory, 'metagame_event_state.json')
        type_name = 'metagame_event_state'
        with open(filepath, encoding='utf-8') as payload_file:
            payload: Dict[str, Any] = json.load(payload_file)
        type_list: List[Dict[str, str]] = payload[f'{type_name}_list']
        self.assertEqual(get_id(type_list[0]), ps2.MetagameEventState.STARTED)
        self.assertEqual(get_id(type_list[1]),
                         ps2.MetagameEventState.RESTARTED)
        self.assertEqual(get_id(type_list[2]),
                         ps2.MetagameEventState.CANCELLED)
        self.assertEqual(get_id(type_list[3]), ps2.MetagameEventState.ENDED)
        self.assertEqual(get_id(type_list[4]),
                         ps2.MetagameEventState.XP_BONUS_CHANGED)

        # TargetType
        filepath = os.path.join(directory, 'target_type.json')
        type_name = 'target_type'
        with open(filepath, encoding='utf-8') as payload_file:
            payload: Dict[str, Any] = json.load(payload_file)
        type_list: List[Dict[str, str]] = payload[f'{type_name}_list']
        self.assertEqual(get_id(type_list[0]), ps2.TargetType.SELF)
        self.assertEqual(get_id(type_list[1]), ps2.TargetType.ANY)
        self.assertEqual(get_id(type_list[2]), ps2.TargetType.ENEMY)
        self.assertEqual(get_id(type_list[3]), ps2.TargetType.ALLY)

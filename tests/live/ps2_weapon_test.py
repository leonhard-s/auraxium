"""Test cases for the ps2.Weapon class."""

import unittest

import auraxium
from auraxium import models, ps2

from tests.utils import SERVICE_ID


@unittest.skipIf(SERVICE_ID in ['', 's:example'], 'missing service ID')
class TestWeaponMethods(unittest.IsolatedAsyncioTestCase):
    """Test weapon-specific helper methods for relational tables."""

    client: auraxium.Client
    weapon: ps2.Weapon

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.client = auraxium.Client(service_id=SERVICE_ID, profiling=True)
        weapon = await self.client.get_by_id(ps2.Weapon, 11)
        if weapon is None:
            self.skipTest('Unable to find weapon used for tests')
            return
        self.weapon = weapon

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()
        await self.client.close()

    async def test_is_heat(self) -> None:
        """Test the is_heat_weapon decorator."""
        self.assertFalse(self.weapon.is_heat_weapon)

    async def test_ammo_slots(self) -> None:
        """Test the ammo_slots() helper method."""
        ammo = await self.weapon.ammo_slots()
        self.assertGreater(len(ammo), 0)
        self.assertIsInstance(ammo[0], models.WeaponAmmoSlot)

    async def test_attachments(self) -> None:
        """Test the attachments() helper method."""
        att = await self.weapon.attachments()
        self.assertGreater(len(att), 0)
        self.assertIsInstance(att[0], ps2.Item)

    async def test_datasheet(self) -> None:
        """Test the datasheet() helper method."""
        data = await self.weapon.datasheet()
        if data is None:
            self.fail('Weapon datasheet not found')
        self.assertIsInstance(data, models.WeaponDatasheet)

    async def test_fire_groups(self) -> None:
        """Test the fire_groups() helper method."""
        fire = await self.weapon.fire_groups()
        self.assertGreater(len(fire), 0)
        self.assertIsInstance(fire[0], ps2.FireGroup)

    async def test_item(self) -> None:
        """Test the item() helper method."""
        item = await self.weapon.item()
        if item is None:
            self.fail('Weapon item not found')
        self.assertIsInstance(item, ps2.Item)

"""Test cases for the ps2.Item class."""

import unittest
from typing import List

# pylint: disable=import-error
import auraxium
from auraxium import models, ps2

from tests.utils import SERVICE_ID


@unittest.skipIf(SERVICE_ID in ['', 's:example'], 'missing service ID')
class TestItemMethods(unittest.IsolatedAsyncioTestCase):
    """Test item-specific helper methods for relational tables."""

    client: auraxium.Client
    item: ps2.Item

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.client = auraxium.Client(service_id=SERVICE_ID, profiling=True)
        item = await self.client.get_by_id(ps2.Item, 20)
        if item is None:
            self.skipTest('Unable to find item used for tests')
            return
        self.item = item

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()
        await self.client.close()

    async def test_attachments(self) -> None:
        """Test the attachments() helper method."""
        att: List[ps2.Item] = await self.item.attachments()  # type: ignore
        self.assertGreater(len(att), 0)
        self.assertIsInstance(att[0], ps2.Item)

    async def test_category(self) -> None:
        """Test the category() helper method."""
        cat = await self.item.category()
        if cat is None:
            self.fail('Item category not found')
        self.assertIsInstance(cat, ps2.ItemCategory)
        self.assertEqual(cat.name.en, 'Assault Rifle')

    async def test_faction(self) -> None:
        """Test the faction() helper method."""
        fac = await self.item.faction()
        if fac is None:
            self.fail('Item faction not found')
        self.assertIsInstance(fac, ps2.Faction)
        self.assertEqual(fac.id, 1)

    async def test_datasheet(self) -> None:
        """Test the datasheet() helper method."""
        data = await self.item.datasheet()
        if data is None:
            self.fail('Item datasheet not found')
        self.assertIsInstance(data, models.WeaponDatasheet)
        self.assertEqual(data.item_id, self.item.id)

    async def test_profiles(self) -> None:
        """Test the profiles() helper method."""
        profiles: List[ps2.Profile] = await self.item.profiles()  # type: ignore
        self.assertGreater(len(profiles), 0)
        self.assertIsInstance(profiles[0], ps2.Profile)

    async def test_type(self) -> None:
        """Test the type() helper method."""
        typ = await self.item.type()
        if typ is None:
            self.fail('Item type not found')
        self.assertIsInstance(typ, ps2.ItemType)
        self.assertEqual(typ.code, 'Weapon')

    async def test_weapon(self) -> None:
        """Test the weapon() helper method."""
        weapon = await self.item.weapon()
        if weapon is None:
            self.fail('Item weapon not found')
        self.assertIsInstance(weapon, ps2.Weapon)
        self.assertEqual(weapon.id, 11)

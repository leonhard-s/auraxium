"""Unit tests for the main REST client.

Some tests will be skipped if the SERVICE_ID environment variable has
not been set.
"""

import unittest

import auraxium
from auraxium.ps2 import Achievement, Character, Loadout, World, Zone

from tests.utils import SERVICE_ID


@unittest.skipIf(SERVICE_ID in ['', 's:example'], 'missing service ID')
class TestRestClient(unittest.IsolatedAsyncioTestCase):
    """Test the getX helper methods from the main REST client."""

    client: auraxium.Client

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.client = auraxium.Client(service_id=SERVICE_ID, profiling=True)

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()
        await self.client.close()

    async def test_count(self) -> None:
        """Test the count() helper method."""
        count = await self.client.count(Character, name__first='Auroram')
        self.assertEqual(count, 1)
        count = await self.client.count(Character, name__first_lower='*auro')
        self.assertGreater(count, 1)

    async def test_find(self) -> None:
        """Test test find() helper method."""
        results = await self.client.find(Zone, results=2)
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Zone)
        results = await self.client.find(Zone, results=3, offset=1)
        self.assertEqual(len(results), 3)

    async def test_get(self) -> None:
        """Test generic get() helper method."""
        achievement = await self.client.get(Achievement, item_id=20)
        if achievement is None:
            self.fail('Achievement not found')
        self.assertIsInstance(achievement, Achievement)
        self.assertEqual(achievement.item_id, 20)
        # Warn if extra results are returned due to multiple ids
        with self.assertWarns(UserWarning):
            await self.client.get(Achievement, achievement_id='1,2')
        # Test missing object returning None
        doesnt_exist = await self.client.get(Character, character_id=1)
        self.assertIsNone(doesnt_exist)

    async def test_get_by_id(self) -> None:
        """Test retrieving API entities by ID."""
        char = await self.client.get_by_id(Character, 5428072203494645969)
        if char is None:
            self.fail('Character not found')
        self.assertIsInstance(char, Character)
        self.assertEqual(char.id, 5428072203494645969)
        self.assertEqual(str(char.name), 'Auroram')
        # Test missing object returning None
        doesnt_exist = await self.client.get_by_id(Character, 1)
        self.assertIsNone(doesnt_exist)
        # Test fallback hooks using missing data (e.g. NSO medic)
        loadout = await self.client.get_by_id(Loadout, 30)
        if loadout is None:
            self.fail('Loadout not found')
        self.assertIsInstance(loadout, Loadout)
        self.assertEqual(loadout.id, 30)
        self.assertEqual(loadout.code_name, 'NSO Medic')
        # Test missing object for type with fallback hook
        loadout = await self.client.get_by_id(Loadout, 5000)
        self.assertIsNone(loadout)

    async def test_get_by_name(self) -> None:
        """Test retrieving API entities by name."""
        # First lookup: cache miss
        zone = await self.client.get_by_name(Zone, 'Indar', locale='en')
        if zone is None:
            self.fail('Zone not found')
        self.assertIsInstance(zone, Zone)
        # Second lookup: cache hit
        zone = await self.client.get_by_name(Zone, 'Indar', locale='en')
        if zone is None:
            self.fail('Zone not found')
        self.assertIsInstance(zone, Zone)
        # Third lookup: cache miss (locale changed)
        zone = await self.client.get_by_name(Zone, 'Indar', locale='fr')
        if zone is None:
            self.fail('Zone not found')
        self.assertIsInstance(zone, Zone)
        # Special character fields
        char = await self.client.get_by_name(Character, 'Auroram')
        if char is None:
            self.fail('Character not found')
        self.assertIsInstance(char, Character)
        world = await self.client.get_by_name(World, 'Wainwright')
        if world is None:
            self.fail('World not found')
        self.assertIsInstance(world, World)

    async def test_context_manager(self) -> None:
        """Test the __aenter__ and __aexit__ interfaces."""
        async with self.client as client:
            self.assertIsInstance(client, auraxium.Client)
            self.assertIs(client, self.client)
            self.assertFalse(client.session.closed)
        self.assertTrue(client.session.closed)

    async def test_latency(self) -> None:
        """Test the latency() helper method."""
        # Initially less than 0
        latency = self.client.latency
        self.assertLess(latency, 0)
        # After a call, it should be greater than 0
        await self.client.get(Character)
        latency = self.client.latency
        self.assertGreater(latency, 0)

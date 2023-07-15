"""Test cases for ps2.leaderboard query functions."""

import unittest

import auraxium
from auraxium import ps2

from tests.utils import SERVICE_ID


@unittest.skipIf(SERVICE_ID in ['', 's:example'], 'missing service ID')
class TestLeaderboard(unittest.IsolatedAsyncioTestCase):
    """Test the leaderboard query methods."""

    client: auraxium.Client

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.client = auraxium.Client(service_id=SERVICE_ID, profiling=True)

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()
        await self.client.close()

    async def test_by_char(self) -> None:
        """Test the by_char() query."""
        # Retrieve a character with very low login count that is unlikely to be
        # leading the leaderboard.
        char = await self.client.get(ps2.Character, times__login_count='<50')
        if char is None:
            self.skipTest('Unable to find low-playtime character for tests')
            return
        result = await ps2.leaderboard.by_char(
            ps2.leaderboard.Stat.KILLS, char, client=self.client)
        self.assertIsNone(result)
        # Retrieve a character with high playtime that is on the leaderboard
        char_id = 5428072203494645969
        result = await ps2.leaderboard.by_char(
            ps2.leaderboard.Stat.KILLS, char_id, client=self.client)
        if result is None:
            self.skipTest('Leaderboard endpoints are down')
            return
        rank, value = result
        self.assertIsInstance(rank, int)
        self.assertIsInstance(value, int)

    async def test_by_char_multi(self) -> None:
        """Test the by_char_multi() query."""
        char_id = 5428072203494645969
        result = await ps2.leaderboard.by_char_multi(
            ps2.leaderboard.Stat.KILLS, char_id, client=self.client)
        if not result:
            self.skipTest('Leaderboard endpoints are down')
            return
        rank, value = result[0]
        self.assertIsInstance(rank, int)
        self.assertIsInstance(value, int)

    async def test_top(self) -> None:
        """Test the top() query."""
        results = await ps2.leaderboard.top(
            ps2.leaderboard.Stat.KILLS, world=13, client=self.client)
        if not results:
            self.skipTest('Leaderboard endpoints are down')
            return
        self.assertGreater(len(results), 0)
        value, character = results[0]
        self.assertIsInstance(value, int)
        self.assertIsInstance(character, ps2.Character)

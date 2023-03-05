"""Test cases for the ps2.Character class."""

import unittest
from typing import List, cast

# pylint: disable=import-error
import auraxium
from auraxium import models, ps2

from tests.utils import SERVICE_ID


@unittest.skipIf(SERVICE_ID in ['', 's:example'], 'missing service ID')
class TestCharacterMethods(unittest.IsolatedAsyncioTestCase):
    """Test character-specific helper methods for relational tables."""

    client: auraxium.Client
    character: ps2.Character

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.client = auraxium.Client(service_id=SERVICE_ID, profiling=True)
        char = await self.client.get_by_id(ps2.Character, 5428072203494645969)
        if char is None:
            self.skipTest('Unable to find character used for tests')
        self.character = cast(ps2.Character, char)

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()
        await self.client.close()

    async def test_achievements(self) -> None:
        """Test the achievements() helper method."""
        achievements = await self.character.achievements()
        self.assertGreater(len(achievements), 0)
        self.assertIsInstance(achievements[0], models.CharacterAchievement)

    async def test_currency(self) -> None:
        """Test the currency() helper method."""
        nanites, asp_tokens = await self.character.currency()
        self.assertIsInstance(nanites, int)
        self.assertIsInstance(asp_tokens, int)

    async def test_directive(self) -> None:
        """Test the directive() helper method."""
        directives = await self.character.directive()
        self.assertGreater(len(directives), 0)
        self.assertIsInstance(directives[0], models.CharacterDirective)

    async def test_directive_objective(self) -> None:
        """Test the directive_objective() helper method."""
        results = await self.character.directive_objective()
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], models.CharacterDirectiveObjective)

    async def test_directive_tier(self) -> None:
        """Test the directive_tier() helper method."""
        results = await self.character.directive_tier()
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], models.CharacterDirectiveTier)

    async def test_directive_tree(self) -> None:
        """Test the directive_tree() helper method."""
        results = await self.character.directive_tree()
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], models.CharacterDirectiveTree)

    async def test_events(self) -> None:
        """Test the events() helper method."""
        events = await self.character.events()
        self.assertGreater(len(events), 0)
        self.assertIsInstance(events[0], dict)

    async def test_events_grouped(self) -> None:
        """Test the events_grouped() helper method."""
        events = await self.character.events_grouped()
        self.assertGreater(len(events), 0)
        self.assertIsInstance(events[0], dict)

    async def test_faction(self) -> None:
        """Test the faction() helper method."""
        faction = await self.character.faction()
        if faction is None:
            self.fail('Unable to get character faction')
        self.assertIsInstance(faction, ps2.Faction)
        self.assertEqual(faction.id, 1)

    async def test_friends(self) -> None:
        """Test the friends() helper method."""
        friends = await self.character.friends()
        self.assertGreater(len(friends), 0)  # Bold assumption!
        self.assertIsInstance(friends[0], ps2.Character)

    async def test_items(self) -> None:
        """Test the items() helper method."""
        items: List[ps2.Item] = await self.character.items(10)  # type: ignore
        self.assertGreater(len(items), 0)
        self.assertIsInstance(items[0], ps2.Item)

    async def test_is_online(self) -> None:
        """Test the is_online() helper method."""
        self.assertIsInstance(await self.character.is_online(), bool)

    async def test_name_long(self) -> None:
        """Test the name_long() helper method."""
        full_name = await self.character.name_long()
        self.assertIsInstance(full_name, str)
        # Title might change
        *_, name = full_name.split(' ')
        self.assertEqual(name, 'Auroram')

    async def test_online_status(self) -> None:
        """Test the online_status() helper method."""
        expected = 13 if await self.character.is_online() else 0
        self.assertEqual(await self.character.online_status(), expected)

    async def test_outfit(self) -> None:
        """Test the outfit() helper method."""
        outfit = await self.character.outfit()
        if outfit is not None:
            self.assertIsInstance(outfit, ps2.Outfit)

    async def test_outfit_member(self) -> None:
        """Test the outfit_member() helper method."""
        outfit_member = await self.character.outfit_member()
        if outfit_member is not None:
            self.assertIsInstance(outfit_member, ps2.OutfitMember)
            self.assertEqual(outfit_member.id, self.character.id)

    async def test_profile(self) -> None:
        """Test the profile() helper method."""
        profile = await self.character.profile()
        self.assertIsInstance(profile, ps2.Profile)

    async def test_misc_getters(self) -> None:
        """Test dynamic getters for misc data."""
        names = ['skill', 'stat', 'stat_by_faction', 'stat_history',
                 'weapon_stat', 'weapon_stat_by_faction']
        for name in names:
            data = await getattr(self.character, name)()
            self.assertGreater(len(data), 0)
            self.assertIsInstance(data[0], dict)

    async def test_title(self) -> None:
        """Test the title() helper method."""
        title = await self.character.title()
        if title is not None:
            self.assertIsInstance(title, ps2.Title)
            name = await self.character.name_long()
            self.assertEqual(name, f'{title.name} {self.character.name}')

    async def test_world(self) -> None:
        """Test the world() helper method."""
        world = await self.character.world()
        if world is None:
            self.fail('Unable to get character world')
        self.assertIsInstance(world, ps2.World)
        self.assertEqual(world.id, 13)

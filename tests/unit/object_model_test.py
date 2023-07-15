"""Unit tests for basic object model functionality and validation."""

import typing
import unittest

import auraxium
from auraxium import census, endpoints
from auraxium._cache import TLRUCache
from auraxium.errors import PayloadError
from auraxium.ps2 import DirectiveTreeCategory, Item, Loadout
from auraxium.types import LocaleData


class TestPs2Object(unittest.TestCase):
    """Test cases for the main PS2Object base class."""

    def setUp(self) -> None:

        class Dummy:
            """Stand-in for a Client, not worth building a real mock for."""
            service_id = 's:example'
            endpoint = endpoints.DBG_CENSUS

        self.client = typing.cast(auraxium.Client, Dummy())

    def test_validation(self) -> None:
        """Test the validation hooks applying properly.

        This only tests one class, proper tests are performed for each
        object type as part of the ``models_test`` file.
        """
        valid = Loadout({
            'loadout_id': '1', 'profile_id': '2', 'faction_id': '3',
            'code_name': 'Test'}, client=self.client)
        self.assertTrue(valid.id == 1)
        self.assertTrue(valid.profile_id == 2)
        self.assertTrue(valid.faction_id == 3)
        self.assertTrue(valid.code_name == 'Test')

        # No colletion ID field present
        with self.assertRaises(PayloadError):
            Loadout({'wrong_id': '1'}, client=self.client)
        # Required fields missing
        with self.assertRaises(PayloadError):
            Loadout({'loadout_id': '1', 'other keys': 'are missing'},
                    client=self.client)

    def test_dunder_eq(self) -> None:
        """Test the __eq__ dunder method for Ps2Object subclasses."""
        # Loadout 1 (valid)
        loadout_1 = Loadout({
            'loadout_id': '1', 'profile_id': '2', 'faction_id': '3',
            'code_name': 'Test'}, client=self.client)
        # Loadout 1 again (valid)
        loadout_2 = Loadout({
            'loadout_id': '1', 'profile_id': '2', 'faction_id': '3',
            'code_name': 'Test'}, client=self.client)
        # Loadout 2 (valid)
        loadout_3 = Loadout({
            'loadout_id': '2', 'profile_id': '4', 'faction_id': '8',
            'code_name': 'Different'}, client=self.client)
        # Directive category (not a loadout)
        names = {s: 'Test' for s in LocaleData.model_fields}
        cat = DirectiveTreeCategory(
            {'directive_tree_category_id': '1', 'name': names},
            client=self.client)

        # Identical instances
        self.assertTrue(loadout_1 == loadout_2)
        # Different instances
        self.assertFalse(loadout_1 == loadout_3)
        # Different class
        self.assertFalse(loadout_1 == cat)

    def test_dunder_repr(self) -> None:
        """Test the __repr__ dunder method."""
        loadout = Loadout({
            'loadout_id': '1', 'profile_id': '2', 'faction_id': '3',
            'code_name': 'Test'}, client=self.client)
        self.assertSequenceEqual(repr(loadout), '<Loadout:1>')

    def test_dunder_hash(self) -> None:
        """Test the __hash__ dunder method."""
        loadout_1 = Loadout({
            'loadout_id': '1', 'profile_id': '2', 'faction_id': '3',
            'code_name': 'Test'}, client=self.client)
        loadout_3 = Loadout({
            'loadout_id': '1', 'profile_id': '2', 'faction_id': '3',
            'code_name': 'Test'}, client=self.client)
        self.assertIsInstance(hash(loadout_1), int)
        self.assertEqual(hash(loadout_1), hash(loadout_3))

    def test_attribute_error(self) -> None:
        """Ensure not all AttributeErrors are consumed by ``.data``."""
        loadout = Loadout({
            'loadout_id': '1', 'profile_id': '2', 'faction_id': '3',
            'code_name': 'Test'}, client=self.client)
        with self.assertRaises(AttributeError):
            _ = loadout.not_a_real_attribute

    def test_query_factory(self) -> None:
        """Make sure generated queries match the object parameters."""
        loadout = Loadout({
            'loadout_id': '12', 'profile_id': '2', 'faction_id': '3',
            'code_name': 'Test'}, client=self.client)
        ref = census.Query('loadout', 'ps2:v2', loadout_id=12)
        self.assertEqual(loadout.query().url(), ref.url())


class TestCachedObject(unittest.TestCase):
    """Test cache modification hooks for cacheable types."""

    def test_alter_cache(self) -> None:
        """Test modification of the underlying cache."""
        cache: TLRUCache[int, Loadout] = getattr(Loadout, '_cache')
        Loadout.alter_cache(5, 15.0)
        self.assertEqual(cache.size, 5)
        self.assertEqual(cache.ttu, 15.0)
        with self.assertRaises(ValueError):
            Loadout.alter_cache(0)


class TestNamedObject(unittest.TestCase):
    """Test caching behaviour for named, cacheable objets."""

    def setUp(self) -> None:

        class Dummy:
            """Stand-in for a Client, not worth building a real mock for."""
            service_id = 's:example'

        self.client = typing.cast(auraxium.Client, Dummy())

    def test_dunder_repr(self) -> None:
        """Test the __repr__ dunder method."""
        names = {s: f'Test_{s}' for s in LocaleData.model_fields}
        cat = DirectiveTreeCategory(
            {'directive_tree_category_id': '12', 'name': names},
            client=self.client)
        self.assertSequenceEqual(
            repr(cat), '<DirectiveTreeCategory:12:\'Test_en\'>')

    def test_dunder_str(self) -> None:
        """Test the __str__ dunder method."""
        names = {s: f'Test_{s}' for s in LocaleData.model_fields}
        cat = DirectiveTreeCategory(
            {'directive_tree_category_id': '12', 'name': names},
            client=self.client)
        self.assertSequenceEqual(str(cat), 'Test_en')


class TestImageMixin(unittest.TestCase):
    """Test the ImageMixin helper class interface."""

    def setUp(self) -> None:

        class Dummy:
            """Stand-in for a Client, not worth building a real mock for."""
            service_id = 's:example'

        self.client = typing.cast(auraxium.Client, Dummy())

    def test_image(self) -> None:
        """Test the image() method."""
        names = {s: f'Test_{s}' for s in LocaleData.model_fields}
        item = Item(
            {'item_id': '1', 'is_vehicle_weapon': '0', 'max_stack_size': '1',
             'name': names, 'is_default_attachment': '0', 'image_id': '123'},
            client=self.client)
        self.assertEqual(item.image(),
                         'https://census.daybreakgames.com/files/'
                         'ps2/images/static/123.png')

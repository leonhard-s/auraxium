"""Unit tests for the auraxium.census sub module.

These tests focus on URL parsing and argument handling. No queries are
to be performed as part of this module.
"""

import unittest
from auraxium import census


class TestURLs(unittest.TestCase):
    """Test cases for basic URL generation."""

    def test_empty_query(self) -> None:
        """Test an empty query using all default values."""
        url = census.Query().url()
        self.assertMultiLineEqual(
            str(url.origin()), 'https://census.daybreakgames.com',
            'Unexpected census endpoint')
        parts = url.parts[1:]  # Remove leading '/'
        self.assertEqual(
            len(parts), 3,
            f'Expected 3 URL components, got {len(parts)}')
        self.assertMultiLineEqual(
            parts[0], 's:example', 'Unexpected service ID')
        self.assertMultiLineEqual(
            parts[1], 'get', 'Unexpected query verb')
        self.assertMultiLineEqual(
            parts[2], 'ps2:v2', 'Unexpected default namespace')

    def test_simple_query(self) -> None:
        """Generate a simple query for a non-standard namespace."""
        url = census.Query('character', namespace='eq2').url()
        parts = url.parts[1:]  # Remove leading '/'
        self.assertEqual(
            len(parts), 4,
            f'Expected 4 URL components, got {len(parts)}')
        self.assertMultiLineEqual(
            parts[0], 's:example',
            'Unexpected service ID')
        self.assertMultiLineEqual(
            parts[1], 'get',
            'Unexpected query verb')
        self.assertMultiLineEqual(
            parts[2], 'eq2',
            'Unexpected namespace/game')
        self.assertMultiLineEqual(
            parts[3], 'character',
            'Unexpected collection')

    def test_count_query(self) -> None:
        """Generate a simple query using the 'count' query verb."""
        url = census.Query('faction').url(verb='count')
        parts = url.parts[1:]  # Remove leading '/'
        self.assertEqual(
            len(parts), 4,
            f'Expected 4 URL components, got {len(parts)}')
        self.assertMultiLineEqual(
            parts[0], 's:example',
            'Unexpected service ID')
        self.assertMultiLineEqual(
            parts[1], 'count',
            'Unexpected query verb')
        self.assertMultiLineEqual(
            parts[2], 'ps2:v2',
            'Unexpected namespace/game')
        self.assertMultiLineEqual(
            parts[3], 'faction',
            'Unexpected collection')

    def test_term_single(self) -> None:
        """Generate a query using a single, manually added term."""
        url = census.Query('item').add_term('name.en', 'Force-Blade').url()
        parts = url.parts[1:]  # Remove leading '/'
        self.assertMultiLineEqual(
            parts[0], 's:example',
            'Unexpected service ID')
        self.assertMultiLineEqual(
            parts[1], 'get',
            'Unexpected query verb')
        self.assertMultiLineEqual(
            parts[2], 'ps2:v2',
            'Unexpected namespace/game')
        self.assertMultiLineEqual(
            parts[3], 'item',
            'Unexpected collection')
        self.assertDictEqual(
            dict(url.query), {'name.en': 'Force-Blade'},
            'Incorrect query string')

    def test_term_implicit(self) -> None:
        """Generate a query using a single, implicitly added term."""
        url = census.Query('vehicle', name__fr='Offenseur').url()
        parts = url.parts[1:]  # Remove leading '/'
        self.assertMultiLineEqual(
            parts[0], 's:example',
            'Unexpected service ID')
        self.assertMultiLineEqual(
            parts[1], 'get',
            'Unexpected query verb')
        self.assertMultiLineEqual(
            parts[2], 'ps2:v2',
            'Unexpected namespace/game')
        self.assertMultiLineEqual(
            parts[3], 'vehicle',
            'Unexpected collection')
        self.assertDictEqual(
            dict(url.query), {'name.fr': 'Offenseur'},
            'Incorrect query string')

    def test_term_multi(self) -> None:
        """Generate a query using multiple query terms."""
        query = census.Query('character').add_term('battle_rank.value', 1)
        url = query.add_term('prestige_rank', 1).url()
        parts = url.parts[1:]  # Remove leading '/'
        self.assertMultiLineEqual(
            parts[0], 's:example',
            'Unexpected service ID')
        self.assertMultiLineEqual(
            parts[1], 'get',
            'Unexpected query verb')
        self.assertMultiLineEqual(
            parts[2], 'ps2:v2',
            'Unexpected namespace/game')
        self.assertMultiLineEqual(
            parts[3], 'character',
            'Unexpected collection')
        self.assertDictEqual(
            dict(url.query), {'battle_rank.value': '1', 'prestige_rank': '1'},
            'Incorrect query string')

    def test_search_modifiers(self) -> None:
        """Generate a query using each of the search modifiers."""
        # NOTE: This check does intentionally not use sensible field names.
        # It only cares about whether the search modifier literals are
        # added correctly.
        modifiers = ['', '<', '[', '>', ']',  '^', '*', '!']
        for index, prefix in enumerate(modifiers):
            query = census.Query('dummy')
            mod = census.SearchModifier(index)
            url = query.add_term('field', 'value', modifier=mod).url()
            self.assertDictEqual(
                dict(url.query), {'field': f'{prefix}value'},
                f'Incorrect search modifier prefix; expected {prefix}')


class TestQueryCommands(unittest.TestCase):
    """Tests for the generation of query commands."""

    def test_qc_only(self) -> None:
        """Generate a query that uses a query command, but no terms."""
        url = census.Query('ability').set_distinct('ability_type_id').url()
        self.assertDictEqual(
            dict(url.query), {'c:distinct': 'ability_type_id'},
            'Incorrect query string')

    def test_qc_multi(self) -> None:
        """Generate a query using multiple query commands."""
        url = census.Query('vehicle').set_limit(10).set_start(20).url()
        self.assertDictEqual(
            dict(url.query), {'c:limit': '10', 'c:start': '20'},
            'Incorrect query string')

    def test_qc_mixed(self) -> None:
        """Generate a query using query commands and terms."""
        url = census.Query('item', faction=1).set_limit(100).url()
        self.assertDictEqual(
            dict(url.query), {'faction': '1', 'c:limit': '100'},
            'Incorrect query string')

    def test_show(self) -> None:
        """Test the c:show query command."""
        query = census.Query('character')
        url = query.set_show_fields('name.first', 'battle_rank.value').url()
        self.assertDictEqual(
            dict(url.query), {'c:show': 'name.first,battle_rank.value'},
            'Incorrect query command: c:show')

    def test_hide(self) -> None:
        """Test the c:hide query command."""
        query = census.Query('character')
        url = query.set_hide_fields('name.first_lower').url()
        self.assertDictEqual(
            dict(url.query), {'c:hide': 'name.first_lower'},
            'Incorrect query command: c:hide')

    def test_sort(self) -> None:
        """Test the c:sort query command."""
        query = census.Query('item')
        url = query.sort('faction_id', ('item_id', False)).url()
        self.assertDictEqual(
            dict(url.query), {'c:sort': 'faction_id,item_id:-1'},
            'Incorrect query command: c:sort')

    def test_has(self) -> None:
        """Test the c:has query command."""
        query = census.Query('weapon')
        url = query.require_fields('heat_capacity').url()
        self.assertDictEqual(
            dict(url.query), {'c:has': 'heat_capacity'},
            'Incorrect query command: c:has')

    def test_resolve(self) -> None:
        """Test the c:resolve query command."""
        query = census.Query('character')
        url = query.set_resolves('online_status').url()
        self.assertDictEqual(
            dict(url.query), {'c:resolve': 'online_status'},
            'Incorrect query command: c:resolve')

    def test_case(self) -> None:
        """Test the c:case query command."""
        query = census.Query('item')
        query.add_term('name.en', 'Pulsar',
                       modifier=census.SearchModifier.CONTAINS)
        url = query.case_insensitive(True).url()
        self.assertDictEqual(
            dict(url.query), {'name.en': '*Pulsar', 'c:case': '0'},
            'Incorrect query command: c:case')

    def test_limit(self) -> None:
        """Test the c:limit query command."""
        query = census.Query('faction')
        url = query.set_limit(5).url()
        self.assertDictEqual(
            dict(url.query), {'c:limit': '5'},
            'Incorrect query command: c:limit')

    def test_limit_per_db(self) -> None:
        """Test the c:limit_per_db query command."""
        query = census.Query('character')
        url = query.set_limit_per_db(20).url()
        self.assertDictEqual(
            dict(url.query), {'c:limitPerDB': '20'},
            'Incorrect query command: c:limitPerDB')

    def test_start(self) -> None:
        """Test the c:start query command."""
        query = census.Query('weapon')
        url = query.sort('weapon_id').set_start(20).url()
        self.assertDictEqual(
            dict(url.query), {'c:sort': 'weapon_id', 'c:start': '20'},
            'Incorrect query command: c:start')

    def test_include_null(self) -> None:
        """Test the c:includeNull query command."""
        query = census.Query('weapon')
        url = query.set_include_null(True).url()
        self.assertDictEqual(
            dict(url.query), {'c:includeNull': '1'},
            'Incorrect query command: c:includeNull')

    def test_lang(self) -> None:
        """Test the c:lang query command."""
        query = census.Query('item')
        url = query.set_locale('en').url()
        self.assertDictEqual(
            dict(url.query), {'c:lang': 'en'},
            'Incorrect query command: c:lang')

    def test_join(self) -> None:
        """Test the c:join query command."""
        query = census.Query('character')
        query.create_join('characters_world')
        url = query.url()
        self.assertDictEqual(
            dict(url.query), {'c:join': 'characters_world'},
            'Incorrect query command: c:join')

    def test_tree(self) -> None:
        """Test the c:tree query command."""
        query = census.Query('vehicle').set_limit(40)
        url = query.as_tree('type_id', True, 'type_').url()
        self.assertIn('c:tree', dict(url.query),
                      'Missing query key: c:tree')
        tree_pairs = url.query['c:tree'].split('^')
        tree_dict = {}
        for pair in tree_pairs:
            try:
                key, value = pair.split(':')
            except ValueError:
                key = 'field'
                value = pair
            tree_dict[key] = value
        self.assertDictEqual(
            tree_dict, {'field': 'type_id', 'prefix': 'type_', 'list': '1'},
            'Invalid key/value pairs for query command: c:tree')

    def test_timing(self) -> None:
        """Test the c:timing query command."""
        url = census.Query('character').profile(True).url()
        self.assertDictEqual(
            dict(url.query), {'c:timing': '1'},
            'Incorrect query command: c:timing')

    def test_exact_match_first(self) -> None:
        """Test the c:exactMatchFirst query command."""
        url = census.Query('character').promote_exact_matches(True).url()
        self.assertDictEqual(
            dict(url.query), {'c:exactMatchFirst': '1'},
            'Incorrect query command: c:exactMatchFirst')

    def test_distinct(self) -> None:
        """Test the c:distinct query command."""
        url = census.Query('effect').set_distinct('effect_type_id').url()
        self.assertDictEqual(
            dict(url.query), {'c:distinct': 'effect_type_id'},
            'Incorrect query command: c:distinct')

    def test_retry(self) -> None:
        """Test the c:retry query command."""
        url = census.Query('character').set_retry(False).url()
        self.assertDictEqual(
            dict(url.query), {'c:retry': '0'},
            'Incorrect query command: c:retry')

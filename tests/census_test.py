"""Unit tests for the auraxium.census sub module.

These tests focus on URL parsing and argument handling. No queries are
to be performed as part of this module.
"""

import unittest
import warnings
from typing import List

import yarl

from auraxium import census  # pylint: disable=import-error

ENDPOINT = 'https://census.daybreakgames.com/'


class TestQueryBaseInterface(unittest.TestCase):
    """Test the class interface of the QueryBase class."""

    def test_add_join(self) -> None:
        """Test QueryBase.add_join()"""
        query = census.QueryBase('collection')
        join = census.JoinedQuery('join')
        query.add_join(join)
        # The joins cannot be compared directly as the add_join method creates
        # a copy of the join.
        self.assertDictEqual(query.joins[0].__dict__, join.__dict__)

    def test_add_term(self) -> None:
        """Test QueryBase.add_term()"""
        query = census.QueryBase()
        query.add_term('field', 'value')
        term = query.data.terms[0]
        self.assertEqual(term.field, 'field')
        self.assertEqual(term.value, 'value')
        self.assertEqual(term.modifier, census.SearchModifier.EQUAL_TO)

    def test_copy(self) -> None:
        """Test QueryBase.copy()"""
        template = census.Query('collection')
        join = template.create_join('join')
        clone = census.QueryBase.copy(template, copy_joins=True)
        self.assertListEqual(clone.joins, [join])

    def test_create_join(self) -> None:
        """Test QueryBase.create_join()"""
        query = census.QueryBase('collection')
        join = query.create_join('join')
        self.assertListEqual(query.joins, [join])

    def test_hide(self) -> None:
        """Test QueryBase.hide()"""
        query = census.QueryBase('collection')
        self.assertListEqual(query.data.hide, [])
        query.hide('one', 'two')
        self.assertListEqual(query.data.hide, ['one', 'two'])

    def test_show(self) -> None:
        """Test QueryBase.show()"""
        query = census.QueryBase('collection')
        self.assertListEqual(query.data.show, [])
        query.show('one', 'two')
        self.assertListEqual(query.data.show, ['one', 'two'])


class TestQueryInterface(unittest.TestCase):
    """Test the class Interface of the Query class."""

    def test_str(self) -> None:
        """Test Query.__str__()"""
        query = census.Query('collection')
        valid = f'{ENDPOINT}s:example/get/ps2:v2/collection'
        self.assertEqual(str(query), valid)

    def test_copy(self) -> None:
        """Test Query.copy()"""
        template_join = census.JoinedQuery('join')
        template_join_list = census.JoinedQuery('join').set_list(True)
        template_query = census.Query('collection')
        # Query from query
        copy_query = census.Query.copy(template_query)
        self.assertEqual(copy_query.data, template_query.data)
        # Query from non-list join
        copy_join = census.Query.copy(template_join)
        self.assertEqual(
            copy_join.data.collection, template_join.data.collection)
        self.assertEqual(copy_join.data.hide, template_join.data.hide)
        self.assertEqual(copy_join.data.show, template_join.data.show)
        self.assertEqual(copy_join.data.terms, template_join.data.terms)
        # Query from list join
        copy_join_list = census.Query.copy(template_join_list)
        self.assertEqual(
            copy_join_list.data.collection, template_join.data.collection)
        self.assertEqual(copy_join_list.data.hide, template_join.data.hide)
        self.assertEqual(copy_join_list.data.show, template_join.data.show)
        self.assertEqual(copy_join_list.data.terms, template_join.data.terms)
        self.assertNotEqual(copy_join_list.data.limit, 1)

    def test_has(self) -> None:
        """Test Query.has()"""
        query = census.Query('collection')
        self.assertListEqual(query.data.has, [])
        query.has('field')
        self.assertListEqual(query.data.has, ['field'])

    def test_distinct(self) -> None:
        """Test Query.distinct()"""
        query = census.Query('collection')
        self.assertEqual(query.data.distinct, None)
        query.distinct('field')
        self.assertEqual(query.data.distinct, 'field')

    def test_exact_match_first(self) -> None:
        """Test Query.exact_match_first()"""
        query = census.Query()
        self.assertEqual(query.data.exact_match_first, False)
        query.exact_match_first(True)
        self.assertEqual(query.data.exact_match_first, True)
        query.exact_match_first(False)
        self.assertEqual(query.data.exact_match_first, False)

    def test_include_null(self) -> None:
        """Test Query.include_null()"""
        query = census.Query()
        self.assertEqual(query.data.include_null, False)
        query.include_null(True)
        self.assertEqual(query.data.include_null, True)
        query.include_null(False)
        self.assertEqual(query.data.include_null, False)

    def test_lang(self) -> None:
        """Test Query.lang()"""
        query = census.Query()
        self.assertEqual(query.data.lang, None)
        query.lang('en')
        self.assertEqual(query.data.lang, 'en')
        query.lang(None)
        self.assertEqual(query.data.lang, None)

    def test_limit(self) -> None:
        """Test Query.limit()"""
        query = census.Query()
        self.assertEqual(query.data.limit, 1)
        query.limit(10)
        self.assertEqual(query.data.limit, 10)
        with self.assertRaises(ValueError):
            query.limit(-1)
        with self.assertRaises(ValueError):
            query.limit(0)
        query.limit_per_db(1)
        self.assertEqual(query.data.limit, 1)

    def test_limit_per_db(self) -> None:
        """Test Query.limit_per_db()"""
        query = census.Query()
        self.assertEqual(query.data.limit_per_db, 1)
        query.limit_per_db(10)
        self.assertEqual(query.data.limit_per_db, 10)
        with self.assertRaises(ValueError):
            query.limit_per_db(-1)
        with self.assertRaises(ValueError):
            query.limit_per_db(0)
        query.limit(1)
        self.assertEqual(query.data.limit_per_db, 1)

    def test_offset(self) -> None:
        """Test Query.offset()"""
        query = census.Query()
        self.assertEqual(query.data.start, 0)
        query.offset(10)
        self.assertEqual(query.data.start, 10)
        with self.assertRaises(ValueError):
            query.offset(-1)
        query.start(0)
        self.assertEqual(query.data.start, 0)

    def test_resolve(self) -> None:
        """Test Query.resolve()"""
        query = census.Query()
        self.assertListEqual(query.data.resolve, [])
        query.resolve('one')
        self.assertListEqual(query.data.resolve, ['one'])
        query.resolve('two', 'three')
        self.assertListEqual(query.data.resolve, ['two', 'three'])

    def test_retry(self) -> None:
        """Test Query.retry()"""
        query = census.Query()
        self.assertTrue(query.data.retry)
        query.retry(False)
        self.assertFalse(query.data.retry)
        query.retry(True)
        self.assertTrue(query.data.retry)

    def test_start(self) -> None:
        """Test Query.start()"""
        query = census.Query()
        self.assertEqual(query.data.start, 0)
        query.start(10)
        self.assertEqual(query.data.start, 10)
        with self.assertRaises(ValueError):
            query.start(-1)
        query.start(0)
        self.assertEqual(query.data.start, 0)

    def test_sort(self) -> None:
        """Test Query.sort()"""
        query = census.Query()
        self.assertListEqual(query.data.sort, [])
        query.sort('field')
        self.assertListEqual(query.data.sort, ['field'])
        query.sort(('field', False))
        self.assertListEqual(query.data.sort, [('field', False)])
        query.sort(('field_1', False), ('field_2', True))
        self.assertListEqual(
            query.data.sort, [('field_1', False), ('field_2', True)])

    def test_timing(self) -> None:
        """Test Query.timing()"""
        query = census.Query()
        self.assertFalse(query.data.timing)
        query.timing(True)
        self.assertTrue(query.data.timing)

    def test_tree(self) -> None:
        """Test Query.tree()"""
        query = census.Query()
        self.assertIsNone(query.data.tree)
        query.tree('field_', is_list=True, prefix='prefix_', start='start_')
        self.assertIsNotNone(query.data.tree)
        assert query.data.tree is not None  # Just here to satisfy linters
        self.assertDictEqual(
            query.data.tree, {'field': 'field_', 'is_list': True,
                              'prefix': 'prefix_', 'start': 'start_'})

    def test_url(self) -> None:
        """Test Query.url()"""
        query = census.Query()
        url = query.url()
        self.assertIsInstance(url, yarl.URL)
        comparison = yarl.URL(f'{ENDPOINT}s:example/get/ps2:v2')
        self.assertEqual(url, comparison)


class TestJoinedQueryInterface(unittest.TestCase):
    """Test the class interface of the JoinedQuery class."""

    def test_copy(self) -> None:
        """Test JoinedQuery.copy()"""
        template_query = census.Query('collection')
        template_query_list = census.Query('join').limit(100)
        template_join = census.JoinedQuery('join')
        # Query from non-list query
        copy_query = census.JoinedQuery.copy(template_query)
        self.assertEqual(
            copy_query.data.collection, template_query.data.collection)
        self.assertFalse(copy_query.data.is_list)
        self.assertEqual(copy_query.data.hide, template_join.data.hide)
        self.assertEqual(copy_query.data.show, template_join.data.show)
        self.assertEqual(copy_query.data.terms, template_join.data.terms)
        # Query from list query
        copy_query_list = census.JoinedQuery.copy(template_query_list)
        self.assertEqual(
            copy_query_list.data.collection, template_join.data.collection)
        self.assertTrue(copy_query_list.data.is_list)
        # Query from list join
        copy_join_list = census.JoinedQuery.copy(template_join)
        self.assertEqual(
            copy_join_list.data.collection, template_join.data.collection)
        self.assertEqual(copy_join_list.data, template_join.data)
        # Try copying a collection-less query
        template_empty_query = census.Query()
        with self.assertRaises(TypeError):
            _ = census.JoinedQuery.copy(template_empty_query)

    def test_serialise(self) -> None:
        """Test JoinedQuery.serialise()"""
        join = census.JoinedQuery('collection')
        serialised_data = join.serialise()
        self.assertEqual(join.data, serialised_data)
        join.create_join('nested_join')
        serialised_data = join.serialise()
        # NOTE: The values of the serialisation are not checked here as any
        # errors will become apparent as part of the URL generation.
        self.assertDictEqual(join.data.__dict__, serialised_data.__dict__)

    def test_set_fields(self) -> None:
        """Test JoinedQuery.set_fields()"""
        join = census.JoinedQuery('collection')
        self.assertIsNone(join.data.field_on)
        self.assertIsNone(join.data.field_to)
        join.set_fields('field1')
        self.assertEqual(join.data.field_on, 'field1')
        self.assertEqual(join.data.field_to, 'field1')
        join.set_fields('field2', 'field3')
        self.assertEqual(join.data.field_on, 'field2')
        self.assertEqual(join.data.field_to, 'field3')

    def test_set_list(self) -> None:
        """Test JoinedQuery.set_list()"""
        join = census.JoinedQuery('collection')
        self.assertFalse(join.data.is_list)
        join.set_list(True)
        self.assertTrue(join.data.is_list)
        join.set_list(False)
        self.assertFalse(join.data.is_list)

    def test_set_outer(self) -> None:
        """Test JoinedQuery.set_outer()"""
        join = census.JoinedQuery('collection')
        self.assertTrue(join.data.is_outer)
        join.set_outer(False)
        self.assertFalse(join.data.is_outer)
        join.set_outer(True)
        self.assertTrue(join.data.is_outer)


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

    def test_serialise(self) -> None:
        """Test JoinedQuery.serialise()"""
        # NOTE: The actual return value of the serialise function is not tested
        # here, that is instead done as part of the larger join checks.
        with self.assertRaises(ValueError):
            _ = census.SearchModifier.serialise(20)

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
        modifiers = ['', '<', '[', '>', ']', '^', '*', '!']
        for index, prefix in enumerate(modifiers):
            query = census.Query('dummy')
            mod = census.SearchModifier(index)
            url = query.add_term('field', 'value', modifier=mod).url()
            self.assertDictEqual(
                dict(url.query), {'field': f'{prefix}value'},
                f'Incorrect search modifier prefix; expected {prefix}')

    def test_warnings_empty_url(self) -> None:
        """Test warnings when using terms with empty collections."""
        query_empty = census.Query(service_id='s:dummy')
        query_empty_terms = census.Query(service_id='s:dummy', field='name')
        query_empty_joins = census.Query(service_id='s:dummy')
        query_empty_joins.create_join('other')
        with warnings.catch_warnings(record=True) as caught:
            assert caught is not None
            _ = query_empty.url()
            print(caught)
            self.assertFalse(find_warning(caught, 'No collection specified'))
        with warnings.catch_warnings(record=True) as caught:
            assert caught is not None
            _ = query_empty_terms.url()
            self.assertTrue(find_warning(
                caught, 'No collection specified, but 1 query terms provided'))
        with warnings.catch_warnings(record=True) as caught:
            assert caught is not None
            _ = query_empty_joins.url()
            self.assertTrue(find_warning(
                caught, 'No collection specified, but 1 joined queries'))


class TestURLsQueryCommands(unittest.TestCase):
    """Tests for the generation of query commands."""

    def test_qc_only(self) -> None:
        """Generate a query that uses a query command, but no terms."""
        url = census.Query('ability').distinct('ability_type_id').url()
        self.assertDictEqual(
            dict(url.query), {'c:distinct': 'ability_type_id'},
            'Incorrect query string')

    def test_qc_multi(self) -> None:
        """Generate a query using multiple query commands."""
        url = census.Query('vehicle').limit(10).start(20).url()
        self.assertDictEqual(
            dict(url.query), {'c:limit': '10', 'c:start': '20'},
            'Incorrect query string')

    def test_qc_mixed(self) -> None:
        """Generate a query using query commands and terms."""
        url = census.Query('item', faction=1).limit(100).url()
        self.assertDictEqual(
            dict(url.query), {'faction': '1', 'c:limit': '100'},
            'Incorrect query string')

    def test_show(self) -> None:
        """Test the c:show query command."""
        query = census.Query('character')
        url = query.show('name.first', 'battle_rank.value').url()
        self.assertDictEqual(
            dict(url.query), {'c:show': 'name.first,battle_rank.value'},
            'Incorrect query command: c:show')
        # Test both hide and show being added
        query.data.hide.append('faction_id')
        with warnings.catch_warnings(record=True) as caught:
            assert caught is not None
            query.url()
            self.assertTrue(find_warning(
                caught, 'Query.show and Query.hide are mutually'))

    def test_hide(self) -> None:
        """Test the c:hide query command."""
        query = census.Query('character')
        url = query.hide('name.first_lower').url()
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
        # Test invalid argument
        with self.assertRaises(ValueError):
            query.sort(('field',))  # type: ignore
            _ = query.url()

    def test_has(self) -> None:
        """Test the c:has query command."""
        query = census.Query('weapon')
        url = query.has('heat_capacity').url()
        self.assertDictEqual(
            dict(url.query), {'c:has': 'heat_capacity'},
            'Incorrect query command: c:has')

    def test_resolve(self) -> None:
        """Test the c:resolve query command."""
        query = census.Query('character')
        url = query.resolve('online_status').url()
        self.assertDictEqual(
            dict(url.query), {'c:resolve': 'online_status'},
            'Incorrect query command: c:resolve')

    def test_case(self) -> None:
        """Test the c:case query command."""
        query = census.Query('item')
        query.add_term('name.en', 'Pulsar',
                       modifier=census.SearchModifier.CONTAINS)
        url = query.case(False).url()
        self.assertDictEqual(
            dict(url.query), {'name.en': '*Pulsar', 'c:case': '0'},
            'Incorrect query command: c:case')

    def test_limit(self) -> None:
        """Test the c:limit query command."""
        query = census.Query('faction')
        url = query.limit(5).url()
        self.assertDictEqual(
            dict(url.query), {'c:limit': '5'},
            'Incorrect query command: c:limit')
        # Test both limit and limit_per_idea being added
        query.data.limit_per_db = 10
        with warnings.catch_warnings(record=True) as caught:
            assert caught is not None
            _ = query.url()
            self.assertTrue(find_warning(
                caught, 'Query.limit and Query.limit_per_db are mutually'))

    def test_limit_per_db(self) -> None:
        """Test the c:limit_per_db query command."""
        query = census.Query('character')
        url = query.limit_per_db(20).url()
        self.assertDictEqual(
            dict(url.query), {'c:limitPerDB': '20'},
            'Incorrect query command: c:limitPerDB')

    def test_start(self) -> None:
        """Test the c:start query command."""
        query = census.Query('weapon')
        url = query.sort('weapon_id').start(20).url()
        self.assertDictEqual(
            dict(url.query), {'c:sort': 'weapon_id', 'c:start': '20'},
            'Incorrect query command: c:start')
        query = census.Query('item')
        url = query.sort('item_id').offset(30).url()
        self.assertDictEqual(
            dict(url.query), {'c:sort': 'item_id', 'c:start': '30'},
            'Incorrect query command: c:start (aliased')

    def test_include_null(self) -> None:
        """Test the c:includeNull query command."""
        query = census.Query('weapon')
        url = query.include_null(True).url()
        self.assertDictEqual(
            dict(url.query), {'c:includeNull': '1'},
            'Incorrect query command: c:includeNull')

    def test_lang(self) -> None:
        """Test the c:lang query command."""
        query = census.Query('item')
        url = query.lang('en').url()
        self.assertDictEqual(
            dict(url.query), {'c:lang': 'en'},
            'Incorrect query command: c:lang')

    def test_join(self) -> None:
        """Test the c:join query command."""
        # Basic join
        query = census.Query('character')
        query.create_join('characters_world')
        url = query.url()
        self.assertDictEqual(
            dict(url.query), {'c:join': 'characters_world'},
            'Incorrect query command: c:join (test #1)')
        # Join with fields and show
        query = census.Query('outfit')
        join = query.create_join('character')
        join.set_fields('leader_character_id', 'character_id')
        join.show('name.first')
        url = query.url()
        self.assertDictEqual(
            dict(url.query),
            {'c:join': 'character^on:leader_character_id'
                       '^to:character_id^show:name.first'},
            'Incorrect query command: c:join (test #2)')
        # Join with hide, list, and inject_at
        query.joins.clear()
        join = query.create_join('outfit_member')
        join.hide('outfit_id')
        join.set_list(True)
        join.set_inject_at('members')
        url = query.url()
        self.assertDictEqual(
            dict(url.query),
            {'c:join': 'outfit_member^list:1'
                       '^hide:outfit_id^inject_at:members'},
            'Incorrect query command: c:join (test #3)')
        # Nested inner joins with list
        query = census.Query('character')
        join = query.create_join('characters_item')
        join.set_outer(False)
        nested = join.create_join('item', faction_id=0, max_stack_size='>1')
        nested.set_outer(False)
        nested.set_list(True)
        url = query.url()
        self.assertDictEqual(
            dict(url.query),
            {'c:join': 'characters_item^outer:0(item^list:1^outer:0'
                       '^terms:faction_id=0\'max_stack_size=>1)'},
            'Incorrect query command: c:join (test #4)')
        # Multiple nested joins with siblings
        query.joins.clear()
        join = query.create_join('parent')
        child_1 = join.create_join('child_1')
        child_2 = join.create_join('child_2')
        grandchild_1 = child_1.create_join('grandchild_1')
        grandchild_1.create_join('great_grandchild_1')
        child_2.create_join('grandchild_2_a')
        child_2.create_join('grandchild_2_b')
        url = query.url()
        self.assertDictEqual(
            dict(url.query),
            {'c:join': 'parent(child_1(grandchild_1(great_grandchild_1)),'
                       'child_2(grandchild_2_a,grandchild_2_b))'},
            'Incorrect query command: c:join (test #5)')

    def test_tree(self) -> None:
        """Test the c:tree query command."""
        query = census.Query('vehicle').limit(40)
        url = query.tree('type_id', True, 'type_', 'start_').url()
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
            tree_dict, {'field': 'type_id', 'prefix': 'type_',
                        'list': '1', 'start': 'start_'},
            'Invalid key/value pairs for query command: c:tree')

    def test_timing(self) -> None:
        """Test the c:timing query command."""
        url = census.Query('character').timing(True).url()
        self.assertDictEqual(
            dict(url.query), {'c:timing': '1'},
            'Incorrect query command: c:timing')

    def test_exact_match_first(self) -> None:
        """Test the c:exactMatchFirst query command."""
        url = census.Query('character').exact_match_first(True).url()
        self.assertDictEqual(
            dict(url.query), {'c:exactMatchFirst': '1'},
            'Incorrect query command: c:exactMatchFirst')

    def test_distinct(self) -> None:
        """Test the c:distinct query command."""
        url = census.Query('effect').distinct('effect_type_id').url()
        self.assertDictEqual(
            dict(url.query), {'c:distinct': 'effect_type_id'},
            'Incorrect query command: c:distinct')

    def test_retry(self) -> None:
        """Test the c:retry query command."""
        url = census.Query('character').retry(False).url()
        self.assertDictEqual(
            dict(url.query), {'c:retry': '0'},
            'Incorrect query command: c:retry')


def find_warning(caught: List[warnings.WarningMessage], msg: str) -> bool:
    """Return whether exactly one matching warning was caught.

    This only works for UserWarning subclasses.

    Arguments:
        caught: The messages to check.
        msg: The warning message string to scan for.

    Returns:
        Whether the given warning matches the requirements.

    """
    matches = 0
    for warning in caught:
        if issubclass(warning.category, UserWarning) and msg in str(warning):
            matches += 1
    return matches == 1

"""Tet cases for the Query object and URL generation."""

import unittest
from auraxium import census


class TestURLs(unittest.TestCase):
    """Test cases comparing URL generation to the expected output."""

    ENDPOINT = 'https://census.daybreakgames.com/'

    def test_rest_endpoint(self):
        """Test whether the ReST API endpoint is correct."""
        test = census.Query().url()
        self.assertTrue(str(test).startswith(self.ENDPOINT))

    def test_service_id(self):
        """Test whether a custom service ID is parsed corretly."""
        # NOTE: This service ID probably does not exist, but this is not
        # relevant for the purpose of this test.
        EXPECTED = f'{self.ENDPOINT}s:arx_test/get/ps2:v2'
        test = census.Query(namespace='ps2:v2', service_id='s:arx_test').url()
        self.assertEqual(str(test), EXPECTED)

    def test_namespace_table(self):
        """Test empty namespace URL."""
        EXPECTED = f'{self.ENDPOINT}s:example/get/ps2:v2'
        test = census.Query(namespace='ps2:v2').url()
        self.assertEqual(str(test), EXPECTED)

    def test_collection_single(self):
        """Test whether basic table lookups are correctly generated."""
        EXPECTED = f'{self.ENDPOINT}s:example/get/ps2:v2/outfit'
        test = census.Query('outfit', namespace='ps2:v2').url()
        self.assertEqual(str(test), EXPECTED)

    def test_query_term_single(self):
        """Test whether a single query term is correctly parsed."""
        EXPECTED = f'{self.ENDPOINT}s:example/get/ps2:v2/world?name.en=Connery'
        test = census.Query('world', name__en='Connery').url()
        self.assertEqual(str(test), EXPECTED)

    def test_query_term_with_modifier_string(self):
        """Test whether a modifer (>, <, [, ], *, !) is correctly handled"""
        EXPECTED = f'{self.ENDPOINT}s:example/get/ps2:v2/character_name' \
                   f'?name.first_lower=^lite&c:show=name.first&c:limit=10'
        test_query = census.Query('character_name', name__first_lower='^lite')
        test_query.limit(10).show('name.first')

        self.assertEqual(test_query.url().human_repr(), EXPECTED)

        correct_term = census.SearchTerm('name.first_lower', 'lite',
                                         census.SearchModifier.STARTS_WITH)
        term = test_query.data.terms[0]
        self.assertTrue(term.field == correct_term.field
                        and term.value == correct_term.value
                        and term.modifier == correct_term.modifier)

    def test_generate_term_with_extra_equals(self):
        EXPECTED = f'{self.ENDPOINT}s:example/get/ps2:v2/character?character_id=5428018587875812257&c:show=name'
        test = census.Query('character', character_id='5428018587875812257')
        test.show('name')
        self.assertEqual(test.url().human_repr(), EXPECTED)

    def test_query_term_with_number(self):
        """Test whether a term with a int value is correctly parsed"""

        EXPECTED = f'{self.ENDPOINT}s:example/get/ps2:v2/character?character_id=5428018587875812257&c:show=name'
        query = census.Query('character', character_id=5428018587875812257)
        test = query.show('name').url()
        self.assertEqual(str(test), EXPECTED)

    def test_query_term_multi(self):
        """Test whether multiple query terms are correctly parsed."""
        # NOTE: NC Flash
        VALID_OPTIONS = [f'{self.ENDPOINT}s:example/get/ps2:v2/vehicle_faction'
                         '?vehicle_id=1&faction_id=2',
                         f'{self.ENDPOINT}s:example/get/ps2:v2/vehicle_faction'
                         '?faction_id=2&vehicle_id=1']
        test = census.Query(
            'vehicle_faction', vehicle_id=1, faction_id=2).url()
        self.assertIn(str(test), VALID_OPTIONS)

    def test_search_modifiers(self):
        """Test whether search modifiers are correctly parsed."""
        MODIFIERS = {'lt': '<', 'lte': '[', 'gt': '>', 'gte': ']',
                     'sw': '^', 'in': '*', 'ne': '!'}
        # NOTE: This does not check if the field and modifier make sense, it
        # only cares about the URL and whether the right one was used.

        def test_query(url, modifier):
            return url.split('=')[1].startswith(MODIFIERS[modifier])

        # Less than
        test = census.Query('dummy')
        test.add_term('field', 'value',
                      modifier=census.SearchModifier.LESS_THAN)
        self.assertTrue(test_query(test.url().human_repr(), 'lt'), 'Less than')
        # Less than or equal
        test = census.Query('dummy')
        test.add_term('field', 'value',
                      modifier=census.SearchModifier.LESS_THAN_OR_EQUAL)
        self.assertTrue(test_query(test.url().human_repr(),
                                   'lte'), 'Less than or equal')
        # Greater than
        test = census.Query('dummy')
        test.add_term('field', 'value',
                      modifier=census.SearchModifier.GREATER_THAN)
        self.assertTrue(test_query(
            test.url().human_repr(), 'gt'), 'Greater than')
        # Greater than or equal
        test = census.Query('dummy')
        test.add_term('field', 'value',
                      modifier=census.SearchModifier.GREATER_THAN_OR_EQUAL)
        self.assertTrue(test_query(test.url().human_repr(),
                                   'gte'), 'Greater than or equal')
        # Starts with (RegEx)
        test = census.Query('dummy')
        test.add_term('field', 'value',
                      modifier=census.SearchModifier.STARTS_WITH)
        self.assertTrue(test_query(
            test.url().human_repr(), 'sw'), 'Starts with')
        # Contains (RegEx)
        test = census.Query('dummy')
        test.add_term('field', 'value',
                      modifier=census.SearchModifier.CONTAINS)
        self.assertTrue(test_query(test.url().human_repr(), 'in'), 'Contains')
        # Not equal
        test = census.Query('dummy')
        test.add_term('field', 'value',
                      modifier=census.SearchModifier.NOT_EQUAL)
        self.assertTrue(test_query(test.url().human_repr(), 'ne'), 'Not equal')

    # Query commands

    def test_qc_only(self):
        """Test query strings only containing query commands."""
        EXPECTED = f'{self.ENDPOINT}s:example/get/ps2:v2/world?c:limit=10'
        test = census.Query('world').limit(10)
        self.assertEqual(test.url().human_repr(), EXPECTED)

    def test_qc_combined(self):
        """Test query strings with query commands and paramters."""
        VALID_OPTIONS = [f'{self.ENDPOINT}s:example/get/ps2:v2/character'
                         '?name.first_lower=^bob&c:limit=50',
                         f'{self.ENDPOINT}s:example/get/ps2:v2/character'
                         '?c:limit=50&name.first_lower=^bob']
        test = census.Query('character')
        test.add_term('name.first_lower', 'bob',
                      modifier=census.SearchModifier.STARTS_WITH)
        test.limit(50)
        self.assertIn(test.url().human_repr(), VALID_OPTIONS)

    def test_qc_show(self):
        """Test the "c:show" query command."""
        VALID_OPTIONS = [f'{self.ENDPOINT}s:example/get/ps2:v2/character?'
                         'c:show=name.first,battle_rank',
                         f'{self.ENDPOINT}s:example/get/ps2:v2/character?'
                         'c:show=battle_rank,name.first']
        test = census.Query('character').show('name.first', 'battle_rank')
        self.assertIn(test.url().human_repr(), VALID_OPTIONS)

    def test_qc_hide(self):
        """Test the "c:hide" query command."""
        VALID_OPTIONS = [f'{self.ENDPOINT}s:example/get/ps2:v2/character?'
                         'c:hide=name.first,battle_rank',
                         f'{self.ENDPOINT}s:example/get/ps2:v2/character?'
                         'c:hide=battle_rank,name.first']
        test = census.Query('character').hide('name.first', 'battle_rank')
        self.assertIn(test.url().human_repr(), VALID_OPTIONS)

    def test_qc_sort(self):
        """Test the "c:sort" query command."""
        ASCENDING = (f'{self.ENDPOINT}s:example/get/ps2:v2/character?'
                     'c:sort=battle_rank')
        DESCENDING = (f'{self.ENDPOINT}s:example/get/ps2:v2/character?'
                      'c:sort=battle_rank:-1')
        test = census.Query('character').sort('battle_rank')
        self.assertEqual(test.url().human_repr(), ASCENDING, 'Ascending')
        test.sort_by = []
        test.sort(('battle_rank', False))
        self.assertEqual(test.url().human_repr(), DESCENDING, 'Descending')

    def test_qc_has(self):
        """Test the "c:has" query command."""
        EXPECTED = f'{self.ENDPOINT}s:example/get/ps2:v2/ability?c:has=param1'
        test = census.Query('ability')
        test.has('param1')
        self.assertEqual(test.url().human_repr(), EXPECTED)

    def test_qc_resolve(self):
        """Test the "c:resolve" query command."""
        EXPECTED = (f'{self.ENDPOINT}s:example/get/ps2:v2/'
                    'character?c:resolve=world')
        test = census.Query('character')
        test.resolve('world')
        self.assertEqual(test.url().human_repr(), EXPECTED)

    # TODO: c:case, c:limit, c:limitPerDb, c:start, c:offset, c:includeNull,
    # c:lang, c:join, c:tree, c:timing, c:exactMatchFirst, c:distinct, c:retry

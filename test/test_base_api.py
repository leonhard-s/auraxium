import json
import unittest

import requests

import auraxium


# Set the custom service id for testing
from . import service_id
auraxium.service_id = service_id


class TestArxBase(unittest.TestCase):
    """Test cases for the core auraxium components."""

    # --- Basic query tests ---

    def test_count(self):
        # Tests a basic count request
        URL = 'http://census.daybreakgames.com/count/ps2/faction'
        expected_response = int(json.loads(requests.get(URL).text)['count'])
        test_response = auraxium.Query('faction', namespace='ps2').count()
        self.assertEqual(expected_response, test_response)

    def test_get_simple(self):
        # Tests a basic get request
        URL = 'http://census.daybreakgames.com/get/ps2/faction?faction_id=1'
        expected_response = json.loads(requests.get(URL).text)['faction_list'][0]
        test_response = auraxium.Query('faction', namespace='ps2', faction_id='1').get(True)
        self.assertEqual(expected_response, test_response)

    # -- Query command tests ---

    def test_join_simple(self):
        # Test single-level joined queries
        URL = ('http://census.daybreakgames.com/get/ps2/outfit?c:join=character'
               '^on:leader_character_id^to:character_id')
        expected_response = json.loads(requests.get(URL).text)['outfit_list']
        query = auraxium.Query('outfit', namespace='ps2')
        query.join('character', on='leader_character_id', to='character_id')
        self.assertEqual(expected_response, query.get())

    # --- Exception tests ---

    def test_invalid_field_name(self):
        # Test if an InvalidSearchTermError is raised when using rubbish field names
        query = auraxium.Query('character', 'ps2', rubbish__field_name='value')
        with self.assertRaises(auraxium.exceptions.InvalidSearchTermError):
            query.get()

    def test_unknown_collection(self):
        # Test if an UnknownCollectionError is raised when using rubbish collection names
        query = auraxium.Query('rubbish_1234', 'ps2')
        with self.assertRaises(auraxium.exceptions.UnknownCollectionError):
            query.get()

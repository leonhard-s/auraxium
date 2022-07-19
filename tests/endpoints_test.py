"""Test cases for custom community endpoint support."""

import unittest

# pylint: disable=import-error
import auraxium
from auraxium import endpoints, ps2


class EndpointConfigurationTest(unittest.TestCase):
    """Local test testing endpoint configuration."""

    def test_defaults(self) -> None:
        """Ensure the PS2 endpoints are used by default."""
        client = auraxium.Client()
        self.assertListEqual(client.endpoints, [endpoints.DBG_CENSUS])
        # client = auraxium.EventClient()
        # client.ess_endpoint = endpoints.DBG_STREAMING

    def test_custom(self) -> None:
        """Ensure a single custom endpoint overrides as intended."""
        client = auraxium.Client(endpoints=endpoints.SANCTUARY_CENSUS)
        self.assertListEqual(client.endpoints, [endpoints.SANCTUARY_CENSUS])

    def test_custom_url(self) -> None:
        """Custom endpoints must be used for URL generation."""
        client = auraxium.Client(endpoints=endpoints.SANCTUARY_CENSUS)
        dummy = ps2.FireGroup({'fire_group_id': 0}, client=client)
        url = str(dummy.query().url())
        self.assertEqual(url, 'https://census.lithafalcon.cc/get/'
                         'ps2:v2/fire_group?fire_group_id=0')

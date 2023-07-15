"""Test cases for custom community endpoint support."""

import unittest

import auraxium
from auraxium import endpoints, ps2


class EndpointConfigurationTest(unittest.IsolatedAsyncioTestCase):
    """Local test testing endpoint configuration."""

    client: auraxium.Client

    async def asyncTearDown(self) -> None:
        await self.client.close()

    async def test_defaults(self) -> None:
        """Ensure the PS2 endpoints are used by default."""
        self.client = auraxium.Client()
        self.assertListEqual(self.client.endpoints, [endpoints.DBG_CENSUS])
        await self.client.close()
        self.client = auraxium.EventClient()
        self.client.ess_endpoint = endpoints.DBG_STREAMING

    async def test_custom(self) -> None:
        """Ensure a single custom endpoint overrides as intended."""
        self.client = auraxium.Client(endpoints=endpoints.SANCTUARY_CENSUS)
        self.assertListEqual(
            self.client.endpoints, [endpoints.SANCTUARY_CENSUS])

    async def test_custom_url(self) -> None:
        """Custom endpoints must be used for URL generation."""
        self.client = auraxium.Client(endpoints=endpoints.SANCTUARY_CENSUS)
        dummy = ps2.FireGroup({'fire_group_id': 0}, client=self.client)
        url = str(dummy.query().url())
        self.assertEqual(url, 'https://census.lithafalcon.cc/get/'
                         'ps2:v2/fire_group?fire_group_id=0')


class LiveEndpointTest(unittest.IsolatedAsyncioTestCase):
    """Live tests for custom community endpoints."""

    client: auraxium.EventClient

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()
        await self.client.close()

    async def test_custom_rest(self) -> None:
        """Test a custom REST endpoint."""
        self.client = auraxium.EventClient(
            endpoints=[endpoints.SANCTUARY_CENSUS])
        result = await self.client.get_by_id(ps2.Faction, 4)
        if result is None:
            self.skipTest('Endpoint not available')

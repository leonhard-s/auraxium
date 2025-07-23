"""Custom test fixture for live tests."""

import asyncio
import unittest
from typing import ClassVar, Optional

import auraxium
from auraxium import census

from tests.utils import SERVICE_ID

__all__ = [
    'LiveApiTestCase',
]

API_AVAILABILITY_TIMEOUT = 10.0


class LiveApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Base class for live API tests.

    This includes globally skipping tests if no service ID is provided,
    as well as checking for API availability before running any tests.
    """

    _api_available: ClassVar[Optional[bool]] = None

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        if self._api_available is None:
            api_available = await self._check_api_availability()
            # pylint: disable=protected-access
            self.__class__._api_available = api_available

        if not self._api_available:
            self.skipTest('unable to connect to census')
        elif SERVICE_ID in ['', 's:example']:
            self.skipTest('missing service ID')

    async def _check_api_availability(self) -> bool:
        api_available = False
        client = auraxium.Client(service_id=SERVICE_ID)
        try:
            query = census.Query(None, service_id=SERVICE_ID)
            data = await asyncio.wait_for(
                client.request(query), timeout=API_AVAILABILITY_TIMEOUT)
            if data and 'datatype_list' in data:
                api_available = True
        except asyncio.TimeoutError:
            pass
        finally:
            await client.close()
        return api_available

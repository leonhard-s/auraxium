"""Unit tests for the auraxium.request sub module.

Some tests will be skipped if the SERVICE_ID environment variable has
not been set.
"""

import json
import os
import unittest
from typing import Any, Dict, cast
import warnings

import aiohttp
import yarl

# pylint: disable=import-error
from auraxium import errors, _rest as request
from auraxium.types import CensusData

from tests.utils import DATA

PAYLOADS = os.path.join(DATA, 'rest')


class DummyResponse:
    """A dummy that can be used like ``aiohttp.ClientResponse``.

    This only implements the parts of the API that are currently used
    by tests, you'll likely have to update this if you are expanding
    the tests its used by.
    """

    def __init__(self, is_json: bool, reports_json: bool = True) -> None:
        self._data = {'success': 'True'}
        self.is_json: bool = is_json
        self.reports_json: bool = reports_json

    @property
    def real_url(self) -> yarl.URL:
        """Return the URL that provoked the response."""
        return yarl.URL('census.daybreakgames.com/get/ps2/')

    @property
    def request_info(self) -> aiohttp.RequestInfo:
        """Return a container with generic request information."""
        return aiohttp.RequestInfo(self.real_url, 'get', {})  # type: ignore

    async def json(self) -> Any:
        """Return the JSON data contained in the response.

        Depending on what values were specified when this dummy
        response was created, this may raise errors.
        """
        if not (self.is_json and self.reports_json):
            raise aiohttp.ContentTypeError(
                self.request_info, (), message='Dummy')
        return self._data

    async def text(self) -> str:
        """Return the response's data as plain text."""
        if self.is_json:
            return str(self._data).replace('\'', '"')
        return str('Non-JSON data')


class TestPayloadParsing(unittest.IsolatedAsyncioTestCase):
    """Ensure payloads are properly converted into errors."""

    def test_url_parser(self) -> None:
        """Test the URL parser used for introspection and errors."""
        url = yarl.URL(
            'http://census.daybreakgames.com/get/ps2/item?name.en=*Punisher')
        self.assertTupleEqual(request.get_components(url), ('ps2', 'item'))
        url = yarl.URL(
            'http://census.daybreakgames.com/get/ps2/')
        self.assertTupleEqual(request.get_components(url), ('ps2', None))
        url = yarl.URL(
            'http://census.daybreakgames.com/s:example/get/ps2/item')
        self.assertTupleEqual(request.get_components(url), ('ps2', 'item'))
        url = yarl.URL(
            'http://census.daybreakgames.com/s:example/xml/get/ps2/item')
        self.assertTupleEqual(request.get_components(url), ('ps2', 'item'))
        url = yarl.URL(
            'http://census.daybreakgames.com/xml/get/ps2/item')
        self.assertTupleEqual(request.get_components(url), ('ps2', 'item'))

    def test_error_parsers(self) -> None:
        """Test error detection."""

        def raise_helper(name: str) -> None:
            filepath = os.path.join(PAYLOADS, 'errors', f'{name}.json')
            with open(filepath) as payload_file:
                payload: Dict[str, Any] = json.load(payload_file)
            url = yarl.URL(payload.pop('_URL'))
            request.raise_for_dict(payload, url)

        # Empty URL
        with self.assertRaises(errors.ServerError):
            raise_helper('empty-url')
        # Invalid namespace
        with self.assertRaises(errors.UnknownCollectionError) as ctx:
            raise_helper('invalid-namespace')
        self.assertSequenceEqual(ctx.exception.namespace, 'bogus')
        self.assertIsNone(ctx.exception.collection)
        # Invalid collection
        with self.assertRaises(errors.UnknownCollectionError) as ctx:
            raise_helper('unknown-collection')
        self.assertSequenceEqual(ctx.exception.namespace, 'ps2')
        self.assertEqual(ctx.exception.collection, 'bogus')
        # Bad syntax
        with self.assertRaises(errors.BadRequestSyntaxError):
            raise_helper('bad-request-syntax')
        # Service unavailable
        with self.assertRaises(errors.ServiceUnavailableError):
            raise_helper('service-unavailable')
        # Invalid service ID
        with self.assertRaises(errors.InvalidServiceIDError):
            raise_helper('service-id_invalid')
        # Missing service ID
        with self.assertRaises(errors.MissingServiceIDError):
            raise_helper('service-id_missing')
        # Generic server error
        with self.assertRaises(errors.ServerError):
            raise_helper('server-error_generic')
        # Specified server error
        with self.assertRaises(errors.ServerError):
            raise_helper('server-error_specific')
        # Generic fallback error
        with self.assertRaises(errors.CensusError):
            raise_helper('fallback')

        # NOTE: Invalid search term errors are handled in another method and
        # are grouped below.

        # Invalid field (term)
        with self.assertRaises(errors.InvalidSearchTermError) as ctx:
            raise_helper('invalid-value_term')
        err = ctx.exception
        self.assertEqual(err.namespace, 'ps2')
        self.assertEqual(err.collection, 'item')
        self.assertEqual(err.field, 'item_id')
        # Invalid field (RegEx)
        with self.assertRaises(errors.InvalidSearchTermError) as ctx:
            raise_helper('invalid-value_regex')
        err = ctx.exception
        self.assertEqual(err.namespace, 'ps2')
        self.assertEqual(err.collection, 'item')
        self.assertEqual(err.field, 'name.en')
        # Invalid field (limit)
        with self.assertRaises(errors.InvalidSearchTermError) as ctx:
            raise_helper('invalid-value_limit')
        err = ctx.exception
        self.assertEqual(err.namespace, 'ps2')
        self.assertEqual(err.collection, 'item')
        self.assertEqual(err.field, 'c:limit')
        # Invalid field (term)
        with self.assertRaises(errors.InvalidSearchTermError) as ctx:
            raise_helper('invalid-field_show')
        err = ctx.exception
        self.assertEqual(err.namespace, 'ps2')
        self.assertEqual(err.collection, 'item')
        self.assertEqual(err.field, 'c:show')
        # Invalid field (c:show)
        with self.assertRaises(errors.InvalidSearchTermError) as ctx:
            raise_helper('invalid-field_term')
        err = ctx.exception
        self.assertEqual(err.namespace, 'ps2')
        self.assertEqual(err.collection, 'item')
        self.assertEqual(err.field, 'invalid_field')

    def test_extract_payload(self) -> None:
        """Test payload extraction (multi)."""
        filepath = os.path.join(
            PAYLOADS, 'datatype_payloads', 'character.json')
        with open(filepath) as file_data:
            data = json.load(file_data)
        data = request.extract_payload(data, 'character')
        self.assertTrue(len(data), 20)
        self.assertTrue('character_id' in data[0])
        self.assertTrue(len(data[0]), 20)
        with self.assertRaises(errors.PayloadError):
            _ = request.extract_payload({}, 'example')

    def test_extract_single(self) -> None:
        """Test payload extraction (single)."""
        filepath = os.path.join(
            PAYLOADS, 'datatype_payloads', 'character.json')
        with open(filepath) as file_data:
            data = json.load(file_data)
        # Ensure warnings are raised
        with warnings.catch_warnings(record=True) as caught:
            assert caught is not None
            _ = request.extract_single(data, 'character')
        warning = caught[0]
        self.assertTrue(
            ((issubclass(warning.category, UserWarning)
              and 'The dictionary passed' in str(warning))), 'Missing warning')
        # Assert no warning with single-payloads
        first = cast(CensusData, data['character_list'][0])
        single: CensusData = {'character_list': [first], 'returned': 1}
        with warnings.catch_warnings(record=True) as caught:
            assert caught is not None
            data = request.extract_single(single, 'character')
        self.assertEqual(len(caught), 0, 'Unexpected warning')
        # Check contents
        self.assertTrue('character_id' in data)
        with self.assertRaises(errors.PayloadError):
            _ = request.extract_single({}, 'example')
        # Check for NotFoundError
        with self.assertRaises(errors.NotFoundError):
            _ = request.extract_single({'item_list': []}, 'item')

    async def test_response_to_dict(self) -> None:
        """Test dict conversion of HTTP responses."""
        # JSON as JSON
        response = DummyResponse(is_json=True, reports_json=True)
        dict_ = await request.response_to_dict(response)  # type: ignore
        self.assertDictEqual(dict_, await response.json())
        # JSON as text
        response = DummyResponse(is_json=True, reports_json=False)
        dict_ = await request.response_to_dict(response)  # type: ignore
        self.assertDictEqual(dict_, json.loads(await response.text()))
        # Invalid
        response = DummyResponse(is_json=False, reports_json=False)
        with self.assertRaises(errors.ResponseError):
            _ = await request.response_to_dict(response)  # type: ignore

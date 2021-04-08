"""REST API interface and response checking for Auraxium.

This module is responsible for performing the HTTP requests themselves,
handling any HTTP-related errors, and converting the returned data into
a dictionary that can be parsed by the object model.

It also checks for API error codes and raises the appropriate
exceptions.

All requests are buffered, allowing up to five HTTP-related errors
before giving up and letting the error propagate outwards.
"""

import asyncio
import copy
import json
import logging
import sys
import warnings
from typing import Any, Dict, Iterator, Literal, List, Optional, Tuple, Type, TypeVar, cast
from types import TracebackType

import aiohttp
import backoff
import yarl

from .census import Query
from .errors import (PayloadError, BadRequestSyntaxError, CensusError,
                     InvalidSearchTermError, InvalidServiceIDError,
                     MaintenanceError, MissingServiceIDError, NotFoundError,
                     ResponseError, ServerError, ServiceUnavailableError,
                     UnknownCollectionError)
from .types import CensusData

__all__ = [
    'RequestClient',
    'extract_payload',
    'extract_single',
    'run_query'
]

_T = TypeVar('_T')

_log = logging.getLogger('auraxium.http')


class RequestClient:
    """The REST request handler for Auraxium."""

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None,
                 service_id: str = 's:example', profiling: bool = False
                 ) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.profiling = profiling
        self.service_id = service_id
        self.session = aiohttp.ClientSession()
        self._timing_cache: List[float] = []

    async def __aenter__(self: _T) -> _T:
        """Enter the context manager and return the client."""
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> Literal[False]:
        """Exit the context manager.

        This closes the internal HTTP session before exiting, no error
        handling will be performed.

        Arguments:
            exc_type: The type of exception that was raised.
            exc_value: The exception value that was raised.
            traceback: The traceback type of the exception.

        Returns:
            Always False, i.e. no error suppression.

        """
        await self.close()
        return False  # Do not suppress any exceptions

    @property
    def latency(self) -> float:
        """Return the average request latency for the client.

        This averages up to the last 100 query times. Use the logging
        utility to gain more insight into which queries take the most
        time.

        """
        if not self._timing_cache:
            return -1.0
        return sum(self._timing_cache) / len(self._timing_cache)

    async def close(self) -> None:
        """Shut down the client.

        This will end the HTTP session used for requests to the REST
        API.

        Call this to clean up before the client object is destroyed.

        """
        _log.info('Shutting down client')
        await self.session.close()

    async def request(self, query: Query, verb: str = 'get') -> CensusData:
        """Perform a REST API request.

        This performs the query and performs error checking to ensure
        the query is valid.

        Refer to the :meth:`auraxium.request.raise_for_dict()` method
        for a list of exceptions raised from API errors.

        Arguments:
            query: The query to perform.
            verb (optional): The query verb to utilise.
                Defaults to ``'get'``.

        Returns:
            The API response payload received.

        """
        if self.profiling:
            # Create a copy of the query before modifying it
            query = copy.copy(query)
            query.timing(True)
        data = await run_query(query, verb=verb, session=self.session)
        if self.profiling and verb == 'get':
            timing = cast(CensusData, data.pop('timing'))
            if _log.level <= logging.DEBUG:
                url = query.url()
                _log.debug('Query times for "%s?%s": %s',
                           '/'.join(url.parts[-2:]), url.query_string,
                           ', '.join([f'{k}: {v}' for k, v in timing.items()]))
            self._timing_cache.append(float(str(timing['total-ms'])))
        return data


def get_components(url: yarl.URL) -> Tuple[str, Optional[str]]:
    """Return the namespace and collection of a given query.

    Arguments:
        url: The :class:`yarl.URL` to process. Only REST API query URLs
            in the DBG census API format are allowed.

    Returns:
        The namespace/game and collection that was accessed. Collection
        may be ``None`` for some queries.

    """
    components = url.path.split('/')[1:]
    if components[0].startswith('s:'):  # Remove service ID
        _ = components.pop(0)
    if components[0] in ('xml', 'json'):  # Remove format specifier
        _ = components.pop(0)
    _ = components.pop(0)  # Remove query verb
    if not components[-1]:  # Remove collection if empty
        _ = components.pop(-1)
    # If only a namespace was provided, return None as the collection
    if len(components) == 1:
        return components[0], None
    assert len(components) == 2, 'Unable to parse URL'
    return components[0], components[1]


async def response_to_dict(response: aiohttp.ClientResponse) -> CensusData:
    """Convert a response received from the server to a dictionary.

    In some cases - mostly error states - the API will return JSON data
    without providing the appropriate ``Content-Type`` entity header,
    which breaks :meth:`aiohttp.ClientResponse.json()`.

    This function catches this error and generates the expected
    dictionary from the plain text response instead, if possible. If
    the native :mod:`json` module cannot parse the response either, a
    :class:`~auraxium.errors.ResponseError` is raised.

    Arguments:
        response: The :class:`aiohttp.ClientResponse` to convert.

    Raises:
        ResponseError: Raised if the response cannot be converted into
            a dictionary.

    Returns:
        A dictionary containing the response payload.

    """
    data: CensusData
    try:
        # NOTE: It is possible to skip content type checking completely by
        # setting the content_type flag to False and letting its JSON decoder
        # error out within aiohttp, then handle that - this is arguably neater.
        data = await response.json()
    except aiohttp.ContentTypeError as err:
        text = await response.text()
        # Run the plain text through the JSON decoder anyway before we let the
        # error propagate to handle the misrepresented content type issue.
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # There really is something wrong with this data, let an updated
            # error propagate.
            raise ResponseError(
                f'Received a non-JSON response: {text}') from err
        _log.info(
            'Received a plain text response containing JSON data: %s', text)
        return data
    return data


def extract_payload(data: CensusData, collection: str) -> List[CensusData]:
    """Extract the payload from a census response dictionary.

    Arguments:
        data: The response dictionary to process.
        collection: The collection name to expect.

    Raises:
        BadPayloadError: Raised if the provided response dictionary
            lacks the collection-specific key expected.

    Returns:
        All dictionaries in the response list.

    """
    try:
        list_ = cast(List[CensusData], data[f'{collection}_list'])
    except KeyError as err:
        raise PayloadError(
            f'Unable to extract list of results due to missing key '
            f'"{collection}_list" in payload: {data}', data) from err
    return list_


def extract_single(data: CensusData, collection: str,
                   no_warn_multi: bool = False) -> CensusData:
    """Extract the payload from a census response dictionary.

    Identical to :meth:`extract_payload`, but only returns the first
    match. If multiple results are found, a warning will be issued.

    Arguments:
        data: The response dictionary to process.
        collection: The collection name to expect.
        no_warn_multi (optional): Set this flag to disable the warning
            issued when using this function on a multi-result payload.

    Raises:
        BadPayloadError: Raised if the provided response dictionary
            lacks the collection-specific key expected.
        NotFoundError: Raised if the collection does not contain any
            results.

    Returns:
        The first result payload in the given dictionary.

    """
    try:
        list_ = extract_payload(data, collection)
    except PayloadError as err:
        raise PayloadError(
            f'Unable to extract result due to missing key "{collection}_list" '
            f'in payload: {data}', data) from err
    if not list_:
        raise NotFoundError('The server did not return any matches')
    if not no_warn_multi and len(list_) > 1:
        warnings.warn('The dictionary passed to extract_single contained '
                      'multiple results. Check your query limit settings or '
                      'use extract_payload if you expect a list of results.')
    return list_[0]


def raise_for_dict(data: CensusData, url: yarl.URL) -> None:
    """Check an API response dictionary for errors.

    This raises the appropriate :class:`auraxium.errors.CensusError`
    subclass for a given API response.

    Arguments:
        data: The API response dictionary to check.
        url: The URL used to perform the request. This is included in
            any errors raised to facilitate troubleshooting.

    Raises:
        UnknownCollectionError: Raised when attempting to query a
            namespace or collection that does not exist.
        BadRequestSyntaxError: Raised if the server reports an
            erroneous query.
        ServiceUnavailableError: Raised if the API service accessed is
            currently unavailable.
        InvalidServiceIDError: Raised when using invalid service IDs.
        MissingServiceIDError: Raised when exceeding the rate limits
            imposed on the public ``s:examples`` service ID.
        ServerError: Raised for server-side query parsing errors.
        InvalidSearchTermError: Raised for bad field names or values
        CensusError: Raised for unknown server-side errors.

    """
    # Syntax parser and namespace dispatching
    if (msg := data.get('error')) is not None:
        if msg == 'No data found.':
            namespace, collection = get_components(url)
            # NOTE: This error is returned if either the namespace or
            # collection are unknown
            if collection is None:
                raise UnknownCollectionError(
                    f'The namespace "{namespace}" does not exist.',
                    url, namespace, collection)
            help_url = Query(namespace=namespace)
            raise UnknownCollectionError(
                f'No collection at "{namespace}/{collection}", try {help_url} '
                f'for a the list of valid collections, or an error message if '
                f'the the namespace "{namespace}" is invalid.',
                url, namespace, collection)
        if msg == 'Bad request syntax.':
            raise BadRequestSyntaxError(
                'An error occurred in the auraxium.census URL generator. '
                'Please report this error at '
                'https://github.com/leonhard-s/auraxium/issues', url)
        if msg == 'service_unavailable':
            raise ServiceUnavailableError(
                'This component of the API is currently unavailable. '
                'Try again later.', url)
        if str(msg).startswith('Provided Service ID is not registered.'):
            raise InvalidServiceIDError(
                'The service ID specified is unknown. Check your spelling '
                'or wait for the email response validating your service ID.',
                url)
        if str(msg).startswith('Missing Service ID.'):
            raise MissingServiceIDError(
                'The default service ID "s:example" is for casual use only. '
                'Wait 60 seconds or apply for your own service ID at '
                'http://census.daybreakgames.com/#devSignup', url)
    # Collection field and query command parsing
    if (code := data.get('errorCode')) is not None:
        if (msg := data.get('errorMessage')) is not None:
            if code == 'SERVER_ERROR':
                if str(msg).startswith('INVALID_SEARCH_TERM'):
                    _process_invalid_search_term(str(msg), url)
                raise ServerError(
                    f'Error code: "{code}", error message: "{msg}"', url)
        if code == 'SERVER_ERROR':
            # NOTE: There are at least two circumstances under which there is
            # no message associated with a server error:
            # 1. An empty request (i.e. https://census.daybreakgames.com/get/)
            # 2. Not providing any arguments to ps2/event
            raise ServerError('Unknown server error', url)
        # Fallback for new and exciting error codes
        raise CensusError(
            f'An unknown error code was encountered: {code}', url)


def _process_invalid_search_term(msg: str, url: yarl.URL) -> None:
    """Parse "INVALID_SEARCH_TERM" error messages.

    This reformats the error message and tries to return a more helpful
    error message through URL introspection.

    This method will return if it cannot provide a specific error.

    Arguments:
        msg: The error message received.
        url: The URL that resulted in the current error.

    Raises:
        InvalidSearchTermError: Raised for bad field names or values

    """
    # Process the URL to provide more helpful errors
    *_, namespace, collection = url.parts
    # Shorter version of the message, with "INVALID_SEARCH_TERM: " chopped off
    chopped = msg[21:].strip()
    # Invalid field name
    if chopped.startswith('Invalid search term. Valid search terms:'):
        # Retrieve the list of valid field names from the error message
        fields_str = chopped.split(':', maxsplit=1)[1].strip()
        fields: List[str] = [f.strip() for f in fields_str[1:-1].split(',')]
        # Parse the query string to find the faulty field name
        culprit: Optional[str] = None
        for field, value in url.query.items():
            if field not in fields:
                culprit = field
                break
        # Tweak the error message depending on whether a culprit was found
        field_info = 'field' if culprit is None else f'"{culprit}"'
        raise InvalidSearchTermError(
            f'Invalid {field_info} for collection '
            f'"{namespace}/{collection}". Valid field names: {fields}',
            url, namespace, collection, culprit)
    # Invalid field value
    if chopped.startswith('Invalid search term:'):
        field = chopped.split(':', maxsplit=1)[1].split()[0][:-1]
        value = url.query[field]
        raise InvalidSearchTermError(
            f'Invalid value "{value}" for field "{field}" of collection '
            f'"{namespace}/{collection}".', url, namespace, collection, field)
    # Invalid RegEx value
    if chopped.startswith('Invalid search value for term:'):
        field = chopped.split(':', maxsplit=1)[1].split()[0][:-1]
        value = url.query[field]
        raise InvalidSearchTermError(
            f'Invalid value "{value}" for field "{field}" of collection '
            f'"{namespace}/{collection}". At least three characters must be '
            'provided in addition to the RegEx flag.',
            url, namespace, collection, field)
    # No valid terms in show/hide fields
    if chopped.startswith('c:show or c:hide resulted'):
        method = 'show' if 'c:show' in str(url) else 'hide'
        raise InvalidSearchTermError(
            f'Invalid field names specified for QueryBase.{method}().',
            url, namespace, collection, f'c:{method}')


async def run_query(query: Query, session: aiohttp.ClientSession,
                    verb: str = 'get') -> CensusData:
    """Perform a top-level Query using the provided HTTP session.

    This will handle check both the HTTP response and JSON contents for
    errors before returning.

    Refer to the :meth:`raise_for_dict()` method for details on the
    exceptions raised.

    Arguments:
        query: The query to run.
        session: The session to use for the request.
        verb (optional): The query verb to pass. Defaults to ``'get'``.

    Raises:
        ResponseError: Raised if the HTTP response contained error
            codes or could not be parsed.

    Returns:
        The response dictionary received.

    """
    url = query.url(verb=verb)
    _log.debug('Performing %s request: %s', verb.upper(), url)

    def on_success(details: Dict[str, Any]) -> None:
        """Called when a query is successful."""
        if (tries := details['tries']) > 1:
            _log.debug('Query successful after %d tries: %s',
                       tries, url)

    def on_backoff(details: Dict[str, Any]) -> None:
        """Called when a query failed and is backed off."""
        wait = details['wait']
        tries = details['tries']
        _log.debug('Backing off %.2f seconds after %d attempts: %s',
                   wait, tries, url)

    def on_giveup(details: Dict[str, Any]) -> None:
        """Called when giving up on a query."""
        elapsed: float = details['elapsed']
        tries: int = details['tries']
        _log.warning('Giving up on query and re-raising exception after %.2f '
                     'seconds and %d attempts: %s', elapsed, tries, url)
        _, exc_value, _ = sys.exc_info()
        assert exc_value is not None
        raise exc_value

    # The following exceptions will be retried if occurring during the request
    backoff_errors = (
        aiohttp.ClientResponseError,
        aiohttp.ClientConnectionError,
        MaintenanceError)
    # Backoff timeout generator
    backoff_gen: Iterator[float] = backoff.expo(  # type: ignore
        base=10, factor=0.001, max_value=5.0)

    @backoff.on_exception(  # type: ignore
        lambda: backoff_gen, backoff_errors, on_backoff=on_backoff,
        on_giveup=on_giveup, on_success=on_success, max_tries=5, jitter=None)
    async def retry_query() -> aiohttp.ClientResponse:
        """Request handling wrapper."""
        response = await session.get(
            url, allow_redirects=False, raise_for_status=True)
        # Trigger MaintenanceErrors from redirect response. This will also be
        # caught by the backoff decorator and will only reach the user if the
        # logic in the on_backoff callback re-raises it.
        if 300 <= response.status < 400:
            raise MaintenanceError(
                'API redirection detected, API maintenance inferred',
                url, response)
        return response

    # Check for HTTP errors
    try:
        response = await retry_query()
    except aiohttp.ClientResponseError as err:
        raise ResponseError(
            f'An HTTP exception occurred: {err.args[0]}') from err
    except aiohttp.ClientConnectionError as err:
        # The connection had issues.
        raise ResponseError(
            f'A network exception occurred: {err.args[0]}') from err
    # Convert the HTTP response into a dictionary
    data = await response_to_dict(response)
    # Check the received dictionary for error codes
    raise_for_dict(data, url)
    return data

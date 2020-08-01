"""Request handling utilities for auraxium.

NOTE: This module is an unfinished placeholder and will be largely
replaced.
"""

import logging
from typing import List, Optional

import aiohttp

from .census import Query
from .types import CensusData

__all__ = ['extract_payload', 'extract_single', 'run_query']

log = logging.getLogger('auraxium.ps2')


def extract_payload(data: CensusData, collection: str) -> List[CensusData]:
    """Extract the payload from a census response dictionary.

    This checks for missing keys and catches common API error states.

    Args:
        data: The response dictionary to process.
        collection: The collection name to expect.

    Returns:
        All dictionaries in the response list.

    """
    try:
        list_: List[CensusData] = data[f'{collection}_list']
    except KeyError as err:
        raise ValueError from err  # TODO: BadPayloadError
    except ValueError as err:
        raise ValueError from err  # TODO: CensusError
    return list_


def extract_single(data: CensusData, collection: str) -> CensusData:
    """Extract the payload from a census response dictionary.

    This checks for missing keys and catches common API error states.

    Args:
        data: The response dictionary to process.
        collection: The collection name to expect.

    Returns:
        The first dictionary returned.

    """
    list_ = extract_payload(data, collection)
    if not list_:
        raise ValueError  # TODO: NotFoundError
    if len(list_) == 1:
        return list_[0]
    raise ValueError  # TODO: CountWarning


def raise_for_dict(data: CensusData) -> None:
    """Raise the appropriate errors for any given census response."""
    if 'error' in data:
        msg: str = data['error']

        if msg == 'No data found.':
            # NOTE: Empty request, invalid namespace, invalid collection
            raise ValueError('No data found error')
        if msg == 'Bad request syntax':
            # NOTE: Malformatted URL, & before ?, etc.
            raise ValueError('Bad request syntax')

    if 'errorCode' in data:
        # code: str = data['errorCode']
        msg = data['errorMessage']

        # raise InvalidSearchTermError(msg.split('.')[1])
        raise ValueError('Invalid search term. ' + msg.split('.')[1])


async def run_query(query: Query, verb: str = 'get',
                    session: Optional[aiohttp.ClientSession] = None
                    ) -> CensusData:
    """Perform a Census API query using aiohttp.

    This also handles and HTTP-related errors.

    Args:
        query: The query to run.
        verb (optional): The query verb to use. Defaults to 'get'.
        session (optional): The session to use for the request.
            Defaults to None.

    Returns:
        The response dictionary received.

    """
    close_session = session is None
    session = session or aiohttp.ClientSession()
    url = query.url(verb=verb)
    log.debug('Performing %s request: %s', verb.upper(), url)
    try:
        async with session.get(url, raise_for_status=True) as response:
            data: CensusData = await response.json()
    except aiohttp.ContentTypeError as err:
        # The API returned a non-JSON response; something went wrong
        raise err
    except aiohttp.ClientResponseError as err:
        # The response was not valid or the status code malformed.
        raise err
    finally:
        if close_session:
            await session.close()
    raise_for_dict(data)
    return data

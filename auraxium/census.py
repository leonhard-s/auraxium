import datetime
import enum
from typing import Any, Dict, List
import requests
from .exceptions import (InvalidSearchTermError, RegExTooShortError,
                         UnknownCollectionError)
from .log import logger
from .type import CensusValue


class SearchModifier(enum.Enum):
    """Enumerates the search modifiers available for Term objects.

    Note that a search modifier may not be valid for all field types.
    """

    # TODO: Do some testing what happens with certain combinations, i.e. could
    # one use the "less_than" option to filter characters alphabetically, etc.

    EQUAL_TO = 0
    NOT_EQUAL_TO = 1
    LESS_THAN = 2
    LESS_THAN_OR_EQUAL = 3
    GREATER_THAN = 4
    GREATER_THAN_OR_EQUAL = 5
    STARTS_WITH = 6
    CONTAINS = 7


class Term():
    """A term or condition for a query or join."""

    def __init__(self, field: str, value: CensusValue,
                 modifier: SearchModifier = SearchModifier.EQUAL_TO) -> None:
        """Initializer."""
        self.field = field
        self.modifier = modifier
        self.value = value

    def to_url(self) -> str:
        """Return the URL representation of this Term."""
        # This list is used to convert the enum value into a string
        MODIFIER_LIST: List[str] = ['', '!', '<', '[', '>', ']', '^', '*']
        modifier = '=' + MODIFIER_LIST[self.modifier.value]
        return self.field + modifier + _value_to_str(self.value)


def retrieve(url: str, convert: bool) -> Dict[str, Any]:
    """Retrieve the server's response for a given URL."""
    logger.debug(f'Performing request: {url}')
    # Get response
    response = requests.get(url)
    # Raise HTTP-related errors
    response.raise_for_status()
    data = response.json()
    # Object-oriented error handling
    _raise_for_data(data)
    # Return count info
    return_count: int = data.pop('returned', -1)
    logger.debug(f'Returned {return_count} entries.')
    # Timing info
    timing: Dict[str, Any] = data.pop('timing', {})
    if timing:
        timing_list = [k[:-3] + ': ' + str(timing[k]) + ' ms' for k in timing]
        logger.debug(f'Timing: {", ".join(timing_list)}')
    # If there are any addional keys, log a warning
    if len(data) > 1:
        logger.warning(f'Unexpected number of keys: {data}')
    # If data type conversion is enabled, process it
    if convert:
        data = _convert_dict(data)
    # Return the remaining response
    return data


def _convert_dict(data: Dict[str, Any], human_date: bool = False) -> Dict[str, Any]:
    """Process a dictionary to be closer to a standard Python one."""
    new_dict: Dict[str, Any] = {}
    value: CensusValue
    for k, v in data.items():
        v: Any
        # Skip the human-readable "*_date" key if the normal timecode exists
        if k[-5:] == '_date' and k[:-5] in data.keys() and not human_date:
            logger.debug(f'Skipped key "{k}" while processing')
            continue
        elif k == 'date' and 'time' in data.keys() and not human_date:
            logger.debug(f'Skipped key "{k}" while processing')
            continue
        # Check if the value is a number
        try:
            value = float(v)
            # Check if the value is an integer
            if value.is_integer():
                value = int(value)
                # If the "*_date" key exists, it must be a timestamp
                if f'{k}_date' in data.keys():
                    value = datetime.datetime.utcfromtimestamp(value)
                elif k == 'time' and 'date' in data.keys():
                    value = datetime.datetime.utcfromtimestamp(value)
            new_dict[k] = value
        except ValueError:
            # Raised for strings
            if v == 'NULL':
                new_dict[k] = None
            # NOTE: The value is already a string, no conversion needed
            new_dict[k] = v
        except TypeError:
            # Raised for lists and sub-dictionaries
            if isinstance(v, list):
                new_dict[k] = [_convert_dict(x, human_date) for x in v]
                continue
            new_dict[k] = _convert_dict(v, human_date)
    return new_dict


def _raise_for_data(data: Dict[str, Any]) -> None:
    """Raise errors according to the keys found in the data."""
    # No data found error
    if data.get('error', '') == 'No data found.':
        msg = 'Attempted to access a collection that does not exist.'
        raise UnknownCollectionError(msg)
    # Server-side errors
    if data.get('errorCode', '') == 'SERVER_ERROR':
        message_words: List[str] = data['errorMessage'].split(': ', 2)
        # Invalid search term
        if message_words[1][1:].startswith('Invalid search term.'):
            msg = 'Attempted to query a collection by an invalid field.'
            raise InvalidSearchTermError(msg)
        # Invalid search value
        elif message_words[1][1:].startswith('Invalid search value'):
            msg = 'RegEx queries must have at least 3 characters.'
            raise RegExTooShortError(msg)


def _value_to_str(value: CensusValue) -> str:
    """Convert any CensusValues into the proper string format."""
    # Datetimes must be converted to integer POSIX timestamps
    if (isinstance(value, datetime.datetime)):
        return str(int(value.timestamp()))
    return str(value)

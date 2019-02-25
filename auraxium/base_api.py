"""Core components of the API wrapper."""

import json
import logging
from typing import Dict, List, Optional, Tuple, Union
from urllib import parse

import requests

from .exceptions import InvalidSearchTermError, RegExTooShortError, UnknownCollectionError
from .constants import CENSUS_ENDPOINT
from .types import Term

# Create a logger
logger = logging.getLogger('auraxium.query')  # pylint: disable=invalid-name


class Query():  # pylint: disable=too-many-public-methods
    """Represents a query to be made to the API server."""

    def __init__(self, collection: str, namespace: str = 'ps2', **kwargs: Tuple[str, str]) -> None:
        self.collection: str = collection
        self._flags: Dict[str, Union[str, int, float]] = {}
        self._qc_joins: List[Join] = []
        self._qc_keys: Dict[str, list] = {}
        self._qc_tree: Optional[str] = None
        self.namespace: str = namespace

        # Turn kwargs into named field/value pairs and store them in self.terms
        self._terms: List[Term] = [Term(k.replace('__', '.'), kwargs[k]) for k in kwargs]

    def case(self, check_case: bool):
        """Toggles case-sensitive string matches for this query.

        Query command.

        Queries are case-sensitive by default. The query object is
        returned to allow for chaining of query commands.

        Keep in mind that using case-insensitive searches is not
        advisable as it greatly slows down the query.
        Commonly searched fields, such as player or outfit names, also
        contain a lowercase version that can be used to get this
        functionality without sacraficing speed.

        """

        if check_case:
            # Case-sensitive searches are the default option, hence why the entry is just removed
            self._flags.pop('case', None)
        else:
            self._flags['case'] = 'false'
        return self

    def count(self, url_only=False) -> Union[int, str]:
        """Returns the number of matching items."""
        url: str = self.generate_url(verb='count')

        # In URL mode, only return the URL generated
        if url_only:
            return str(url)

        return int(retrieve(url, count=True))

    def distinct(self, field: str) -> 'Query':
        """Returns the distinct values for a given field.

        Query command.

        Results are capped to 20,000 results. The query object is
        returned to allow for chaining of query commands.

        """

        if field is None:
            self._qc_keys.pop('distinct', None)
        else:
            self._qc_keys['distinct'] = [str(field)]
        return self

    def exact_match_first(self, enable: bool) -> 'Query':
        """Return exact matches first when using RegEx search modes.

        Query command.

        When using RegEx searches like `=^value`("starts with") or
        `=*value` ("contains"), enabling this setting will make sure
        an exact match is always at the top of the results list.

        This overrides any sorting behaviour specified. The query
        object is returned to allow for chaining of query commands.

        """

        if enable:
            self._flags['exactMatchFirst'] = 'true'
        else:
            # False is the default option, hence why the key is removed instead
            self._flags.pop('exactMatchFirst', None)
        return self

    def generate_url(self, verb: str) -> str:
        """Generates the URL representing this query."""
        from . import service_id

        # Input checking
        if verb not in ['count', 'get']:
            # NOTE: While it makes little sense to use the string representations of the verbs,
            # using an Enum would make even less sense... optimization is welcome!
            raise ValueError('The only supported verbs are "count" and "get"')

        # Warn the user if they are using the default service id
        if service_id == 's:example':
            logger.warning('The default service id is bandwidth-limited. It is recommended to '
                           'apply for your own at (http://census.daybreakgames.com/#devSignup).')

        # Create a list of the core URL components to concatenate
        elements = [CENSUS_ENDPOINT, service_id, verb, self.namespace]

        # If the collection is not specified, the query is used to show the collections available
        # for the given namespace.
        if self.collection is None:
            return '/'.join(elements)

        # If the collection is not empty, add the collection to the list of elements to concatenate
        elements.append(self.collection)
        url = '/'.join(elements)

        # Add query search terms
        item_list = [str(term.field) + '=' + parse.quote_plus(str(term.value))
                     for term in self._terms]

        # Process flag-type query commands
        item_list.extend(['c:' + c + '=' + str(self._flags[c])
                          for c in self._flags])
        # Process key-type query commands
        item_list.extend(['c:' + c + '=' + ','.join([str(i) for i in self._qc_keys[c]])
                          for c in self._qc_keys])  # Process the tree query command (if it exists)

        if self._qc_tree is not None:
            item_list.append(self._qc_tree)
        # Process any join query commands
        if self._qc_joins:
            item_list.append(_process_joins(*self._qc_joins))

        # Finalize and return the URL
        if item_list:
            url += '?'
        url += '&'.join(item_list)

        return url

    def get(self, single=False, url_only: bool = False) -> Union[str, dict]:
        """Perform the API query defined by the Query object."""

        url: str = self.generate_url(verb='get')

        if url_only:
            return url

        if single:
            return retrieve(url)[0]
        return retrieve(url)

    def has(self, field: str, *args: str) -> 'Query':
        """Only return results with a non-Null values for these fields.

        Query command.

        Useful for filtering common collections based on the fields
        that are populated. Example: Only weapons using a heat mechanic
        will have values for the corresponding fields.

        The query object is returned to allow for chaining of query
        commands.

        """

        if field is None:
            self._qc_keys.pop('has', None)
        else:
            self._qc_keys['has'] = [field]
            self._qc_keys['has'].extend(args)
        return self

    def hide(self, field: str, *args: str) -> 'Query':
        """Hides the specified fields from the response.

        Query command.

        This command will only take effect if the "show" command has
        not been used. The query object is returned to allow for
        chaining of query commands.

        """

        if field is None:
            self._qc_keys.pop('hide', None)
        else:
            self._qc_keys['hide'] = [field]
            self._qc_keys['hide'].extend(args)
        return self

    def include_null(self, enable: bool) -> 'Query':
        """Includes NULL value fields in the response.

        Query command.

        Useful for finding out which fields exist for a given
        collection. The query object is returned to allow for chaining
        of query commands.

        """

        if enable:
            self._flags['includeNull'] = 'true'
        else:
            # False is the default option
            self._flags.pop('includeNull', None)
        return self

    def join(self, *args, **kwargs) -> 'Join':
        """Creates an inner (or joined) query.

        All arguments passed to this function are forwarded to the new
        Join object's `__init__` method, see it for details.

        """

        new_join = Join(*args, **kwargs)
        self._qc_joins.append(new_join)
        return new_join

    def lang(self, locale: str) -> 'Query':
        """If set, only fields for the given locale will be returned.

        Query command.

        Accepted locales are "de", "en", "es", "fre" and "tr". The "tr"
        locale is technically supported, but only populated for a small
        number of fields.

        The query object is returned to allow for chaining of query
        commands.

        """

        if locale is None:
            self._qc_keys.pop('lang', None)
        if locale not in ['de', 'en', 'es', 'fr', 'it', 'tr']:
            raise ValueError('The locale specified is invalid.')
        else:
            self._qc_keys['lang'] = [str(locale)]
        return self

    def limit(self, results: int) -> 'Query':
        """Limits the number of results returned. Defaults to 1.

        Query command.

        When the expected number of results is unknown, it is advisable
        to first run a "count" query to determine the number of results
        expected.

        The query object is returned to allow for chaining of query
        commands.

        """

        if results is None or results == 1:
            self._qc_keys.pop('limit', None)
        elif results < 1:
            raise ValueError(
                'Can\'t limit the results to a number smaller than 1')
        else:
            self._qc_keys['limit'] = [int(results)]
        return self

    def limit_per_db(self, results: int) -> 'Query':
        """Limits the number of results returned. Defaults to 1.

        Query command.

        The "character" collection is distributed randomly across 20
        databases. Using `limit_per_db` might have more predictable
        results than using `limit`.

        The query object is returned to allow for chaining of query
        commands.

        """

        if results is None:
            self._qc_keys.pop('limitPerDB', None)
        elif results < 1:
            raise ValueError(
                'Can\'t limit the results to a number smaller than 1')
        else:
            self._qc_keys['limitPerDB'] = [int(results)]
        return self

    def resolve(self, field: str, *args: str) -> 'Query':
        """Resolves one or more resolvable fields.

        Query command.

        Returning the list of collections for a namespace also returns
        the resolve lists for that collection. If you require a link
        between two collections that are not directly resolvable, use
        the `join` command instead.

        The query object is returned to allow for chaining of query
        commands.

        """

        if field is None:
            self._qc_keys.pop('resolve', None)
        else:
            self._qc_keys['resolve'] = [field]
            self._qc_keys['resolve'].extend(args)
        return self

    def retry(self, enable: bool) -> 'Query':
        """If set to false, results will not be retried before failing.

        Query command.

        By default, queries are retried once before failing. Depending
        on the use-case, it might be preferable to have queries fail
        quickly.

        The query object is returned to allow for chaining of query
        commands.

        """

        if enable:
            # "True" is the default option
            self._flags.pop('retry', None)
        else:
            self._flags['retry'] = 'false'
        return self

    def show(self, field: str, *args: str) -> 'Query':
        """Only include the field names specified in the response.

        Query command.

        This command will override the `hide` command. Be sure to only
        use one or the other to prevent unexpected behavior.

        The query object is returned to allow for chaining of query
        commands.

        """

        if field is None:
            self._qc_keys.pop('show', None)
        else:
            self._qc_keys['show'] = [field]
            self._qc_keys['show'].extend(args)
        return self

    def sort(self, field: str, *args: str) -> 'Query':
        """Allows sorting the results returned by one or more fields.

        Query command.

        Append `:-1` to a field to sort by descending order. The query
        object is returned to allow for chaining of query commands.

        """

        if field is None:
            self._qc_keys.pop('sort', None)
        else:
            self._qc_keys['sort'] = [field]
            self._qc_keys['sort'].extend(args)
        return self

    def start(self, offset: int) -> 'Query':
        """Skips the first <offset> results in the response.

        Query command.

        When combined with `limit`, this can be used for creating a
        page view for a large collection.

        The query object is returned to allow for chaining of query
        commands.

        """

        if offset is None or offset == 0:
            self._qc_keys.pop('start', None)
        elif offset < 0:
            raise ValueError('The starting offset can\'t be negative.')
        else:
            self._qc_keys['start'] = [int(offset)]
        return self

    def timing(self, enable: bool) -> 'Query':
        """Enables timing output in the response.

        Query command.

        If enabled, timing information will be included in the
        response. The query object is returned to allow for chaining
        of query commands.

        """

        if enable:
            self._flags['timing'] = 'true'
        else:
            # False is the default option
            self._flags.pop('timing', None)
        return self

    def tree(self, field: str, is_list: bool = False,
             prefix: str = '', start: Optional[int] = None) -> 'Query':
        """Restructures the results returned into a tree view.

        Query command.

        Causes the results returned to be formatted as a tree view.

        "field" is the field used for generating the tree view.
        "list" causes items to be grouped into lists
        "prefix" will be prefixed to the field values
        "start" is the name of the field where the tree view will start

        The query object is returned to allow for chaining of query
        commands.

        """

        self._qc_tree = 'c:tree=' + field
        if is_list:
            self._qc_tree += '^list:1'
        if prefix != '':
            self._qc_tree += '^prefix:' + prefix
        if start is not None and start < 0:
            raise ValueError('The starting offset must be greater than 0.')
        elif start is not None and start > 0:
            self._qc_tree += '^start:' + str(start)
        return self


class Join():
    """Represents an inner (or joined) query.

    Created by the `auraxium.Query.join()` and `Join.join()` methods.

    Note regarding the `on` and `to` arguments:
    The sentence to remember is "I want to match the value of the field
    `on the parent` `<to> the one of the child`.

    """

    def __init__(self, collection: str, inject_at: Optional[str] = None,
                 on: Optional[str] = None, to: Optional[str] = None, **kwargs) -> None:
        self.collection: str = collection
        self._hide: List[str] = []
        self._inner_joins: List['Join'] = []
        self._show: List[str] = []
        self._flags: Dict[str, str] = {}
        self._keys: Dict[str, Optional[str]] = {'inject_at': inject_at, 'on': on, 'to': to}

        # Turn kwargs into named field/value pairs and store them in self.terms
        self._terms: List[Term] = [Term(k.replace('__', '.'), kwargs[k]) for k in kwargs]

    def hide(self, *args: str) -> 'Join':
        """Identical to the `hide` query command.

        Note that the field used to link joins may be hidden for the
        item that was joined, but it must be included for the parent.

        The join object is returned to allow for chaining.

        """
        self._hide = [*args]
        return self

    def is_list(self, is_list: bool) -> 'Join':
        """Set this flag if this join is expected to return a list.

        Defaults to False, not a list.

        The join object is returned to allow for chaining.

        """

        if is_list:
            self._flags['list'] = '1'
        else:
            # Default option
            self._flags.pop('list', None)
        return self

    def is_outer_join(self, is_outer_join: bool) -> 'Join':
        """Flags the current join as an outer join.

        An outer join will also include non-matching items, an inner
        join will only include matching items. Joins are outer joins
        by default.

        The join object is returned to allow for chaining.

        """

        if is_outer_join:
            # Default option
            self._flags.pop('outer', None)
        else:
            self._flags['outer'] = '0'
        return self

    def join(self, *args, **kwargs) -> 'Join':
        """Creates an inner join for this join.

        All arguments passed to this function are forwarded to the new
        Join object's `__init__` method, see it for details.

        The created join is returned for further nesting.

        """

        inner_join = Join(*args, **kwargs)
        self._inner_joins.append(inner_join)
        return inner_join

    def process(self) -> str:
        """Process the join and return its string representation.

        Processes the Join object's contents and generates the string
        representation for it. Also recurses over any inner joins and
        procceses them, you therefore only need to run this method for
        top-level joins.

        """

        # The collection or type of the join
        string = self.collection

        # Process flags ('list' and 'outer')
        if self._flags:
            string += '^' + \
                '^'.join(f + ':' + self._flags[f] for f in self._flags)

        # Process keys ('inject_at', 'on' and 'to')
        for k in self._keys:
            if self._keys[k] is not None:
                string += '^' + k + ':' + str(self._keys[k])

        # Process 'show' and 'hide' lists
        if self._show:
            string += '^show:' + '\''.join(self._show)
        elif self._hide:
            string += '^hide:' + '\''.join(self._hide)

        # Process terms
        if self._terms:
            string += '^terms:' + \
                '\''.join([t.field + '=' + t.value for t in self._terms])

        # Process inner joins
        string += ''.join(['(' + j.process() + ')' for j in self._inner_joins])

        return string

    def show(self, *args: str) -> 'Join':
        """Identical to the `show` query command.

        Note that the field used to link joins may be hidden for the
        item that was joined, but it must be included for the parent.

        The join object is returned to allow for chaining.

        """
        self._show = [*args]
        return self


def _process_joins(*args: 'Join') -> str:
    """Processes all joins in the list.

    A warning will be raised if more than one argument is passed as
    this is still untested due to a lack of known use-cases.

    """

    if len(args) > 1:
        logger.warning('Multiple top-level joins are not yet supported. Expect erroneous '
                       'behaviour and let the wrapper devs know of your use-case. Thanks!')
    return 'c:join=' + ','.join([join.process() for join in args])


def retrieve(url, count: bool = False) -> Union[dict, int]:
    """Retrieves the object using the URL given."""
    # Log the request's URL in case an error occurs
    logger.debug('Performing request: %s', url)
    data = json.loads(requests.get(url).text)

    try:
        # Log the number of results returned
        if count:
            results = data.pop('count')
            # Return the number of results
            return int(results)

    except KeyError as err:

        # Unknown collection
        try:
            if data['error'] == 'No data found.':
                raise UnknownCollectionError('Attempted to access a collection that does not '
                                             'exist.') from err
            else:
                raise err
        except KeyError:
            pass

        # Invalid search term
        try:
            if data['errorCode'] == 'SERVER_ERROR':
                message_words = data['errorMessage'].split(': ', 2)

                # Invalid search term
                if message_words[0] == 'INVALID_SEARCH_TERM':

                    # Invalid field name
                    if message_words[1][1:].startswith('Invalid search term.'):
                        raise InvalidSearchTermError('Attempted to query a collection by an '
                                                     'invalid field name.') from err

                    if message_words[1][1:].startswith('Invalid search value'):
                        raise RegExTooShortError('Unable to perform RegEx query: RegEx queries '
                                                 'must have at least 3 characters.') from err

        except KeyError:
            pass

        # Fallback
        raise err

    results = data.pop('returned')
    logger.debug('Found %s results', results)

    # If timing data has been provided, log it
    timing = data.pop('timing', {})
    if timing:
        timing_list = [k[:-3] + ': ' + str(timing[k]) + ' ms' for k in timing]
        logger.debug('Timing: %s', ', '.join(timing_list))

    # If there is more than one key leftover, raise an alarm bell
    if len(data) > 1:
        logger.warning('Unexpcted number of keys: %s', data)

    # Return the remaining key
    return data[list(data.keys())[0]]

import json
import logging
from enum import Enum

import requests

from .exceptions import (APILimitationError, ServiceIDMissingError,
                         ServiceIDUnknownError, ServiceUnavailableError)

# Create a logger
logger = logging.getLogger('auraxium.census')

# The endpoint used for all Census API requests.
_CENSUS_BASE_URL = 'http://census.daybreakgames.com/'
# The PlanetSide 2 (PC) namespace. No PS4 support yet.
_NAMESPACE = 'ps2'
# The id used to identify this service.
service_id = 's:example'
# The default locale to use when no other is specified.
default_locale = 'en'
# Forces all Querys to provide timing information.
timing_override = True


class SearchModifier(Enum):
    """Enumerates the search modifiers available to Querys and Joins.

    Attributes
    ----------
    EQUAL_TO
        Only return exact matches.
    CONTAINS
        Matches strings containing the given string.
    GREATER_THAN
        Matches numbers larger than the one given.
    GREATER_OR_EQUAL
        Matches numbers larger than or equal to the one given.
    LESS_THAN
        Matches numbers less than the one given.
    LESS_OR_EQUAL
        Matches numbers less than or equal to the one given.
    STARTS_WITH
        Matches strings starting with the given string.
    NOT_EQUAL_TO
        Matches anything except exact matches.

    """

    EQUAL_TO = 1
    CONTAINS = 2
    GREATER_THAN = 3
    GREATER_OR_EQUAL = 4
    LESS_THAN = 5
    LESS_OR_EQUAL = 6
    STARTS_WITH = 7
    NOT_EQUAL_TO = 8


class FilterTerm(object):
    """A filter term used to reduce the amount of data returned.


    Parameters
    ----------
    field : str
        The name of the field to filter by.
    value : str
        The value to filter by
    modifier : auraxium.SearchModifier
        Allows filtering by magnitude or other, non-exact matches.

    Attributes
    ----------
    field
    modifier
    value

    """

    def __init__(self, field, value, modifier=SearchModifier.EQUAL_TO):
        self.field = field
        self.modifier = modifier
        self.value = value

    def __str__(self):
        """Converts the FilterTerm into a string.

        Converts the FilterTerm object into its string representation, following the
        syntax laid out by the Census API.

        Returns
        -------
        str
            The string representation of the term.

        """
        # This list contains the string representations of the search modifiers in
        # the order they have been defined in the SearchModifier enum:
        MODIFIERS = ['=', '=*', '=>', '=]', '=<', '=[', '=^', '=!']
        return self.field + MODIFIERS[self.modifier.value - 1] + str(self.value)


class Join(object):
    """An inner (joined) query used for advanced requests.

    Joins can be created using the auraxium.Query.join() method. They can
    also be nested using the auraxium.Join.join() method.

    Parameters
    ----------
    type : auraxium.CensusBaseClass
        The data type the inner query will access.
    is_list : Boolean
        Signals whether the data returned is expected to be a list. False by
        default.
    match : str
        The field on the joined data type to match with its parent.
    match_parent : str
        The field on the parent data type to match with its child. Will be set
        to equal `match` if unset.
    name : str
        Allows overriding of the name of the field the joined query's results
        be placed in.
    is_outer_join : Boolean
        Whether the result should include non-matches. True by default.

    Attributes
    ----------
    _filter_terms : list of auraxium.FilterTerm
        A list of terms to filter the result by.
    _hide : list of str
        A list of fields to exclude from the response. Only used if the `_show`
        attribute is empty.
    joins : list of auraxium.Join
        A list of Joins nested inside this one.
    _show : list of str
        If this list is not empty, only fields specified herein will be
        included in the response.
    type
    is_list
    name
    is_outer_join
    match
    match_parent

    """

    def __init__(self, type, is_list=False, match=None,
                 match_parent=None, name=None, is_outer_join=True):
        self.type = type
        self._filter_terms = []
        self._hide = []
        self.is_list = is_list
        self.is_outer_join = is_outer_join
        self.joins = []
        self.name = name
        self.match = match if match != None else type._collection + '_id'
        self.match_parent = match_parent if match_parent != None else self.match
        self._show = []

    def __str__(self):
        """Converts the Join object into its string representation.

        This string representation follows the Census API syntax and can be
        used in URLs.

        Returns
        -------
        str
            The string representation of the Join.

        """

        s = 'type:'.format(self.type._collection)
        if self.match != None:
            s += '^on:{}'.format(self.match)
        if self.match_parent != None:
            s += '^to:{}'.format(self.match_parent)
        if self.is_list:
            s += '^list:1'
        if not self.is_outer_join:
            s += '^outer:0'

        if len(self._show) > 0:
            s += '^show:{}'.format('\''.join(self._show))
        elif len(self._hide) > 0:
            s += '^hide:{}'.format('\''.join(self._hide))
        s += '^inject_at:'
        if not self.name == None:
            s += self.name
        else:
            s += self.type._collection
            if self.is_list:
                s += '_list'
        if len(self._filter_terms) > 0:
            s += '^terms:'
            for term in self._filter_terms:
                s += '{}\''.format(str(term))
            s = s[:-1]  # Remove the final '-separator
        if len(self.joins) > 0:
            # Enter another level of join-ception
            s += '('
            # Loop through all inner joins
            for join in self.joins:
                # TODO: If there is more than one nested join at the same
                # "depth", this is likely to cause some issues. I was unable to
                # do any testing on this yet as I couldn't find a use-case that
                # requires this.
                s += str(join)
            s += ')'
        return s

    def join(self, type, **kwargs):
        """Creates a new Join for this join.

        Creates a new Join object and appends it to the parent Join's `joins`
        list. The created Join is also returned to allow for further nesting.

        Parameters
        ----------
        type : auraxium.CensusBaseClass
            The data type the inner query will access.
        **kwargs
            Any `**kwargs` passed to this function will be forwarded to the
            Join object's `__init` method. See it for instructions.

        Returns
        -------
        auraxium.Join
            The Join created by the method.

        """

        join = Join(type, **kwargs)
        self.joins.append(join)
        return join


class Query(object):
    """Represents a request to be sent to the Census API servers.

    After creation, a request may be filtered or joined to. A request does not
    generate network traffic until the `auraxium.Query.count()` or
    `auraxium.Query.get()` methods are called.

    Parameters
    ----------
    type : auraxium.CensusBaseClass
        The data type to search.
    check_case : Boolean
        Whether to check for case when matching strings. True by default.
    distinct_values : list of str
        Lists fields to retrieve the distinct values for.
    exact_match_first : Boolean
        Forces exact matches to be first in the list when using non-exact
        matches like `SearchModifier.STARTS_WITH` or `SearchModifier.CONTAINS`.
        Overrides any other sorting behaviour. False by default.
    include_empty : Boolean
        Whether to include empty fields in the response. False by default.
    locale : str
        Allows specifying the language to retrieve for localized strings.
    limit : int
        The number of items to retrieve.
    limit_per_db : int
        The `characers` collection's entries are distributed randomly across
        20 databases. Using `limit_per_db` might have more predictable results
        than `limit`.
    retry : Boolean
        If true, failed queries will be repeated once before giving up. Set to
        False if you prefer your queries fail quickly. True by default.
    offset : int
        Skips the first N results. When combined with `limit`, can be useful
        for per-page viewing of large datasets. 0 by default.
    timing : Boolean
        Whether to include profiling information in the response. False by
        default.

    Attributes
    ----------
    _filter_terms : list of auraxium.FilterTerm
        A list of FilterTerm objects to apply to the query. Filter terms are
        used to filter the amount of data returned from a query.
    _has_fields : NYI
        (Not yet implemented)
    _hide : list of str
        A list of fields to ommit from the response. Only used if the `_show`
        list is empty.
    joins : list of auraxium.Join
        A list of queries that have been joined to this one. See the
        `auraxium.Join` object for details.
    _show : list of str
        If not empty, only fields in this list will be included in the
        response.
    _sort_by : NYI
        (Not yet implemented)
    _tree : NYI
        (Not yet implemented)
    check_case
    distinct_values
    exact_match_first
    include_empty
    locale
    limit
    limit_per_db
    retry
    offset
    type
    timing

    """

    def __init__(self, type, check_case=True, distinct_values=None,
                 exact_match_first=False, id=None, include_empty=False, locale=None,
                 limit=None, limit_per_db=None, retry=True, offset=0,
                 timing=False):
        self.check_case = check_case
        self.distinct_values = distinct_values
        self.exact_match_first = exact_match_first
        self._has_fields = []
        self._hide = []
        self.include_empty = include_empty
        self.locale = default_locale if locale is None else locale
        self.limit = limit
        self.limit_per_db = limit_per_db
        self.joins = []
        self.retry = retry
        self._show = []
        self._sort_by = []
        self.offset = offset
        self._filter_terms = []
        self.timing = timing
        self._tree = []
        self.type = type

        # ID
        if id != None:
            self.add_filter('{}_id'.format(type._collection), id)

    def add_filter(self, *args):
        """Applies a filter term to the query performed.

        Parameters
        ----------
        *args
            All args passed are forwarded to the auraxium.FilterTerm.__init__
            method.

        Returns
        -------
        auraxium.Query
            The request the filter was applied to. Useful for chaining.

        """

        term = FilterTerm(*args)
        self._filter_terms.append(term)
        return self

    def count(self):
        """Performs a count query for the Query.

        Performs the Query and returns the number of matching entries in the
        database. Joined queries are ignored when performing a count query,
        only the primary request is evaluated.

        Returns
        -------
        int
            The number of matching entries in the database.

        """

        r = self._retrieve(verb='count')
        return int(r['count'])

    def _generate_url(self, verb, collection_override=None):
        """Generates a Census API compatible URL respresenting this Query.

        Parameters
        ----------
        verb : str
            Specifies the kind of request to perform. Accepts "count" and
            "get".

        Returns
        -------
        str
            The URL representation of the Query, including Joins.

        """

        collection = self.type._collection if collection_override == None else collection_override

        url = '{}{}/{}/{}/{}'.format(_CENSUS_BASE_URL, service_id, verb,
                                     _NAMESPACE, collection)
        for term in self._filter_terms:
            url += '&{}'.format(str(term))
        if not self.check_case:
            url += '&c:case=false'
            logger.warning('Ignoring case is not advisable for performance '
                           'reasons. Most fields provide a lowercase version '
                           'as well, it is highly recommended you use that '
                           ' instead if you can.')
        if not self.distinct_values == None:
            url += '&c:distinct={}'.format(self.distinct_values)
        if self.exact_match_first:
            url += '&c:exactMatchFirst=true'
        if len(self._has_fields) > 0:
            url += '&c:has={}'.format(','.join(self.has_fields))
        if self.include_empty:
            url += '&c:includeNull=true'
        if self.locale != None:
            url += '&c:lang={}'.format(self.locale)
        elif default_locale != None:
            url += '&c:lang={}'.format(default_locale)
        if self.limit != None and self.limit > 1:
            url += '&c:limit={}'.format(self.limit)
        if self.limit_per_db != None:
            if self.type._collection != 'character':
                logger.warning('The query command "limit_per_db" is only '
                               'usable with the "character" collection. '
                               'Ignoring...')
            else:
                url += '&c:limitPerDb={}'.format(self.limit_per_db)
        if not self.retry:
            url += '&c:retry=false'
        if len(self._sort_by) > 0:
            # TODO: Sort by
            logger.warning('c:sort is not yet implemented. Skipping...')
        if self.offset > 0:
            url += '&c:start={}'.format(self.offset)
        if self.timing or timing_override:
            url += '&c:timing=true'
        if len(self._tree) > 0:
            # TODO: Tree view
            logger.warning('c:tree is not yet implemented. Skipping...')
        if len(self._show) > 0:
            url += '&c:show={}'.format(','.join(self._show))
        elif len(self._hide) > 0:
            url += '&c:hide={}'.format(','.join(self._hide))
        if len(self.joins) > 0:
            url += '&c:join='
            for join in self.joins:
                url += str(join)
        # Replace the first occurrence of "&" with "?" to fix the syntax
        return url.replace('&', '?', 1)

    def get(self):
        """Performs a get query for the Query.

        Performs the Query and returns the number of matching entries as
        specified by the `limit` and `limit_per_db` attributes. Joined queries
        will not provide error messages if they fail, they will just be
        missing.

        Returns
        -------
        list of auraxium.CensusBaseClass
            Returns the list of objects generated from the server's response.

        """

        r = self._retrieve(verb='get')
        return [self.type(input_dict=dict) for dict in r['{}_list'.format(self.type._collection)]]

    def get_single(self):
        """Performs a get query for the Query returning only one item.

        Performs the Query and returns the first matching entry. Joined
        queries will not provide error messages if they fail, they will just be
        missing.

        Returns
        -------
        list of auraxium.CensusBaseClass
            Returns the list of objects generated from the server's response.

        """

        r = self._retrieve(verb='get')
        return r['{}_list'.format(self.type._collection)][0]

    def hide(self, *args):
        # If the input is a list, keep it - if it's not, make it into one
        self._hide = [*args]
        return self

    def join(self, type, **kwargs):
        """Creates a new Join for this Query.

        Creates a new Join object and appends it to the Query's `joins`
        list. The created Join is also returned to allow for nesting.

        Parameters
        ----------
        type : auraxium.CensusBaseClass
            The data type the inner query will access.
        **kwargs
            Any `**kwargs` passed to this function will be forwarded to the
            Join object's `__init` method. See it for instructions.

        Returns
        -------
        auraxium.Join
            The Join created by the method.

        """

        join = Join(type, **kwargs)
        self.joins.append(join)
        return join

    def _retrieve(self, verb, collection_override=None):
        """Performs the Query and retrieves the server's response.

        Parameters
        ----------
        verb : str
            Specifies the kind of request to perform. Accepts "count" and
            "get".

        Raises
        ------
        auraxium.exceptions.ServiceUnavailableError
            Raised when the collection is temporarily unavailable.
        auraxium.exceptions.ServiceIDUnknownError
            Raised if the Service ID used has not claimed.
        auraxium.exceptions.ServiceIDMissingError
            Raised if the Service ID is missing and the default service ID's
            bandwidth limitation has been exceeded.

        Returns
        -------
        dict
            A dict representation of the server's reponse.

        """

        url = self._generate_url(verb, collection_override=collection_override)
        logger.debug('Performing {} request: {}'.format(verb, url))
        r = json.loads(requests.get(url).text)

        # Check for common errors
        if 'error' in r.keys():
            if r['error'] == 'service_unavailable':
                raise ServiceUnavailableError()
            elif r['error'].startswith('Provided Service ID is not'):
                raise ServiceIDUnknownError('The provided Service ID has not '
                                            'been registered.')
            elif r['error'].startswith('Missing Service ID.'):
                raise ServiceIDMissingError('A valid Service ID is required '
                                            'for continued api use. (You can also wait for the end '
                                            'of the cooldown and retry.)')
        # Timing
        if 'timing' in r.keys():
            timing_list = ['{}: {} ms'.format(
                s[:-3], r['timing'][s]) for s in r['timing'].keys()]
            logger.info('Query profiling: ' + ', '.join(timing_list))
        return r

    def show(self, *args):
        # If the input is a list, keep it - if it's not, make it into one
        self._show = [*args]
        return self

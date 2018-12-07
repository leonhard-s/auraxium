import json
from enum import Enum

import requests

from .collections import get_collection
from .exceptions import (APILimitationError, InvalidJoinError,
                         ServiceIDMissingError, ServiceIDUnknownError,
                         ServiceUnavailableError)

# The endpoint used for all Census API requests.
CENSUS_BASE_URL = 'http://census.daybreakgames.com/'
# The Planetside 2 (PC) namespace. No PS4 support yet.
NAMESPACE = 'ps2'

# The id used to identify this service.
service_id = 's:example'


class SearchModifier(Enum):
    EQUAL_TO = 1
    CONTAINS = 2
    GREATER_THAN = 3
    GREATER_OR_EQUAL = 4
    LESS_THAN = 5
    LESS_OR_EQUAL = 6
    STARTS_WITH = 7
    NOT_EQUAL_TO = 8


class Join():
    def __init__(self, collection, hide=[], list=False, match=None,
                 name=None, show=[]):
        self.collection = collection
        self.hide = hide
        self.list = list
        self.joins = []
        self.match_this = match
        self.match_parent = match
        self.name = name
        self.show = show

    def __str__(self):
        """Converts the join into a string"""
        # collection / type
        string = str(self.collection)
        # inject_at
        if self.name == None:
            string += '^inject_at:{}'.format(str(self.collection))
            if self.list:
                string += '_list'
        # list
        if self.list:
            string += '^list:1'
        # on
        if self.match_this != None:
            string += '^on:{}'.format(self.match_this)
        # to
        if self.match_parent != None:
            string += '^to:{}'.format(self.match_parent)
        # # outer
        # if not self.is_outer_join:
        #     string += '^outer:0'
        # # terms
        # if len(self.terms) > 0:
        #     string += '^terms:'
        #     # loop through all filter terms
        #     for term in self.terms:
        #         string += '{}\''.format(evaluate_term(term))
        #     # Slice the final '-separator off
        #     string = string[:-1]

        # show
        if len(self.show) > 0:
            string += '^show:{}'.format('\''.join(turn_into_list(self.show)))
        # hide
        elif len(self.hide) > 0:
            string += '^hide:{}'.format('\''.join(turn_into_list(self.hide)))

        # nested joins
        if len(self.joins) > 0:
            # Enter another level of join-ception
            string += '('
            # Loop through all inner joins
            for join in self.joins:
                string += str(join)
            string += ')'

        # Return the string
        print('[Census] Inner join generated:')
        print(string)
        return string

    def join(self, collection, **kwargs):
        join = Join(collection, **kwargs)
        self.joins.append(join)
        return join


class Request():
    def __init__(self, collection, hide, limit, show, terms, verb):
        self.collection = collection
        self.joins = []
        self.hide = hide
        self.limit = limit
        self.show = show
        self.terms = terms
        self.url = ''
        self.verb = verb
        for term in self.terms:
            if len(term) == 2:
                term['modifier'] = SearchModifier.EQUAL_TO

    def call(self):
        """Retrieves the response for the request.
        If the url does not exist, it is generated beforehand.
        """
        # If the url has not been setgenerate it.
        if self.url == '':
            print('[Census] Generating url...')
            self.generate_url()
        else:
            print('[Census] Using cached URL.')

        # Retrieve the response from the server.
        print('[Census] Retrieving response for the following URL:')
        print(self.url)
        response = json.loads(requests.get(self.url).text)
        print('[Census] Response received:')
        print(response)

        # Check for common errors
        if 'error' in response.keys():
            if response['error'] == 'service_unavailable':
                raise ServiceUnavailableError()
            elif response['error'].startswith('Provided Service ID is not'):
                raise ServiceIDUnknownError()
            elif response['error'].startswith('Missing Service ID.'):
                raise ServiceIDMissingError()
        elif 'count' in response.keys():
            if response['count'] < 0:
                raise APILimitationError('The collection "{}" cannot be '
                                         'enumerated.'.format(self.collection))

        # Return the response
        return response

    def generate_url(self):
        """Generates a DBG url using the object information for the request"""
        # Concatenate the core elements of the URL
        url = '{}{}/{}/{}/{}'.format(CENSUS_BASE_URL,
                                     service_id,
                                     self.verb,
                                     NAMESPACE,
                                     str(self.collection))

        # Terms
        for term in self.terms:
            url += '&{}'.format(evaluate_term(term))

        # Limit
        if self.limit != 20:
            url += '&c:limit={}'.format(self.limit)

        # Show
        if len(self.show) > 0:
            url += '&c:show={}'.format(','.join(self.show))
        # Hide
        elif len(self.hide) > 0:
            url += '&c:hide={}'.format(','.join(self.hide))

        # Joins
        if len(self.joins) > 0:
            url += '&c:join='
            for join in self.joins:
                url += str(join)

        # Replaces the first occurrence of "&" with "?"
        url = url.replace('&', '?', 1)
        print('[Census] URL generated:')
        print(url)
        self.url = url

    def join(self, collection, **kwargs):
        # Make sure the request is using the "get" verb before proceeding
        if not self.verb == 'get':
            raise InvalidJoinError(
                'Joined queries can only be performed with the verb "get". '
                'This request has the verb "{}".'.format(self.verb))
            return

        join = Join(collection, **kwargs)
        self.joins.append(join)
        return join


def count(collection, terms=[], **kwargs):
    """Sends a count request."""
    # Create a new Request object
    request = Request(collection=get_collection(collection),
                      verb='get',
                      **kwargs)
    return request


def evaluate_term(term):
    """Converts a term dictionary into a string like "field=^value"."""
    operator = '='

    # This list contains the characters signifying their search modifier in the
    # order they are listed in the enum.
    char_list = ['', '*', '>', ']', '<', '[', '^', '!']
    if 'modifier' in term.keys():
        operator += char_list[term['modifier'].value - 1]

    return term['field'] + operator + term['value']


def get(collection, hide=[], limit=20, show=[], terms=[]):
    request = Request(collection=get_collection(collection),
                      hide=turn_into_list(hide),
                      show=turn_into_list(show),
                      limit=limit,
                      # Show, Hide, Sort, Has, Resolve?, Case, Limit
                      # LimitPerDb?, Start, IncludeNull, Lang, Join?,
                      # Tree, Timing, exactMatchFirst, Distinct, Retry
                      terms=turn_into_list(terms),
                      verb='get')
    return request


def turn_into_list(object):
    """Returns a list containing the object passed.

    If a list is passed to this function, this function will not create a
    nested list, it will instead just return the list itself."""

    if isinstance(object, list):
        return object
    else:
        return [object]

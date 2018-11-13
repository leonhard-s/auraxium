import json

import requests

# This is the base URL used to access the Daybreak Game Company's server.
_CENSUS_BASE_URL = 'http://census.daybreakgames.com/'


class Request():
    """Represents a request to make to the Census API server.

    A request instance provides an object-based way of generating the URL
    required to retrieve the desired information from the API server. It can
    also be kept around and retrieved repeatedly, which is helpful for
    scheduled requests.

    Parameters
    ----------
    collection : string
        The Census API collection to access. Required.
    namespace : string
        The namespace for the request. Determines which collections will be
        available. See 'http://census.daybreakgames.com/get/<namespace>/' for
        a list of collections for a given namespace. Default: 'ps2'.
    terms : list
        A list containing filtering information telling the server which
        elements of the collection we want to access. Optional.
    verb : string
        The operation we want the server to perform. Can be one of two strings:
        'count' returns the number of matching items, 'get' will return a list
        of matching items. Default: 'get'.
    The following query commands are supported:
        case (bool), distinct (bool), exact_match_first (bool),
        has (list), hide (list), include_null (bool), lang (str), limit (int),
        retry (bool), show (list), sort (list), start (int), timing (bool),
        tree (list)
    (Please refer to the query commands documentation for details.)

    Attributes
    ----------
    joins : list
        A list of Request.Join objects attached to the request. Do not add new
        ones by hand, use the Request.join() method instead.
    collection : string
        The Census API collection to access.
    commands : dict
        A dictionary containing any query commands to send with this request.
    terms: list
        A list containing filtering information telling the server which
        elements of the collection we want to access.
    namespace : string
        The namespace for the request; determines which collections will be
        available.
    verb : string
        The operation we want the server to perform.

    """

    def __init__(
            self, collection, namespace='ps2', terms=[], verb='get', **kwargs):
        self.collection = collection
        self.commands = {}
        self.joins = []
        self.namespace = namespace
        self.terms = terms
        self.verb = verb

        # For every search term
        for item in terms:
            # If one of the lists only has two items, set its type to 'equals'
            if len(item) == 2:
                item.insert(1, 'equals')

        # For every query command
        for key, value in kwargs.items():
            # Any kwargs are treated as query commands here, they will be
            # checked as part of the Request.retrieve() method.
            self.commands[key] = value

    class Join():
        """Represents a joined query inside a request.

        Joined queries can/should be used to minimize the number of individual
        requests sent to the server. Do not instantiate manually, use the
        methods Request.join() and Join.join() instead.

        Parameters
        ----------
        collection : string
            The Census API collection the joined query will access. Required.
        list : bool
            Whether the joined data is going to be a list or not.
            Default: False.
        name : string
            The name of the field where the joined data will be inserted into
            the response. Default: `join_<collection>`.
        on : string
            The field on the parent collection to match to.
            Default: `<parent_collection>_id`.
        outer : bool
            Decides whether non-matches will be included in the response. If
            set to false, non-matches will not be included. Default: True.
        terms : list
            A list containing filtering information telling the server which
            elements of the collection we want to access. Optional.
        to : string
            The field on the child collection to match with.
            Default: `<child_collection>_id`.
        The following query commands are supported:
            hide (list), show (list)
        (Please refer to the query commands documentation for details.)

        Attributes
        ----------
        collection : string
            The Census API collection the joined query will access.
        commands : dict
            A dictionary containing any query commands to send with the joined
            request.
        joins : list
            A list of nested Request.Join objects attached to the Join. Do not
            add new ones by hand, use the Join.join() method instead.
        list : bool
            Whether the joined data is going to be a list or not.
        nickname : string
            The name of the field where the joined data will be inserted into the response.
        on : string
            The field on the parent collection to match to.
        outer : bool
            Decides whether non-matches will be included in the response. If
            set to false, non-matches will not be included.
        terms : list
            A list containing filtering information telling the server which
            elements of the collection we want to access.
        to : string
            The field on the child collection to match with.

        Methods
        -------
        join() : Request.Join
            Creates a new join and appends it to the 'joins' attribute.

        """

        def __init__(
                self, collection, nickname=None, list=False, on=None,
                outer=True, terms=[], to=None, **kwargs):
            self.collection = collection
            self.commands = {}
            self.joins = []
            self.list = list
            self.nickname = nickname
            self.on = on
            self.outer = outer
            self.terms = terms
            self.to = to

            # Set concatenated default values
            if self.nickname == None:
                self.nickname = 'join_{}'.format(self.collection)
            if self.on == None:
                self.on = '{}_id'.format(self.collection)
            if self.to == None:
                self.to = '{}_id'.format(self.collection)

            # For every query command
            for key, value in kwargs.items():
                if key == 'show':
                    self.commands[key] = value
                elif key == 'hide':
                    self.commands[key] = value
                else:
                    print('Unsupported query command: "{}"'.format(key))

        def join(self, collection, **kwargs):
            """Creates a new Join for the Request.

            The created Join object will automatically be appended to the
            Request.joins list. The returned Join object may be referenced to
            create nested joins using the Join.join() method.

            Parameters
            ----------
            **kwargs
                All keyword arguments will be forwarded to the Join object's
                __init__() method.

            Returns
            -------
            Request.Join
                The created Join object. Added to the "joins" list
                automatically, only reference for creating nested
                joins.

            """

            join = Request.Join(collection, **kwargs)
            self.inner_joins.append(join)
            return join

    def join(self, collection, **kwargs):
        """Creates a new Join for the request.

        Creates a new Join and appends it to the request's "joins" attribute.

        Parameters
        ----------
        **kwargs
            All keyword arguments will be forwarded to the Join object's
            __init__() method.

        Returns
        -------
        Request.Join
            The created Join object. Added to the "joins" list
            automatically, only reference for creating nested
            joins.

        """

        join = self.Join(collection, **kwargs)
        self.joins.append(join)
        return join

    def retrieve(self):
        """Performs the request and returns the server's response.

        Returns
        -------
        dict
            The response of the server. In most cases, even a server error
            will return a valid dictionary containing additional information.

        """

        def serialize_join(join):
            """Converts a Join object into a string.

            Generates the URL-friendly representation of the join and any
            nested joins contained within.

            Parameters
            ----------
            join : Request.Join
                The Join object to serialize.

            Returns
            -------
            str
                The string representation of the join(s).

            """

            # Key: type
            string = join.collection
            # Key: inject_at
            string += '^inject_at:{}'.format(join.nickname)
            # Key: list
            if join.list:
                string += '^list:1'
            # Key: on
            string += '^on:{}'.format(join.on)
            # Key: outer
            if not join.outer:
                string += '^outer:0'
            # Key: terms
            if len(join.terms) > 0:
                string += '^terms:'
                # Loop through all filter terms
                for key in join.terms:
                    string += '{}={}\''.format(key, join.terms[key])
                # Slice the final '-separator off the end of the string
                string = string[:-1]
            # Key: to
            string += '^to:{}'.format(join.to)

            # If the 'show' list is not empty, add them
            if 'show' in join.commands:
                string += '^show:{}'.format('\''.join(join.commands['show']))
            # Only use the 'hide' parameter if the 'show' list is empty
            elif 'hide' in join.commands:
                string += '^hide:{}'.format('\''.join(join.commands['hide']))

            # If there are any inner joins
            if len(join.joins) > 0:
                # Enter a new layer of join-ception
                string += '('
                # Loop through the inner joins
                for inner_join in join.joins:
                    serialize_join(inner_join)
                string += ')'
            return string

        # Concatenate the core parts of the request into a URL
        url = '{}{}/{}/{}'.format(_CENSUS_BASE_URL, self.verb, self.namespace,
                                  self.collection)

        # Loop through any search modifiers that may have been specified
        for item in self.terms:
            url += '&'
            # 'equals'
            if item[1] == 'equals':
                url += '{}={}'.format(item[0], item[-1])
            elif item[1] == 'contains':
                url += '{}=*{}'.format(item[0], item[-1])
            # 'greater_or_equal'
            elif item[1] == 'greater_or_equal':
                url += '{}=]{}'.format(item[0], item[-1])
            # 'greater_than'
            elif item[1] == 'greater_than':
                url += '{}=>{}'.format(item[0], item[-1])
            # 'less_or_equal'
            elif item[1] == 'less_or_equal':
                url += '{}=[{}'.format(item[0], item[-1])
            # 'less_than'
            elif item[1] == 'less_than':
                url += '{}=<{}'.format(item[0], item[-1])
            # 'not'
            elif item[1] == 'not':
                url += '{}=!{}'.format(item[0], item[-1])
            # 'starts_with'
            elif item[1] == 'starts_with':
                url += '{}=^{}'.format(item[0], item[-1])
            else:
                print('Error: Unknown search modifier: {}'.format(item[1]))

        # Case
        if 'case' in self.commands:
            if not self.commands['case']:
                url += '&c:case=false'

        # Distinct
        if 'distinct' in self.commands:
            url += '&c:distinct={}'.format(self.commands['distinct'])

        # Exact match first (overrides c:sort)
        if 'exact_match_first' in self.commands:
            if self.commands['exact_match_first']:
                url += '&c:exactMatchFirst=true'

        # Has
        if 'has' in self.commands:
            url += '&c:has='.format(','.join(self.commands['has']))

        # Include null
        if 'include_null' in self.commands:
            if self.commands['include_null']:
                url += 'c:includeNull=true'

        # Language
        if 'lang' in self.commands:
            url += '&c:lang={}'.format(self.commands['lang'])
        else:
            url += '&c:lang=en'

        # Limit
        if 'limit' in self.commands:
            url += '&c:limit={}'.format(self.commands['limit'])

        # Limit per DB
        if 'limit_per_db' in self.commands:
            url += '&c:limit_per_db={}'.format(self.commands['limit_per_db'])

        # Retry
        if 'retry' in self.commands:
            if not self.commands['retry']:
                url += '&c:retry=false'

        # Sort
        if 'sort' in self.commands:
            url += '&c:sort='.format(','.join(self.commands['sort']))

        # Start
        if 'start' in self.commands:
            url += '&c:start={}'.format(self.commands['start'])

        # timing
        if 'timing' in self.commands:
            if self.commands['timing']:
                url += '&c:timing=true'
        # else:
        #     # Use bot setting

        # Tree
        if 'tree' in self.commands:
            url += '&c:tree={}'.format(self.commands['tree'])

        # If the 'show' list is not empty, add them
        if 'show' in self.commands:
            url += '&c:show={}'.format(','.join(self.commands['show']))
            # TODO: Add a warning to let the user know inputs are being ignored?
            # if 'hide' in self.commands:
            #     print('Info: c:show has been specified, omitting c:hide.')
        # Only use the 'hide' parameter if the 'show' list is empty
        elif 'hide' in self.commands:
            url += '&c:hide={}'.format(','.join(self.commands['hide']))

        # If there are any joins
        if len(self.joins) > 0:
            url += '&c:join='
            # Loop through all outer joins
            for join in self.joins:
                url += serialize_join(join)

        # In the above code, we never worried about which the first query
        # was going to be and just used '&' everywhere. This is fixed here.
        url = url.replace('&', '?', 1)
        print(url)
        # Get the response from the server and convert it to a dictionary
        response = json.loads(requests.get(url).text)

        return response

from typing import Any, Dict, List, Optional, Tuple
from .census import retrieve, SearchModifier, Term, generate_term
from .constants import CENSUS_ENDPOINT
from .join import Join
from .type import CensusValue


class Query():
    """A query to be made to the REST API.

    Once created, a query may be re-run any number of times.
    """

    def __init__(self, collection: str = '', namespace: str = '',
                 service_id: str = '', case: bool = True,
                 exact_match_first: bool = False, include_null: bool = False,
                 lang: str = '', limit: int = 1,
                 show_fields: List[str] = None, hide_fields: List[str] = None,
                 limit_per_db: Optional[int] = None, retry: bool = True,
                 start: int = 0, timing: bool = False,
                 **kwargs: CensusValue) -> None:
        """Initializer."""
        self.collection = collection
        self.namespace = namespace
        self.service_id = service_id
        # Query commands
        self.case = case
        self._distinct = ''
        self.exact_match_first = exact_match_first
        self.has_field: List[str] = []
        self.show_fields = [] if show_fields is None else show_fields
        self.hide_fields = [] if hide_fields is None else hide_fields
        self.include_null = include_null
        self.lang = lang
        if limit < 1:
            raise ValueError('negative counts are not a thing')
        self.limit = limit
        if limit_per_db is not None and limit_per_db < 1:
            raise ValueError('negative counts are not a thing')
        self.limit_per_db = limit_per_db
        self.joins: List[Join] = []
        self.resolves: List[str] = []
        self.retry = retry
        self.start = start
        self.sort_by: List[str] = []
        self.timing = timing
        # Additional kwargs are passed on to the `generate_term` method
        self.terms: List[Term] = []
        for field, value in kwargs.items():
            self.terms.append(generate_term(field.replace('__', '.'), value))

    def add_term(self, field: str, value: CensusValue,
                 modifier: SearchModifier = SearchModifier.EQUAL_TO) -> 'Query':
        """Add a search term to this query.

        Any results returned by a query must meet every term defined
        for it.
        """
        new_term = Term(field, value, modifier)
        self.terms.append(new_term)
        return self

    def count(self) -> int:
        """Return the number of matching items for this query.

        Not all collections are countable.
        """
        data = retrieve(self.url(count=True), True)
        return int(data['count'])

    def distinct(self, field_name: str) -> 'Query':
        """Return the distinct values for a given field.

        Results are capped to 20,000 results.
        """
        self._distinct = field_name
        return self

    def get(self, convert: bool = True) -> List[Dict[str, Any]]:
        """Perform the query and return the results list."""
        data = retrieve(self.url(), convert=convert)
        return data[f'{self.collection}_list']

    def has(self, field_name: str, *args: str) -> 'Query':
        """Only return results with non-NULL values for these fields.

        Useful for filtering common collections based on the fields
        that are populated. Example: Only weapons using a heat
        mechanic will/should have non-NULL values for related fields.
        """
        self.has_field = [field_name]
        self.has_field.extend(args)
        return self

    def set_hide_fields(self, field_name: str, *args: str) -> 'Query':
        """Hide the given fields from the response.

        This only takes effect if `show_fields` is not specified.
        """
        self.hide_fields = [field_name]
        self.hide_fields.extend(args)
        return self

    def join(self, collection: str, inject_at: str = '', is_list: bool = False,
             on: str = '', is_outer: bool = True, to: str = '',
             hide: List[str] = None, show: List[str] = None,
             **kwargs: Tuple[str, CensusValue]) -> Join:
        """Create an inner query (or join) for this query.

        All arguments passed to this function are forwarded to the new
        Join's initializer. The created join is returned.
        """
        join = Join(collection, inject_at, is_list,
                    on, is_outer, to, show, hide, **kwargs)
        self.joins.append(join)
        return join

    def url(self, count: bool = False) -> str:
        """Generate the URL for this query."""
        from . import namespace, service_id
        # This list holds the elements of the URL path
        path_items: List[str] = [CENSUS_ENDPOINT]
        # Use the query's service ID if it has been changed
        if self.service_id:
            path_items.append('s:' + self.service_id)
        else:
            path_items.append('s:' + service_id)
        # Set the query verb
        path_items.append('count' if count else 'get')
        # Use the query's namespace if it has been changed
        if self.namespace:
            path_items.append(self.namespace)
        else:
            path_items.append(namespace)
        # Add the collection if required
        if self.collection:
            path_items.append(self.collection)
        # Concatenate the URL path elements
        url = '/'.join(path_items)
        # Create a list of all query string items
        query_string_items = [t.to_url() for t in self.terms]
        # Process any query commands
        query_string_items.extend(_process_query_commands(self))
        # Append the query string to the URL
        if query_string_items:
            url += '?' + '&'.join(query_string_items)
        return url

    def resolve(self, field: str, *args: str) -> 'Query':
        """Resolve one or more resolvable fields.

        Returning the list of collections for a namespace also returns
        lists of resolvable fields for that collections.

        For a more flexible option, see the `join` method.
        """
        self.resolves = [field]
        if args:
            self.resolves.extend(args)
        return self

    def set_show_fields(self, field_name: str, *args: str) -> 'Query':
        """Only include the given fields in the response.

        This overrides the `hide_fields` method.
        """
        self.show_fields = [field_name]
        self.show_fields.extend(args)
        return self

    def sort(self, field_name: str, descending: bool = False) -> 'Query':
        """Sorting the results by the given field."""
        string = field_name
        if descending:
            string += ':-1'
        self.sort_by.append(string)
        return self

    def tree(self, field: str, is_list: bool = False, prefix: str = '',
             start: int = 0) -> 'Query':
        """Restructure the results returned into a tree view.

        "field" is the field used for generating the tree view.
        "list" causes items to be grouped into lists
        "prefix" will be prefixed to the field values
        "start" is the name of the field where the tree view will start

        The query object is returned to allow for chaining of query
        commands.
        """
        raise NotImplementedError()


def _process_query_commands(query: Query) -> List[str]:
    """Generate a list of query string items from query commands."""
    items: List[str] = []
    # NOTE: The order the query commands are processed in is the same as in
    # the documentation, this is not random.
    # c:show
    if query.show_fields:
        items.append('c:show=' + ','.join(query.show_fields))
        if query.hide_fields:
            raise Warning('show_fields overrides hide_fields')
    # c:hide
    elif query.hide_fields:
        items.append('c:hide=' + ','.join(query.hide_fields))
    # c:sort
    if query.sort_by:
        items.append('c:sort=' + ','.join(query.sort_by))
    # c:has
    if query.has_field:
        items.append('c:has=' + ','.join(query.has_field))
    # c:resolve
    if query.resolves:
        items.append('c:resolve=' + ','.join(query.resolves))
    # c:case
    if not query.case:
        items.append('c:case=0')
    # c:limit
    if query.limit > 1:
        items.append(f'c:limit={query.limit}')
    # c:limitPerDB
    if query.limit_per_db is not None and query.limit_per_db > 1:
        items.append(f'c:limitPerDB={query.limit_per_db}')
    # c:start
    if query.start > 0:
        items.append(f'c:start={query.start}')
    # c:includeNull
    if query.include_null:
        items.append('c:includeNull=1')
    # c:lang
    if query.lang != '':
        items.append(f'c:lang={query.lang}')
    # c:join
    if query.joins:
        join_string = 'c:join='
        join_string += ','.join([j.process_join() for j in query.joins])
        items.append(join_string)
    # c:tree
    # TODO: Implement "c:tree" query command
    # c:timing
    if query.timing:
        items.append('c:timing=1')
    # c:exactMatchFirst
    if query.exact_match_first:
        items.append('c:exactMatchFirst=1')
    return items

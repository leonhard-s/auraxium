"""QueryBase handling components.

This includes top-level queries, as well as inner, joined queries.
"""

import copy
from typing import Any, Callable, List, Optional, Tuple, Type, TypeVar, Union

import yarl

from .support import (CensusValue, default_query_data, QueryData,
                      SearchModifier, SearchTerm)

_QueryBaseT = TypeVar('_QueryBaseT', bound='QueryBase')
_T = TypeVar('_T')


class QueryBase:
    """Base class for functionality shared between queries and joins.

    If you want to re-use the same query multiple times, use this
    class. For more control about how the query is performed, refer to
    the Query and JoinedQuery subclasses.

    Attributes:
        collection: The API collection to access.
        hide_fields: The list of fields to hide from the results. See
            the QueryBase.set_hide_fields() setter method for details.
        joins: A list of inner queries that were attached to this one.
        show_fields: The list of fields to include in the results. See
            the QueryBase.set_show_fields() setter method for details.
        terms: Filter terms used to reduce the number of results.

    """

    def __init__(self, collection: Optional[str] = None,
                 **kwargs: CensusValue) -> None:
        """Initialise the query.

        This class contains the core query information like the API
        collection to access and any filter terms provided. This exists
        mostly to reduce code repetition, use its subclasses, Query and
        JoinedQuery, for API interaction.

        You can move generic information between the QueryBase class
        and its subclasses via the QueryBase.copy() factory. This is
        useful if you have an existing query and would like to join it
        onto another. See that method's docstring for details.

        Args:
            collection (optional): The API collection to access or None
                to display the list of available collections. Defaults
                to None.
            *kwargs: Key/value pairs to pass to the QueryBase.add_term()
                method.

        """
        self.collection = collection
        self.commands: QueryData = default_query_data()
        self.joins: List['JoinedQuery'] = []
        self.terms: List[SearchTerm] = []
        # Replace and double underscores with dots to allow accessing inner
        # fields like "name.first" or "battle_rank.value"
        kwargs = {k.replace('__', '.'): v for k, v in kwargs.items()}
        # Run the add_term method for each of the converted key/value pairs
        _ = [self.add_term(k, v, parse_modifier=True)
             for k, v in kwargs.items()]

    def add_join(self: _QueryBaseT, query: 'JoinedQuery',
                 **kwargs: Any) -> _QueryBaseT:
        """Add an existing JoinedQuery to this query.

        This converts an existing QueryBase instance to a JoinedQuery
        using the QueryBase.copy() factory. The created join is then
        added to this query.

        To create a new query and add it immediately, use the
        create_join method instead.

        Args:
            query: Another query to join to the current query.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.joins.append(JoinedQuery.copy(query, **kwargs))
        return self

    def add_term(self: _QueryBaseT, field: str, value: CensusValue,
                 modifier: SearchModifier = SearchModifier.EQUAL_TO, *,
                 parse_modifier: bool = False) -> _QueryBaseT:
        """Add a new filter term to the query.

        Filter terms are used to either reduce the number of results
        returned, or to specify the exact ID expected. Refer to the
        docstring of the SearchTerm class for details and examples.

        Args:
            field: The field to filter by.
            value: The value of the filter term.
            modifier(optional): A search modifier to use. This will
                only be used if parse_modifier is False. Defaults to
                SearchModifier.EQUAL_TO.
            parse_modifier(optional): If True, the search modifier
                will be inferred from the value. Defaults to False.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        if parse_modifier:
            term = SearchTerm.infer(field, value)
        else:
            term = SearchTerm(field, value, modifier=modifier)
        self.terms.append(term)
        return self

    @classmethod
    def copy(cls: Type[_QueryBaseT], template: 'QueryBase',
             copy_joins: bool = False, deep_copy: bool = False,
             **kwargs: Any) -> _QueryBaseT:
        """Create a new query, copying most data from the template.

        The new query will share the collection, terms and show/hide
        markers of the template. If copy_joins is enabled, it will also
        copy its list of joins.

        Among other things, allows easy creation of joins from existing
        queries, which is handy if you have complex existing joins or
        hidden fields that would be tedious to recreate.

        By default, this creates a shallow copy. Modifying the terms or
        joined queries will cause mutations of the template. Set the
        deep_copy flag to ensure complete independence.

        Any keyword arguments are passed to the new query's
        initialiser.

        Example:
            # This is an existing query that does what we need it to.
            # Maybe it has a complex join structure or hidden fields
            # that we would like to keep unchanged.
            old = Query('character')

            # This is an unrelated, new query. We want to return the
            # exact same data structure
            new = Query('outfit_member', outfit_id=...).limit(1000)

            # Create a join emulating the original query and add it
            join = JoinedQuery.copy(old, copy_joins=True)
            new.add_join(join)

        Args:
            template: The query to copy.
            copy_joins (optional): Whether to recursively copy joined
                queries. Defaults to False.
            deep_copy (optional): Whether to perform a deep copy. Use
                this if you intend to modify the list of terms or other
                mutable types to avoid changing the template. Defaults
                to False.
            **kwargs: Any keyword arguments are passed on to the new
                query's constructor.

        Returns:
            An instance of the current class populated with information
            from the template query.

        """

        def dummy_copy(obj: _T) -> _T:
            """Dummy function that does not actually copy anything."""
            return obj

        # NOTE: This assignment will cause mypy errors if performed via a
        # ternary operator.
        copy_func: Callable[[_T], _T] = dummy_copy
        if deep_copy:
            copy_func = copy.deepcopy
        instance = cls(copy_func(template.collection), **kwargs)
        instance.terms = copy_func(template.terms)
        if copy_joins:
            instance.joins = copy_func(template.joins)
        instance.commands['hide'] = copy_func(template.commands['hide'])
        instance.commands['show'] = copy_func(template.commands['show'])

        return instance

    def create_join(self, collection: str, *args: Any,
                    **kwargs: Any) -> 'JoinedQuery':
        """Create a new joined query and add it to the current one.

        See the initialiser for JoinedQuery for arguments, this method
        passes and parameters given on.

        Args:
            collection: The collection to join.
            *args: Any anonymous positional arguments are passed on to
                JoinedQuery.__init__()
            *kwargs: Any anonymous keyword arguments are passed on to
                JoinedQuery.__init__()

        Returns:
            The JoinedQuery instance that was created.

        """
        join = JoinedQuery(collection, *args, **kwargs)
        self.joins.append(join)
        return join

    def hide(self: _QueryBaseT, field: str, *args: str) -> _QueryBaseT:
        """Set the fields to hide in the response.

        The given fields will not be included in the result. Note that
        this can break joins if the field they are attached to is not
        included.

        This is mutually exclusive with QueryBase.show(); setting one
        will undo any changes made by the other.

        Args:
            field: A field name to hide from the result data.
            *args: Any number of additional fields to hide.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['hide'] = [field]
        self.commands['hide'].extend(args)
        self.commands['show'] = []
        return self

    def show(self: _QueryBaseT, field: str, *args: str) -> _QueryBaseT:
        """Set the fields to show in the response.

        Any other fields will not be included in the result. Note that
        this can break joins if the field they are attached to is not
        included.

        This is mutually exclusive with QueryBase.hide(); setting one
        will undo any changes made by the other.

        Args:
            field: A field name to include in the result data.
            *args: Any number of additional fields to include.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['show'] = [field]
        self.commands['show'].extend(args)
        self.commands['hide'] = []
        return self


class Query(QueryBase):
    """The main query supplied to the API.

    The top-level query has access to additional return value formats
    such as sorting or tree views, and also supports additional, global
    flags that will propagate through to any inner, joined queries.

    This subclasses QueryBase. Refer to its docstring for details on
    inherited methods and attributes.

    You can find additional information on the attributes in their
    respective setter methods.

    Attributes:
        namespace: The API namespace to access.
        service_id: A unique ID used to identify your API client. Note
            that the default service ID is heavily rate limited.

    """

    def __init__(self, collection: Optional[str] = None,
                 namespace: str = 'ps2:v2', service_id: str = 's:example',
                 **kwargs: CensusValue) -> None:
        """Create a new top-level query.

        The collection argument, as well as any keyword arguments, are
        passed on to the constructor of the QueryBase class.

        Args:
            collection (optional): The API collection to access.
                Defaults to None.
            namespace (optional): The namespace to access.  Defaults to
                'ps2:v2'.
            service_id (optional): Your personal service ID. Note that
                the default service ID is heavily rate limited.
                Defaults to 's:example'.

        """
        super().__init__(collection, **kwargs)
        self.namespace = namespace
        self.service_id = service_id

    def __str__(self) -> str:
        """Return the string representation of the query.

        This is the URL in its finished form. Use Query.url()
        to get the URL as a yarl object for extra control.

        Returns:
            The full URL describing this query and all of its joins.

        """
        return str(self.url().human_repr())

    def case(self, value: bool = True) -> 'Query':
        """Globally ignore case for this query.

        Note that case-insensitive look-ups are significantly slower.
        Where available, use a case-sensitive query targetting a
        lowercase field like ps2/character.name.first_lower.

        Args:
            value (optional): Whether to ignore case for this query.
                Defaults to True.

        Returns:
            The full URL describing this query and all of its joins.

        """
        self.commands['case'] = value
        return self

    def has(self, field: str, *args: str) -> 'Query':
        """Hide results with a NULL value at the given field.

        This is useful for filtering large data sets by optional
        fields, such as searching the ps2/weapons collection for
        heat-based weapons using the heat-mechanic-specific fields.

        This updates the has_fields attribute.

        Args:
            field: The field required for results to be included.
            *args: Additional required fields.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['has'] = [field]
        self.commands['has'].extend(args)
        return self

    def distinct(self, field: Optional[str]) -> 'Query':
        """Query command used to show all unique values for a field.

        Args:
            field: The field to show unique values for. Set to None to
                disable.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['distinct'] = field
        return self

    def exact_match_first(self, value: bool = True) -> 'Query':
        """Whether to display exact matches before partial matches.

        When performing RegEx searches (i.e. ones using either
        SearchModifier.STARTS_WITH or SearchModifier.CONTAINS), this
        setting will always promote an exact match to be the first item
        returned, regardless of any sorting settings applied.

        Args:
            value (optional): Whether to promote exact matches.
                Defaults to True.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['exact_match_first'] = value
        return self

    def include_null(self, value: bool) -> 'Query':
        """Whether to include NULL values in the response.

        This is useful for API introspection, but it is generally more
        bandwidth-friendly to use the dict.get() method with a default
        value when parsing the result dictionary.

        This only affects the top-level query itself; joined queries
        will only show non-NULL values.

        Args:
            value: Enable or disable the setting.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['include_null'] = value
        return self

    def lang(self, lang: Optional[str] = None) -> 'Query':
        """Set the locale to user for the query.

        By default, queries return all locales for localised strings.
        Use this flag to only include the given locale, or reset to
        None to include all localisations.

        The following locales are currently supported and maintained.

            German: 'de', English: 'en', Spanish: 'es',
            French: 'fr', Italian: 'it'

        Args:
            lang (optional): The locale identifier to return. Defaults
                to None.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['lang'] = lang
        return self

    def limit(self, limit: int) -> 'Query':
        """Specify the number of results returned.

        By default, the API will only return the first match for any
        given query, you can increase the number of results using this
        method.

        The maximum number of values permissable varies from collection
        to collection, e.g. 100k for ps2/character, but only 5000 for
        ps2/item. Use your best judgement.

        This is mutually exclusive with Query.set_limit_per_db(),
        setting one will undo the changes made by the other.

        Args:
            limit: The number of results to return. Must be at least 1.

        Raises:
            ValueError: Raised if limit is less than 1.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        if limit < 1:
            raise ValueError('limit must be greater than or equal to 1')
        self.commands['limit'] = limit
        self.commands['limit_per_db'] = 1
        return self

    def limit_per_db(self, limit_per_db: int) -> 'Query':
        """Specify the number of results returned per database.

        This method works similarly to Query.set_limit(), but will
        yield better results for distributed collections such as
        ps2/character, which is spread across 20 different databases
        more or less randomly.

        This is mutually exclusive with Query.set_limit(), setting
        one will undo the changes made by the other.

        Args:
            limit_per_db: The number of results to return per database.
                Must be at least 1.

        Raises:
            ValueError: Raised if limit_per_db is less than 1.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        if limit_per_db < 1:
            raise ValueError('limit_per_db must be greater than or equal to 1')
        self.commands['limit_per_db'] = limit_per_db
        self.commands['limit'] = 1
        return self

    def offset(self, offset: int) -> 'Query':
        """Alias for the Query.start() method.

        Refer to its docstring for details.

        Args:
            offset: The number of results to skip.

        Raises:
            ValueError: Raised if offset is negative.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        try:
            self.start(offset)
        except ValueError as err:
            raise ValueError('offset may not be negative') from err
        return self

    def resolve(self, name: str, *args: str) -> 'Query':
        """Resolve additional data for a collection.

        Resolves are a lighter version of joined queries and can be
        used to quickly include associated information with the
        results.

        Perform a query with no collection specified to see a list of
        resolvable names for each collection.

        Args:
            name: A resolvable name to attach to the query.
            *args: Any number of additional resolvable names to attach.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['resolve'] = [name]
        self.commands['resolve'].extend(args)
        return self

    def retry(self, retry: bool = False) -> 'Query':
        """Enable automatic query retry.

        By default, failed queries will be retried automatically. Set
        this to False to disable this behaviour if you want to fail
        early.

        Args:
            retry (optional): Whether to enable automatic query
                retrying. Defaults to False.

        Returns:
            The full URL describing this query and all of its joins.

        """
        self.commands['retry'] = retry
        return self

    def start(self, start: int) -> 'Query':
        """Skip the given number of results in the response.

        Together with Query.set_limit(), this can be used to create
        a paginated view of API data.

        Args:
            start: The number of results to skip.

        Raises:
            ValueError: Raised if start is negative.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        if start < 1:
            raise ValueError('start may not be negative')
        self.commands['start'] = start
        return self

    def sort(self, field: Union[str, Tuple[str, bool]],
             *args: Union[str, Tuple[str, bool]]) -> 'Query':
        """Sort the results by one or more fields.

        By default, this uses ascending sort order. For descending
        order, pass a tuple with a negative second element:

            QueryBase.sort('field1', ('field'2, True))  # Ascending
            QueryBase.sort(('field3', False))  # Descending

        If multiple field names are provided, multiple sorting passes
        will be performed in order to further refine the list returned.

        Args:
            field: A qualified field name to sort by.
            *args: Additional fields to sort by.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['sort'] = [field]
        self.commands['sort'].extend(args)
        return self

    def timing(self, value: bool = True) -> 'Query':
        """Enabling query profiling output.

        Setting this flag will include an additional "timing" key in
        the response, providing timing information for the main query
        and any joins.

        Args:
            value (optional): Whether to enable profiling. Defaults to
                True.

        Returns:
            The full URL describing this query and all of its joins.

        """
        self.commands['timing'] = value
        return self

    def tree(self, field: str, is_list: bool = False, prefix: str = '',
             start: Optional[str] = None) -> 'Query':
        """Reformat a result list into a data tree.

        This is useful for lists of data with obvious categorisation,
        such as grouping weapons by their type.

        Args:
            field: The field to remove and use for the data structure.
            list (optional): Whether the tree data is a list. Defaults
                to 0.
            prefix (optional): A prefix to add to the field value to
                increase readability. Defaults to ''.
            start (optional): Used to tell the tree where to start. If
                None, the root list of results will be reformatted as a
                tree. Defaults to None.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.commands['tree'] = {'field': field, 'is_list': is_list,
                                 'prefix': prefix, 'start': start}
        return self

    def url(self, verb: str = 'get', skip_checks: bool = False) -> yarl.URL:
        """Generate the URL representing this query.

        This will also recursively process any joined queries.

        Args:
            verb (optional): The query verb to use for the query. Known
                options are 'get', used to return a list of results,
                and 'count', used to return the length of that list.
                Defaults to 'get'.
            skip_checks (optional): By default, the url generator will
                perform a number of checks to validate your query.
                Enabling this flag will skip the checks. Defaults to
                False.

        Returns:
            A URL object representing the query.

        """
        # NOTE: This local import is required to avoid a circular import.
        # pylint: disable=import-outside-toplevel
        from .urlgen import generate_url
        return generate_url(self, verb, validate=not skip_checks)


class JoinedQuery(QueryBase):
    """A sub-query to be joined to an existing query.

    Joined queries (or "joins") allow performing multiple, related
    look-ups in the same request. For a simpler but less powerful
    interface, see the Query.resolve() method.

    This subclasses QueryBase. Refer to its docstring for details on
    inherited methods and attributes.

    You can find additional information on the attributes in their
    respective setter methods.

    Attributes:
        inject_at: The name of the field to inject the results at.
        is_list: Whether the join should return a list.
        is_outer: Whether non-matches will be included in the results.
        child_field: The field on the child collection to join to.
        parent_field: The field on the parent collection onto which the
            child will be joined.

    """

    def __init__(self, collection: str, **kwargs: CensusValue) -> None:
        """Instantiate a joined, inner query."""
        super().__init__(collection, **kwargs)
        self.inject_at: Optional[str] = None
        self.is_list: bool = False
        self.is_outer: bool = True
        self.child_field: Optional[str] = None
        self.parent_field: Optional[str] = None

    @classmethod
    def copy(cls, template: QueryBase, copy_joins: bool = False,
             deep_copy: bool = False, **kwargs: Any) -> 'JoinedQuery':
        """Create a new query, copying most data from the template.

        The new query will share the collection, terms and show/hide
        markers of the template. If copy_joins is enabled, it will also
        copy its list of joins.

        Among other things, allows easy creation of joins from existing
        queries, which is handy if you have complex existing joins or
        hidden fields that would be tedious to recreate.

        By default, this creates a shallow copy. Modifying the terms or
        joined queries will cause mutations of the template. Set the
        deep_copy flag to ensure complete independence.

        Any keyword arguments are passed to the new query's
        initialiser.

        Example:
            # This is an existing query that does what we need it to.
            # Maybe it has a complex join structure or hidden fields
            # that we would like to keep unchanged.
            old = Query('character')

            # This is an unrelated, new query. We want to return the
            # exact same data structure
            new = Query('outfit_member', outfit_id=...).limit(1000)

            # Create a join emulating the original query and add it
            join = JoinedQuery.copy(old, copy_joins=True)
            new.add_join(join)

        Args:
            template: The query to copy.
            copy_joins (optional): Whether to recursively copy joined
                queries. Defaults to False.
            deep_copy (optional): Whether to perform a deep copy. Use
                this if you intend to modify the list of terms or other
                mutable types to avoid changing the template. Defaults
                to False.
            **kwargs: Any keyword arguments are passed on to the new
                query's constructor.

        Raises:
            TypeError: Raised when attempting to copy into a
                JoinedQuery without a collection specified.

        Returns:
            An instance of the current class populated with information
            from the template query.

        """
        # A joined query cannot be created without a collection
        if template.collection is None:
            raise TypeError('JoinedQuery requries a collection')
        # Run the original implementation as normal
        instance = super().copy(template, copy_joins=copy_joins,
                                deep_copy=deep_copy, **kwargs)
        # If the original query had a non-default limit value, the join should
        # also return a list.
        if (isinstance(template, Query)
                and template.limit is not None
                and template.commands['limit'] > 1):
            instance.is_list = True
        return instance

    def set_fields(self, parent: str, child: str) -> 'JoinedQuery':
        """Set the field names to use for the join.

        The API will use inferred names whenever possible, inferred
        names might be <parent-collection>_id or <child-collection>_id.

        Use this method to specify the field names manually.

        Args:
            parent: The field name on the parent collection.
            child: The field name on the child collection.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.parent_field = parent
        self.child_field = child
        return self

    def set_inject_at(self, name: str) -> 'JoinedQuery':
        """Set the field name to inject the join's results at.

        A joined query must inject its own results into the top-level
        query. By default, this is done via the following field name:

            <parent-field>_join_<child-collection>

        This method allows you to specify a more human-friendly name to
        be used instead. Be wary of name collisions.

        Args:
            name: A custom field name to inject the joins results at.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.inject_at = name
        return self

    def set_list(self, is_list: bool) -> 'JoinedQuery':
        """Set whether the current join should return a list.

        If True, the join will return any matching elements. Be wary of
        large relational collections such as ps2/characters_item; there
        is no limiting system, just an eventual hard cutoff. Use terms
        to reduce the number of matching elements when flagging a join
        as a list.

        Args:
            is_list: Whether the join should return a list.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.is_list = is_list
        return self

    def set_outer(self, is_outer: bool) -> 'JoinedQuery':
        """Set whether the current join is an outer or inner join.

        An outer join (the default setting) will include all results,
        regardless of whether some of the terms in its joins are met or
        not.

        An inner join will exclude these settings, which can be useful
        when filtering by inner values.

        For example, say you were displaying a ps2/characters_item
        list with the associated ps2/item collection joined. Even if
        you added a term to only add the joins for items that are
        weapons, you would still find the full ps2/character_item list
        in your results. This is the outer join behaviour.
        However, if the join is flagged as an inner join, it will
        discard any results that do not meet the join's terms.

        Args:
            is_outer: If Truethe join will be an outer join. Set to
                False for inner join behaviour.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.is_outer = is_outer
        return self

    def serialise(self, verbose: bool = False) -> str:
        """Return a string representation of the joined query.

        This generates is the string that will be inserted into the
        URL. This will also recursively process any inner joins added.

        Args:
            verbose (optional): By default, the serialisation will try
                to save space by omitting fields left at their default
                value. Set this flag to True to change that. Defaults
                to False.

        Returns:
            The string representation of the joined query.

        """
        # NOTE: This local import is required to avoid a circular import.
        # pylint: disable=import-outside-toplevel
        from .urlgen import process_join
        return process_join(self, verbose)

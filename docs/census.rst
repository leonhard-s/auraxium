====================
Census URL Generator
====================

.. module:: auraxium.census

The :mod:`auraxium.census` module provides a low-level Python wrapper around the PlanetSide 2 REST API. It is used internally by Auraxium to generate any URLs needed for traversal of the object model, but may also be used by advanced users to customise queries and increase performance of their apps.

The following pages cover the URL generator interface and usage, but the underlying REST endpoint's structure, functionality and limitations are outside the scope of this document. If you are unfamiliar with the Daybreak Game Company's Census API or would like a refresh, please refer to the `Census API Primer`_ in the repository Wiki.

For an example of how to use the URL generator and custom queries in conjunction with the Auraxium object model, refer to the :doc:`../usage/advanced/queries` page.

.. note::

   The URL generator is independent from the rest of the Auraxium package and may be imported separately. If your use case does not benefit from the object model or event streaming client, you can still use the URL generator on its own to keep your source code free of URL literals:

   .. code-block:: python3

      from auraxium import census

      my_query = census.Query('character', name__first='Higby')
      my_query.create_join('character_online_status')

      print(type(my_query.url()))
      # <class 'yarl.URL'>
      print(my_query.url())
      # http://census.daybreakgames.com/get/ps2/character?name.first=Higby&c:join=characters_online_status

.. currentmodule:: auraxium.census

Overview
========

The :mod:`auraxium.census` URL generator works by combining one or more queries and query commands into a single URL and query string. This can then be returned as a :class:`yarl.URL` or cast to :class:`str`.

.. important::

   This module only generates URLs, it does not make requests and also does not provide any exception handling facilities. After generating your URL using the :meth:`Query.url` factory, you must pass it to an HTTP library like :mod:`requests` or :mod:`aiohttp` to handle the web request.

Query interface
===============

Basic functionality supported by all queries is defined in the :class:`QueryBase` class. This includes specifying the collection to access, any number of key-value pairs to match (referred to as `terms` for the rest of the documentation), as well as the :meth:`~QueryBase.show` and :meth:`~QueryBase.hide` methods, which allow the exclusion of unneeded fields from the response.

.. note::

   All query-like objects use a fluent interface for most of their configuration methods. This means that they all return their instance, which allows for method chaining:

   .. code-block:: python3

      from auraxium import census

      # Without method chaining
      my_query = census.Query('character', name__first='Auroram')
      my_query.case(False)
      my_query.show('name.first', 'prestige_level')

      # With method chaining
      my_query = (census.Query('character', name__first='Auroram')
               .case(False).show('name.first', 'prestige_level'))

   Use of this pattern is optional, but it can aid readability when working with complex or heavily nested queries.

This base class is mentioned here for completeness and due to its use in type hints and other parts of the documentation. However, most users will only ever need to directly interact with its subclasses, covered in the next sections.

For a full list of the basic query interface, refer to the :class:`QueryBase API reference<QueryBase>` below.

Top level queries
-----------------

The PlanetSide 2 API defines two distinct types of queries. The first is the main query sent to the server, referred to as the `top level query` in this documentation. It is represented by the :class:`Query` class.

To generate a URL from a query, run the :meth:`Query.url` method. By default, this uses the ``get`` query verb. This is the main endpoint used to retrieve data and supports the entire query interface, and will return actual matches for a given query. Alternatively, one can specify ``verb='count'`` to instead only return the number of potential matches. This is helpful when working with filtered data sets of unknown size, so that pagination or other custom formats can be used to display the requested data.

Top level queries also support global flags (or `query commands`) that allow enable :meth:`case insensitive<Query.case>` string comparison, :meth:`sorting <Query.sort>` of results, or enable special query modes like :meth:`~Query.distinct`, illustrated below:

.. code-block:: python3

   from auraxium import census

   my_query = census.Query('map_region')
   my_query.distinct('facility_type')

   my_query.url()
   # http://census.daybreakgames.com/get/ps2/map_region?c:distinct=facility_type

This query now won't return actual map regions, but instead up to 20'000 unique values for the given field:

.. code-block:: json

   {
      "count": 7,
      "map_region_list": [
         {
            "facility_type": [
               "Amp Station",
               "Bio Lab",
               "Construction Outpost",
               "Large Outpost",
               "Small Outpost",
               "Tech Plant",
               "Warpgate"
            ]
         }
      ],
      "returned": 1
   }

Joined queries
--------------

The other type of query are joined queries, also known as `joins`. These are represented by the :class:`JoinedQuery` class and behave much like regular queries, but are attached to an existing parent query, either a top level :class:`Query` or another join.

Joins are used to return data related to another query's return values as part of the same response. This allows effectively returning related data, such as the name of a player, their outfit, and their top played classes in a single request.

.. important::

   Some API collections, like ``character`` and ``outfit_member``, can have access times in excess of several seconds depending on your client's location. When working with these large tables, it is often preferable to use few large joins rather than multiple smaller queries to reduce latency.

   In particular, it is often worth considering the use of ``single_character_by_id``, which is an indexed, high-performance table containing most data for a given character. The downside is that it contains all player statistics and items, which makes it a very bandwidth-intensive payload to transmit. It also does not support hiding fields or other query commands that could be used to reduce its size.

The relation between a join and its parent is defined by the :meth:`~JoinedQuery.set_fields` method. The joins data is then inserted into an extra field in the response, either named ``<parent_field>_join_<joined_collection>`` (default) or a custom name specified through the :meth:`JoinedQuery.set_inject_at` method.

Joined queries can not be directly translated into a URL, the must be attached to a top level query instead. This can be done via the :meth:`QueryBase.add_join` (for existing joins) or :meth:`QueryBase.create_join` (for new joins) methods. The :meth:`JoinedQuery.serialise` method allows conersion of a :class:`JoinedQuery` into its URL-compatible, serialised format. This hook is used by the parent query when the top level query's :meth:`Query.url` method is called.

For more information on joined queries, pitfalls and examples, refer to the `Joined Queries`_ section of the aforementioned `Census API primer`_ Wiki article.

Query templates
---------------

The core features of a query (i.e. its collection, terms, show/hide field lists and any attached joins) are shared across all types of queries. This allows partial conversion between query types.

This conversion is done as part of the :meth:`Query.copy`/:meth:`JoinedQuery.copy` methods, which take in a template query and creates a new instance of their own class using any applicable values from the given template.

Terms and search modifiers
==========================

The key-value pairs used to filter queries (previously introduced as the query's `terms`) are represented by the :class:`SearchTerm` class, which provides facilities for parsing, serialising and formatting these terms for use in query strings.

Terms can be added directly using a query's :meth:`QueryBase.add_term` method, or may alternatively be generated via keyword arguments as part of the query instantiation:

.. code-block:: python3

   from auraxium import census

   # Added manually
   my_query = census.Query('character')
   my_query.add_term('name.first', 'Higby')

   # Added via keyword arguments
   my_query = census.Query('character, name__first='Higby')

.. note::

   When passing field names as keyword arguments, double underscores will be replaced with a single dot in the search term's :attr:`~SearchTerm.field`. This allows inline definition of nested keys as in the example above.

Search modifiers
----------------

The :meth:`QueryBase.add_term` method also provides a `modifier` field, which allows specifying the type of match to perform via the :class:`SearchModifier` enumerator. Search modifiers allow exact value matches (like :class:`SearchModifier.EQUAL_TO <SearchModifier>` or :class:`SearchModifier.NOT_EQUAL <SearchModifier>`), to ranges (:class:`SearchModifier.GREATER_THAN <SearchModifier>`, etc.), and even basic text value comparison (:class:`SearchModifier.STARTSWITH <SearchModifier>` and :class:`SearchModifier.CONTAINS <SearchModifier>`).

Note that it is allowed to pass the same value multiple times, with different constraints:

.. code-block:: python3

   from auraxium import census

   # Find players between BR 100 and 120
   my_query = census.Query('character')
   my_query.add_term('battle_rank.value', 100, census.SearchModifier.GREATER_THAN)
   my_query.add_term('battle_rank.value', 120, census.SearchModifier.LESS_THAN_OR_EQUAL)

Examples
========

This example retrieves a character by name and joins their online status.

.. code-block:: python3

   """Usage example for the auraxium.census module."""
   from auraxium import census

   query = census.Query('character', service_id='s:example')
   query.add_term('name.first_lower', 'auroram')
   query.limit(20)
   join = query.create_join('characters_online_status')
   url = str(query.url())

   print(url)
   # https://census.daybreakgames.com/s:example/get/ps2:v2/character?c:limit=20&c:join=characters_online_status

API reference
=============

Query types
-----------

.. autoclass:: QueryBase(collection=None, **kwargs)

   .. automethod:: __init__(collection: str | None = None, **kwargs: float | int | str) -> None

   .. automethod:: add_join(query: QueryBase, **kwargs) -> QueryBase

   .. automethod:: add_term(field: str, value: float | int | str, modifier: SearchModifier = SearchModifier.EQUAL_TO, *, parse_modifier: bool = False) -> QueryBase

   .. automethod:: copy(template: QueryBase, copy_joins: bool = False, deep_copy: bool = False, kwargs) -> QueryBase

   .. automethod:: create_join(collection: str, *args, **kwargs) -> JoinedQuery

   .. automethod:: hide(field: str, *args: str) -> QueryBase

   .. automethod:: show(field: str, *args: str) -> QueryBase

.. autoclass:: Query(collection=None, namespace='ps2:v2', service_id='s:example', **kwargs)

   .. automethod:: __init__(collection: str | None = None, namespace: str = 'ps2:v2', service_id: str = 's:example', **kwargs: float | int | str) -> None

   .. automethod:: __str__() -> str

   .. automethod:: case(value: bool = True) -> Query

   .. automethod:: copy(template: QueryBase, copy_joins: bool = False, deep_copy: bool = False, **kwargs) -> Query

   .. automethod:: has(field: str, *args: str) -> Query

   .. automethod:: distinct(field: str | None) -> Query

   .. automethod:: exact_match_first(value: bool = True) -> Query

   .. automethod:: include_null(value: bool) -> Query

   .. automethod:: lang(lang: str | None = None) -> Query

   .. automethod:: limit(limit: int) -> Query

   .. automethod:: limit_per_db(limit_per_db: int) -> Query

   .. automethod:: offset(offset: int) -> Query

   .. automethod:: resolve(name: str, *args: str) -> Query

   .. automethod:: retry(retry: bool = False) -> Query

   .. automethod:: start(start: int) -> Query

   .. automethod:: sort(field: str | tuple[str, bool], *args: str | tuple[str, bool]) -> Query

   .. automethod:: timing(value: bool = True) -> Query

   .. automethod:: tree(field: str, is_list: bool = False, prefix: str = '', start: str | None = None) -> Query

   .. automethod:: url(verb: str = 'get', skip_checks: bool = False) -> yarl.URL

.. autoclass:: JoinedQuery(collection, **kwargs)

   .. automethod:: __init__(collection: str, **kwargs: float | int | str) -> None

   .. automethod:: copy(template: QueryBase, copy_joins: bool = False, deep_copy = False, **kwargs) -> JoinedQuery

   .. automethod:: serialise() -> JoinedQueryData

   .. automethod:: set_fields(parent: str | None, child: str | None = None) -> JoinedQuery

   .. automethod:: set_inject_at(key: str | None) -> JoinedQuery

   .. automethod:: set_list(is_list: bool) -> JoinedQuery

   .. automethod:: set_outer(is_outer: bool) -> JoinedQuery

Search modifiers & filters
--------------------------

.. autoclass:: SearchModifier()
   :members:
   :exclude-members: from_value, serialise

   .. automethod:: from_value(value: float | int | str) -> SearchModifier

   .. automethod:: serialise(enum_value: int | SearchModifier) -> str

.. autoclass:: SearchTerm(field, value, modifier=SearchModifier.EQUAL_TO)

   .. automethod:: __init__(field: str, value: float | int | str, modifier: SearchModifier = SearchModifier.EQUAL_TO) -> None

   .. automethod:: as_tuple() -> tuple[str, str]

   .. automethod:: infer(field: str, value: float | int | str) -> SearchTerm

   .. automethod:: serialise() -> str

Data classes
------------

The following classes are mostly for internal use, but are provided for type inferrence and introspection.

.. autoclass:: QueryBaseData(**kwargs)
   :members:
   :exclude-members: from_base

   .. automethod:: from_base(data: QueryBaseData) -> QueryBaseData

.. autoclass:: QueryData(**kwargs)
   :members:

.. autoclass:: JoinedQueryData(**kwargs)
   :members:

.. _Census API Primer: https://github.com/leonhard-s/auraxium/wiki/Census-API-Primer
.. _Joined Queries: https://github.com/leonhard-s/auraxium/wiki/Census-API-Primer#joined-queries

"""Low-level Census API wrapper and URL generator.

This module is responsible for generating the URLs used to interface
with the Census API. It is game agnostic and should work for any title
supporting the Daybreak Game Company Census API.
It mostly serves as an internal utility to generate the queries used by
Auraxium's primary, object-oriented interface. It is however completely
stand-alone and can be used on its own.

This module does not perform any queries; it only dynamically generates
the URLs required. Use an HTTP library of your choice to handle the
network side.
When selecting an HTTP library, keep in mind that some API collections,
like ``character`` and ``outfit_member``, can have access times in
excess of several seconds.
For bots and most other use-cases, it is therefore advisable to use an
asynchronous library like `aiohttp`_ to prevent your program from
locking up while waiting for the server to respond.

To generate a census query URL using this module, instantiate a
:class:`Query`, tweak its settings as desired and finally call the
:meth:`Query.url()` method. This will return a :class:`yarl.URL`
instance that can be used as-is or cast to :class:`str`.

Queries come in two flavours, :class:`Query` for top-level queries, and
and :class:`JoinedQuery` for inner, joined queries (aka. joins). Both
inherit from :class:`QueryBase`, which defines shared utility present
in both sub classes.

You can also use one query as a template when creating another, which
can be helpful when building large, deeply nested queries. See the
:meth:`QueryBase.copy()` method for details.

Example:
    This snippet will look up a character by name and return their
    online status.

    .. code-block:: python3

        from auraxium import census

        query = census.Query('character')
        query.add_term(field='name.first_lower', value='auroram')
        join = query.create_join('characters_online_status')
        join.inject_at = 'online_status'
        print(query.url())

    :meth:`Query.url()` returns a :class:`yarl.URL` instance, which you
    would generally pass to your HTTP library of choice, rather than
    printing it.

.. _aiohttp:
    https://docs.aiohttp.org/en/stable/

"""

from .query import JoinedQuery, Query, QueryBase
from .support import SearchModifier, SearchTerm

__all__ = [
    'JoinedQuery',
    'Query',
    'QueryBase',
    'SearchModifier',
    'SearchTerm'
]

__version__ = '0.1.0'

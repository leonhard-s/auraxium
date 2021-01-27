The Census Module
=================

The Census module, located at :mod:`auraxium.census`, is responsible for generating the URLs used to interface with the Census API. It is game agnostic and should work for any title supporting the `Daybreak Game Company Census API <http://census.daybreakgames.com/>`_. It mostly serves as an internal utility to generate the queries used by Auraxium’s primary, object-oriented interface. It is however completely stand-alone and can be used on its own.

This module does not perform any queries; it only dynamically generates the URLs required. Use an HTTP library of your choice to handle the network side.

.. note::

   When selecting an HTTP library, keep in mind that some API collections, like ``character`` and ``outfit_member``, can have access times in excess of several seconds.

   For bots and most other use-cases, it is therefore advisable to use an asynchronous library like :mod:`aiohttp` to prevent your program from locking up while waiting for the server to respond.

Usage
-----

To generate a census query URL using this module, instantiate a Query, tweak its settings as desired and finally call the :meth:`Query.url()` method. This will return a :class:`yarl.URL` instance that can be used as-is or cast to :class:`str`.

Queries come in two flavours, :class:`Query` for top-level queries, and and :class:`JoinedQuery` for inner, joined queries (aka. joins). Both inherit from :class:`QueryBase`, which defines shared utility present in both sub classes.

You can also use one query as a template when creating another, which can be helpful when building large, deeply nested queries. See the :meth:`QueryBase.copy()` method for details.

Example
-------

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

API Reference
-------------

.. autoclass:: auraxium.census.Query
   :members:

.. autoclass:: auraxium.census.JoinedQuery
   :members:

.. autoclass:: auraxium.census.QueryBase
   :members:

.. autoclass:: auraxium.census.SearchModifier
   :members:

.. autoclass:: auraxium.census.SearchTerm
   :members:
   
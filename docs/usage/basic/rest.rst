===============
Auraxium Client
===============

All of Auraxium's API interactions are performed through the :class:`auraxium.Client` class, which contains a few essential references, like the current event loop, the connection pool, or the unique service ID used to identify your app.

.. note::

   You can use the default value of ``s:example`` for testing, but you may run into rate limiting issues if your app generates more than 5-6 queries a minute.

   You can apply for your custom service ID here; the process is free, and you usually hear back within a few hours.

Retrieving Data
===============

.. note::

   The game-specific object representations for PlanetSide 2 reside in the :mod:`auraxium.ps2` submodule. Refer to the `Object Model Documentation <api/ps2.html>`_ for details.

The :class:`auraxium.Client` class exposes several methods used to access the REST API data, like :meth:`~auraxium.Client.get()`, used to return a single match, or :meth:`~auraxium.Client.find()`, used to return a list of matching entries.

It also provides some utility methods, like :meth:`~auraxium.Client.get_by_id()` and :meth:`~auraxium.Client.get_by_name()`. They behave much like the more general :meth:`~auraxium.Client.get()` but are generally preferrably for performance as they use an internal TLRU cache to keep recently used objects in local storage.

This means that repeatedly accessing an object through :meth:`~auraxium.Client.get_by_id()` will only generate network traffic once, after which it is retrieved from cache:

.. code-block:: python3

   import asyncio
   import auraxium
   from auraxium import ps2

   async def main():
       async with auraxium.Client() as client:

           char = await client.get_by_name(ps2.Character, 'auroram')
           print(char.name)
           print(char.data.prestige_level)

           # NOTE: Any methods that might incur network traffic are asynchronous.
           # If the data type has been cached locally, no network communication
           # is required and the coroutine will be done with no delay.

           # This will only generate a request once per faction, as the faction
           # data type is cached forever by default
           print(await char.faction())

           # The online status is never cached as it is bound to change at any
           # moment.
           print(await char.is_online())

   asyncio.get_event_loop().run_until_complete(main())

==============================
Optimizing With Custom Queries
==============================

This document covers how to improve performance for expensive requests that slow down your application.

It is therefore highly advisable to read the `Census API Primer`_ in the repository Wiki before continuing, as well as the usage instructions for Auraxium's :doc:`URL Generator <../basic/census>`.

.. note::

   The optimizations explained herein are likely not needed unless you are sending out hundreds of requests a second and are already running into bottlenecks.

Motivation
==========

The Auraxium object model makes the API more accessible and facilitates traversal of its relations, but in return gives up some flexibility of the original Daybreak Games Census API.

One such optimization are `Joins`_, a means of bundling multiple related queries into a single request, similar to how SQL joins allow returning data from multiple tables. This allows requesting a lot of data in a single query, like resolving particular statistics for outfit members of a particular rank.

Due to their dynamic nature, joins are not available through the object model, but are fully supported by the :mod:`auraxium.census` module, which Auraxium uses to generate the URLs needed to access the Census API.

The following sections will cover how to move between the object model and URL generator, how to parse and validate the payloads received, and how to convert the bulk data retrieved back into the object model representation.

Generating Custom URLs
======================

You can generate a :class:`auraxium.census.Query` representation for any persistent object in the object model using the :meth:`Ps2Object.query <auraxium.base.Ps2Object.query>` method:

.. code-block:: python3
   :emphasize-lines: 3

   client = auraxium.Client()
   char = await client.get_by_name(auraxium.ps2.Character, 'Higby')
   char_query = char.query()

   print(char_query)
   # https://census.daybreakgames.com/s:example/get/ps2:v2/character?character_id=5428072203494645969

In this case, the created query is identical to this:

.. code-block:: python3

   query = auraxium.census.Query('character', character_id=5428072203494645969)

This query can now be customized as per the :mod:`auraxium.census` module API.

For the purposes of this example, we will return the online status of all of a character's friends; an operation that is not possible in a single operation when using the object model:

.. code-block:: python3

   def get_online_friends(char: auraxium.ps2.Character) -> yarl.URL:
       """Return the online friends of the given character."""
       query = char.query()

       # Join the characters' friends
       join = query.create_join('characters_friend')
       join.set_inject_at('friends')

       return query.url()

Since :mod:`auraxium.census` only generates URLs, we cannot use it to perform the HTTP request itself.

While you can pass this :class:`yarl.URL` directly to an :mod:`aiohttp` session, it is recommended to use the :meth:`auraxium.Client.request` method instead to allow the client to log and monitor the performance of this request, as well as trigger the appropriate exceptions for any API issues encountered.

This requires us to switch to a coroutine, as well as pass the client instance to the function:

.. code-block:: python3
   :emphasize-lines: 1-2,10

   async def get_online_friends(char: auraxium.ps2.Character,
                         client: auraxium.Client) -> dict[str, Any]:
       """Return the online friends of the given character."""
       query = char.query()

       # Join the characters' friends
       join = query.create_join('characters_friend')
       join.set_inject_at('friends')

       return await client.request(query)

Running this method yields us a dictionary containing the API's response payload, the parts we are interested in are highlighted:

.. code-block:: python3
   :emphasize-lines: 12,14,17,19

   {
       'character_list': [
           {
               'character_id': '...',
               'name': {...},
               ...
               'character_id_join_characters_friend': {
                   'character_id': '...',
                   ...
                   'friend_list': [
                       {
                           'character_id': '...',
                           'last_login_time': '...',
                           'online': '0'
                       },
                       {
                           'character_id': '...',
                           'last_login_time': '...',
                           'online': '0'
                       },
                       ...
                   ]
               }
           }
       ],
       'returned': 1
   }

Let's add a list comprehension to filter the friends list by their online status:

.. code-block:: python3
   :emphasize-lines: 3,13-14,16

   async def get_online_friends(char: auraxium.ps2.Character,
                                client: auraxium.Client
                                ) -> list[int]:
       """Return the online friends of the given character."""
       query = char.query()

       # Join the characters' friends
       join = query.create_join('characters_friend')
       join.set_inject_at('friends')

       data = await client.request(query)
       friends_data = data['character_list'][0]['friends']['friend_list']
       online_ids = [
           int(f['character_id']) for f in friends_data if int(f['online']) != 0]

       return online_ids

This now returns a list of character IDs that are in the input character's friends list and online.

Converting Census Payloads
==========================

In the previous section, we created a custom function that retrieves the IDs of the friends of a player that are currently online.

However, it would be more convenient if we could have it return a list of :class:`auraxium.ps2.Character` instances instead. We could of course pass these IDs into a helper like :meth:`auraxium.Client.find()` to resolve them, but we can do better by including the data needed to create these instances in the same query.

.. note::

   This strategy is lower-latency as it only uses a single query, but it also significantly increases bandwidth due to the character data being retrieved for all friends, not just online ones. This trade-off between latency and payload size can generally not be avoided when working with joins.

To achieve this, another join is added to the friends list, which will contain the full character payload for each friend (even offline ones, but most players' friends lists should be short enough for this to not affect performance).

.. code-block:: python3
   :emphasize-lines: 3,11-14,18-19,21

   async def get_online_friends(char: auraxium.ps2.Character,
                                client: auraxium.Client
                                ) -> list[dict[str, Any]]:
       """Return the online friends of the given character."""
       query = char.query()

       # Join the characters' friends
       join = query.create_join('characters_friend')
       join.set_inject_at('friends')

       # Join the friends' character
       char_join = join.create_join('character')
       char_join.set_fields('friend_list.character_id', 'character_id')
       char_join.set_inject_at('character')

       data = await client.request(query)
       friends_data = data['character_list'][0]['friends']['friend_list']
       online_friends = [
           f['character'] for f in friends_data if int(f['online']) != 0]

       return online_friends

This now returns a list of payloads compatible with the ``character`` collection. We can therefore feed these payloads directly into the :class:`auraxium.ps2.Character` class's constructor:

.. literalinclude:: ../../../examples/get_online_friends.py
   :start-at: async def
   :end-at: return
   :emphasize-lines: 2,20

That's it - this type of method now behaves exactly the same as any built-in helper method like :meth:`auraxium.ps2.Character.get_online` and should play along nicely with other instances and object model utilities.

.. _Census API Primer: https://github.com/leonhard-s/auraxium/wiki/Census-API-Primer
.. _Joins: https://github.com/leonhard-s/auraxium/wiki/Census-API-Primer#joined-queries

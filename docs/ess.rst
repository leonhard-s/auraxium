Event Streaming
===============

In addition to the REST interface wrapped by Auraxium's object model, PlanetSide 2 also exposes a websocket interface that can be used to stream in-game events in next to real time.

The Auraxium client supports this endpoint through a trigger/action system, explained below.

Triggers
--------

To receive data through the event stream, you must define a trigger. A trigger is made up of three things:

* One or more **events** that tells it to wake up
* Any number of **conditions** that decide whether to run or not
* An **action** that will be run if the conditions are met

Events
------

Events are pre-defined things happening in-game that can be listened to. You can find the list of events in the streaming service `documentation <https://census.daybreakgames.com/#what-is-websocket>`_, as well as in the documentation for the :class:`auraxium.EventType` enumerator.

.. note::

    Some events, like ``ContinentUnlock``, are currently broken on Daybreak's side. Do your own tests before investing too much time, things break a lot with the event streaming API.

The event :attr:`auraxium.EventType.GAIN_EXPERIENCE` allows for further filtering due to the very large number of event responses it can generate. See :meth:`auraxium.EventType.filter_experience()` method for details.

Conditions
----------

Trigger conditions can be attached to a trigger to limit what events it will respond to, in addition to the event type.

This is useful if you have a commonly encountered event (like :attr:`EventType.DEATH`) and would like your action to only run if the event data matches some other requirement (for example "the killing player must be part of my outfit").

Conditions can either be a variable or attribute that evaluates to True or False, or a callable that takes in the payload dictionary received through the websocket and returns True or False depending on its contents.

.. code-block:: python3

    valid_character_ids = [5428072203494645969, ...]

    def check_killer_id(payload: Dict[str, str]) -> bool:
        """Example condition that compares the payload's killing player."""
        assert payload['event_name'] == 'Death'
        char_id = int(payload['attacker_character_id'])
        return char_id in valid_character_ids

Actions
-------

The trigger's action is a method or function that will be run when a matching event is encountered and all of the trigger's conditions are met.

If the action is a coroutine according to :meth:`asyncio.iscoroutinefunction()`, it will be awaited. You can therefore use both regular methods and coroutines as trigger actions.

The only argument passed to the function set as the trigger action is the event received:

.. code-block:: python3

    async def example_action(event: Event) -> None:
        """Example function to showcase the signature used for actions.

        Keep in mind that this could also be a regular function (i.e. one
        defined without the "async" keyword).
        """
        # Do stuff here

Registering Triggers
--------------------

The easiest way to register a trigger to the client is via the :meth:`auraxium.EventClient.trigger()` decorator. It takes the event/s to listen for as the arguments and creates a trigger using the decorated function as the trigger action.

.. note::
    
    Keep in mind that the websocket connection will be continuously looping, waiting for new events to come in.

    This means that using :class:`auraxium.EventClient()` as a context manager may cause issues since the context manager will close the connection when the context manager is exited.

Here is an example trigger setup:

.. code-block:: python3

    import asyncio
    import auraxium
    from auraxium import ps2

    loop = asyncio.get_event_loop()

    async def main():
        # NOTE: Depending on player activity, this script will likely exceed the
        # ~6 requests per minute and IP address limit for the default service ID.
        client = auraxium.EventClient(service_id='s:example')

        @client.trigger(auraxium.EventType.BATTLE_RANK_UP)
        async def print_levelup(event):
            char_id = event.character_id
            char = await client.get_by_id(ps2.Character, char_id)

            # NOTE: This value is likely different from char.data.battle_rank as
            # the REST API tends to lag by a few minutes.
            new_battle_rank = event.battle_rank

            print(f'{await char.name_long()} has reached BR {new_battle_rank}!')

    loop.create_task(main())
    loop.run_forever()

API Reference
-------------

.. autoclass:: auraxium.Trigger
    :members:

.. autoclass:: auraxium.EventType
    :members:

    .. automethod:: auraxium.EventType.from_event_name
        :noindex:
    .. automethod:: auraxium.EventType.from_payload
        :noindex:
    .. automethod:: auraxium.EventType.filter_experience
        :noindex:

.. autoclass:: auraxium.Event
    :members:

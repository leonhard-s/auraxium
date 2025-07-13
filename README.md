# <img src="https://raw.githubusercontent.com/leonhard-s/auraxium/master/assets/icon_256.png" align="left" height="140"/>Auraxium

Auraxium is an object-oriented, pure-Python wrapper for the [PlanetSide 2](https://www.planetside2.com/) API.  
It provides a simple object model that can be used by players and outfits without requiring deep knowledge of the API and its idiosyncrasies.

![PyPI - License](https://img.shields.io/pypi/l/auraxium)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/leonhard-s/auraxium/ci-testing.yaml?label=tests)
[![Coveralls github branch](https://img.shields.io/coveralls/github/leonhard-s/auraxium/master)](https://coveralls.io/github/leonhard-s/auraxium)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/auraxium)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/leonhard-s/auraxium/publish-pypi.yaml)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/leonhard-s/auraxium)](https://www.codefactor.io/repository/github/leonhard-s/auraxium)
[![PyPI](https://img.shields.io/pypi/v/auraxium)](https://pypi.org/project/auraxium/)
[![Read the Docs](https://img.shields.io/readthedocs/auraxium)](https://auraxium.readthedocs.io/en/latest/)

***

- Clean, Pythonic API
- Asynchronous endpoints to keep apps responsive during high API load
- Low-level interface for more optimised, custom queries
- Support for the real-time event streaming service (ESS)
- User-configurable caching system
- Fully type annotated

The documentation for this project is hosted at [Read the Docs](https://auraxium.readthedocs.io/en/latest/).

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Boilerplate Code](#boilerplate-code)
- [Usage](#usage)
  - [Retrieving Data](#retrieving-data)
  - [Event Streaming](#event-streaming)
- [Technical Details](#technical-details)
  - [Object Hierarchy](#object-hierarchy)
  - [Caching](#caching)
  - [Network Connections](#network-connections)
- [Object Model Alternatives](#object-model-alternatives)
- [Contributing](#contributing)

## Overview

The [Census API](https://census.daybreakgames.com/) used by PlanetSide 2 is powerful, but its design also carries a steep learning curve that makes a lot of basic API interactions rather tedious.

Auraxium streamlines this by hiding the game-agnostic queries behind an object model specific to PlanetSide 2. Whenever data is accessed that is not currently loaded, the library dynamically generates and performs the necessary queries in the background before resuming execution.

All queries that may incur network traffic and latency are asynchronous, which keeps multi-user applications - such as Discord bots - responsive.

## Getting Started

All API interactions are performed through the [`auraxium.Client`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.Client) object. It is the main endpoint used to interact with the API and contains a few essential references, like the current event loop, the connection pool, or the unique service ID used to identify your app.

> **Regarding service IDs:** You can use the default value of `s:example` for testing, but you may run into rate limiting issues if your app generates more than ~10 queries a minute.
>
> You can apply for your custom service ID [here](https://census.daybreakgames.com/#devSignup); the process is free, and you usually hear back within a few hours.

Some of these references are also required for any queries carried out behind the scenes, so the client object is also handed around behind the scenes; be mindful when updating them as this may cause issues with ongoing background queries.

### Boilerplate code

The aforementioned [`auraxium.Client`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.Client) object must be closed using the [`auraxium.Client.close()`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.Client.close) method before it is destroyed to avoid issues.

Alternatively, you can use the asynchronous context manager interface to automatically close it when leaving the block:

```py
import auraxium

async with auraxium.Client() as client:
    # Your code here
```

Since Auraxium is an asynchronous library, we also need to wrap our code in a coroutine to be able to use the `async` keyword.

This gives us the following snippet:

```py
import asyncio
import auraxium

async def main():
    async with auraxium.Client() as client:
        # Your code here

asyncio.run(main())
```

With that, the stage is set for some actual code.

## Usage

The game-specific object representations for PlanetSide 2 can be found in the `auraxium.ps2` sub module. Common ones include `ps2.Character`, `ps2.Outfit`, or `ps2.Item`.

> **Note:** The original data used to build a given object representation is always available via that object's `.data` attribute, which will be a type-hinted, [named tuple](https://docs.python.org/3/library/collections.html#collections.namedtuple).

### Retrieving Data

The `auraxium.Client` class exposes several methods used to access the REST API data, like [`Client.get()`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.Client.get), used to return a single match, or [`Client.find()`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.Client.find), used to return a list of matching entries.

It also provides some utility methods, like [`Client.get_by_id()`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.Client.get_by_id) and [`Client.get_by_name()`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.Client.get_by_name). They behave much like the more general [`Client.get()`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.Client.get) but are cached to provide better performance for common lookups.

This means that repeatedly accessing an object through [`.get_by_id()`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.Client.get_by_id) will only generate network traffic once, after which it is retrieved from cache (refer to the [Caching](#caching) section for more information).

Here is the above boilerplate code again, this time with a simple script that prints various character properties:

```py
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
        # is required.

        # This will only generate a request once per faction, as the faction
        # data type is cached forever by default.
        print(await char.faction())

        # The online status is never cached as it is bound to change at any
        # moment.
        print(await char.is_online())

asyncio.run(main())
```

## Event Streaming

In addition to the REST interface wrapped by Auraxium's object model, PlanetSide 2 also exposes an event stream that can be used to react to in-game events in next to real time.

This can be used to track outfit member performance, implement your own stat tracker, or monitor server population.

The Auraxium client supports this endpoint through a trigger-action system.

### Triggers

To receive data through the event stream, you must define a trigger. A trigger is made up of three things:

- One or more **events** that tells it to wake up
- Any number of **conditions** that decide whether to run or not
- An **action** that will be run if the conditions are met

#### Events

The event type definitions are available in the [`auraxium.event`](https://auraxium.readthedocs.io/en/latest/api/event.html#event-types) namespace.

#### Conditions

Trigger conditions can be attached to a trigger to limit what events it will respond to, in addition to the event type.

This is useful if you have a commonly encountered event (like [`event.DEATH`](https://auraxium.readthedocs.io/en/latest/api/event.html#auraxium.event.DEATH)) and would like your action to only run if the event data matches some other requirement (for example "the killing player must be part of my outfit").

#### Actions

The trigger's action is a method or function that will be run when the event fires and all conditions evaluate to True.

If the action is a coroutine according to [`inspect.iscoroutinefunction()`](https://docs.python.org/3/library/inspect.html#inspect.iscoroutinefunction), it will be awaited.

The only argument passed to the function set as the trigger action is the event received:

```py
async def example_action(event: Event) -> None:
    """Example function to showcase the signature used for actions.

    Keep in mind that this could also be a regular function (i.e. one
    defined without the "async" keyword).
    """
    # Do stuff here
```

### Registering Triggers

The easiest way to register a trigger to the client is via the [`auraxium.event.EventClient.trigger()`](https://auraxium.readthedocs.io/en/latest/api/event.html#auraxium.event.EventClient.trigger) decorator. It takes the event/s to listen for as the arguments and creates a trigger using the decorated function as the trigger action.

> **Important:** Keep in mind that the websocket connection will be continuously looping, waiting for new events to come in.
>
> This means that using [`auraxium.event.EventClient()`](https://auraxium.readthedocs.io/en/latest/api/event.html#auraxium.event.EventClient) as a context manager may cause issues since the context manager will close the connection when the context manager is exited.

```py
import asyncio
from auraxium import event, ps2

async def main():
    # NOTE: Depending on player activity, this script will likely exceed the
    # ~6 requests per minute and IP address limit for the default service ID.
    client = event.EventClient(service_id='s:example')

    @client.trigger(event.BattleRankUp)
    async def print_levelup(evt):
        char = await client.get_by_id(ps2.Character, evt.character_id)

        # NOTE: This value is likely different from char.data.battle_rank as
        # the REST API tends to lag by a few minutes.
        new_battle_rank = evt.battle_rank

        print(f'{await char.name_long()} has reached BR {new_battle_rank}!')

loop = asyncio.new_event_loop()
loop.create_task(main())
loop.run_forever()
```

## Technical Details

The following section contains more detailed implementation details for those who want to know; it is safe to ignore if you are only getting started.

### Object Hierarchy

All classes in the Auraxium object model inherit from `Ps2Object`. It defines the API table and ID field to use for generic queries and implements methods like `.get()` or `.find()`.

#### Cache Objects

Cached objects are based off the `Cached` class, which introduces a class-specific cache for matching instances before falling back to the regular implementation.

It also adds methods for updating the class cache settings at runtime.

See the [Caching](#caching) section for details on the caching system.

#### Named Objects

Named objects are based off the `Named` class and always cached. This base class guarantees a `.name`] attribute and allows the use of the [`.get_by_name()`](https://auraxium.readthedocs.io/en/latest/api/rest.html#auraxium.base.Named.get_by_name) method, which is also cached.

This caching strategy is almost identical to the one used for IDs, except that it uses a string constructed of the lower-case name and locale identifier to store objects (e.g. `'en_sunderer'`).

### Caching

Auraxium uses timed least-recently-used (TLRU) caches for its objects.

They have a size constraint (i.e. how many objects may be cached at any given time), as well as a maximum age per item (referred to as TTU, "time-to-use"). The TTU is used to ensure frequently used items are updated occasionally and not too far out of date.

When new items are added to the cache, it first removes any expired items (i.e. `time_added - now > ttu`).
It then removes as many least-recently-used items as necessary to accommodate the new elements.

The LRU side of things is implemented via an [`collections.OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict); every time an item is retrieved from the cache (and is not expired), it is moved back to the start of the dictionary, the last items of the dictionary are then chopped off as needed.

### Network Connections

For as long as it is active, the `auraxium.Client` object will always have a [`aiohttp.ClientSession`](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession) running in case the REST API must be accessed.

The websocket connection, which is required for event streaming, is only active when there are triggers registered and active.

If the last trigger is removed, the websocket connection is quietly closed after a delay. If a new trigger is added, it will automatically be recreated in the background.

## Object Model Alternatives

For some users or applications, Auraxium's object model may be a bad fit, like for highly nested, complex queries or for users that are already familiar with the Census API.

Here are a few Python alternatives for these cases:

- The URL generator used by Auraxium to generate the queries for the object model can also be used on its own.

    This still requires *some* understanding of the Census API data model but takes away the syntactic pitfalls involved.

    It only generates queries, so you will have to pick your own flavour of HTTP library (like [requests](https://requests.readthedocs.io/en/master/) or [aiohttp](https://docs.aiohttp.org/en/stable/)) to make the queries.

    ```py
    """Usage example for the auraxium.census module."""
    from auraxium import census

    query = census.Query('character', service_id='s:example')
    query.add_term('name.first_lower', 'auroram')
    query.limit(20)
    join = query.create_join('characters_online_status')
    url = str(query.url())

    print(url)
    # https://census.daybreakgames.com/s:example/get/ps2:v2/character?c:limit=20&c:join=characters_online_status
    ```

    Refer to the [census module documentation](https://auraxium.readthedocs.io/en/latest/usage/basic/census.html) for details.

- For an even simpler syntax, you can check out [spascou/ps2-census](https://github.com/spascou/ps2-census), which was inspired by an earlier version of Auraxium.

    It too sticks closely to the original Census API, but also provides methods for retrieving the queried data.

    It also features a query factory system that allows creation of common queries from templates.

    ```py
    """Usage example for spascou's ps2-census module."""
    import ps2_census as ps2

    query = ps2.Query(ps2.Collection.CHARACTER, service_id='s:example')
    query.filter('name.first_lower', 'auroram')
    query.limit(20)
    query.join(ps2.Join(ps2.Collection.CHARACTERS_ONLINE_STATUS))

    print(query.get())
    # {'character_list': [...], 'returned': 1}
    ```

    Refer to the [ps2-census documentation](https://github.com/spascou/ps2-census#query-building) for details.

## Contributing

If you have found a bug or would like to suggest a new feature or change, feel free to get in touch via the [repository issues](https://github.com/leonhard-s/auraxium/issues).

Please check out [CONTRIBUTING.md](https://github.com/leonhard-s/auraxium/blob/master/CONTRIBUTING.md) before opening any pull requests for details.

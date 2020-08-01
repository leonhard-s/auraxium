# <img src="assets/icon_256.png" align="left" height="140"/>Auraxium

Auraxium is an object-oriented, pure-Python wrapper for the [PlanetSide 2](https://www.planetside2.com/) API.\
It provides a simple object model that can be used by players and outfits without requiring deep knowledge of the API and its idiosyncrasies.

***

- Clean, Pythonic API.
- Asynchronous endpoints keep apps **responsive** during high API load
- Low-level interface for more optimised, custom queries.
- User-configurable **caching** system.
- Fully type annotated.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Boilerplate Code](#boilerplate-code)
- [Usage](#usage)
  - *Under construction*
- [Object Model Alternatives](#object-model-alternatives)
- [Contributing](#contributing)

## Overview

The [Census API](https://census.daybreakgames.com/) used by PlanetSide 2 is powerful, but its design also carries a steep learning curve that makes a lot of basic API interactions rather tedious.

Auraxium streamlines this by hiding the game-agnostic queries behind an object model specific to PlanetSide 2. Whenever data is accessed that is not currently loaded, the library dynamically generates and performs the necessary queries in the background before resuming execution.

All queries that may incur network traffic and latency are asynchronous, which keeps multi-user applications - such as Discord bots - responsive.

## Getting Started

All API interactions are performed through the `auraxium.Client` object. It is the main endpoint used to interact with the API and contains a number of essential references, like the current event loop, the connection pool, or the unique service ID used to identify your app.

> **Regarding service IDs:** You can use the default value of `s:example` for testing, but you may run into rate limiting issues if your app generates more than 5-6 queries a minute.
>
> You can apply for your custom service ID [here](https://census.daybreakgames.com/#devSignup); the process is free and you usually hear back within a few hours.

Some of these references are also required for any queries carried out behind the scenes, so the client object is also handed around behind the scenes; be mindful when updating them as this may cause issues with ongoing background queries.

### Boilerplate code

The aforementioned `auraxium.Client` object must be closed using the `auraxium.Client.close()` method before it is destroyed to avoid issues.

Alternatively, you can use the context manager interface to automatically close it when leaving the block:

```py
import auraxium

with auraxium.Client() as client:
    # Your code here
```

Since Auraxium is an asynchronous library, we also need to wrap our code in a coroutine to be able to use the `async` keyword.

This gives us the following snippet:

```py
import asyncio
import auraxium

async def main():
    with auraxium.Client() as client:
        # Your code here

asyncio.run_until_complete(main())
```

With that, the stage is set for some actual code.

## Usage

The game-specific object representations for PlanetSide 2 can be found in the `auraxium.ps2` sub module. Common ones include `Character`, `Outfit`, or `Item`.

> **Note:** The original data used to build a given object representation is always available via that object's `.data` attribute, which will be a type-hinted, [named tuple](https://docs.python.org/3/library/collections.html#collections.namedtuple).

A lot of object representations are linked through methods. For example, you can use `Weapon.item()` to retrieve the item data for a given weapon, or `Item.weapon()` to get back to the associated weapon.

### Under Construction

This project is still undergoing development, and a lot of features and endpoints are not yet implemented.

Take this final snippet for inspiration and refer to source code introspection for details:

```py
import asyncio
import auraxium

async def main():
    with auraxium.Client() as client:

        item = await client.get(auraxium.ps2.Item, name__en='*Pulsar')
        # Get a list of classes that can use this item
        users = [p.data.description for p in await item.profiles()]
        users_str = ', '.join(users[:-1]) + ', and ' + users[-1]
        category = (await item.category()).data.name.en
        print(f'The {item.name()} is a(n) {category} usable by {users_str}.')

asyncio.run_until_complete(main())
```

## Object Model Alternatives

For some users or applications, Auraxium's object model may be a bad fit, like for highly nested, complex queries or for users that are already familiar with the Census API.

Here are a few Python alternatives for these cases:

- The URL generator used by Auraxium to generate the queries for the object model can also be used on its own.

    This still requires *some* understanding of the Census API data model, but takes away the syntactic pitfalls involved.

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

    Refer to the [census module documentation](https://auraxium.readthedocs.io/en/latest/) for details.

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

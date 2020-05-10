# <img src="assets/icon_256.png" align="left" height="140"/>Auraxium

Auraxium is a Python wrapper for the [Daybreak Game Company Census API](https://census.daybreakgames.com/). While its core components have been designed to work with any title using the Census API syntax, it is mainly being developed and tested with [PlanetSide 2](https://www.planetside2.com/) in mind.

***

## Overview

Auraxium's goal is to facilitate the use of the API without compromising functionality. This is achieved by first instantiating an object representing the query to perform, which then generates the URL required.

This functionality is available for all games that support the original Census API.

For PlanetSide 2, it additionaly provides <!--[an object-oriented interface](#object-model) as well as -->a client for the PlanetSide 2 [Event Streaming Service](https://census.daybreakgames.com/#what-is-websocket) (ESS).

## How to use

This section provides basic usage examples for the API wrapper. For a proper how-to and detailed examples, check out to [the Auraxium wiki](https://github.com/leonhard-s/auraxium/wiki) instead. The following snippets are only meant to showcase the syntax.

**Note:** Testing for namespaces other than `ps2` (i.e. PlanetSide 2, PC version) has been either extremely basic or simply non-existant. If you would like to expand the current tests to cover other games or namespaces, [do feel free to contribute](#contributing).

### Basic requests

Requests are defined by instantiating a `Query` object and passing it the collection to access, as well as the game namespace to use, like `ps2`, `dcuo` or `eq2`.

Any remaining keyword arguments will be interpreted as field/value pairs to pass to the query. To generate the URL and retrieve the response, use the `Query.get()` method.

```py
import auraxium

# Retrieve and print the PlanetSide 2 weapon with the ID "22"
my_query = auraxium.Query('weapon', namespace='ps2', weapon_id='22')
print(my_query.get())
```

**Note:** Double-underscores will be interpreted as dots, which can be used to access subkeys in your queries. See the next section for an example.

### Query commands

Query commands like `c:sort` or `c:join` are represented through methods of the `Query` object.

To illustrate, the following is a compound query that retrieves a weapon by name, which requires two nested joins to achieve in a single request:

```py
import auraxium

# Get the weapon's item by name
my_query = auraxium.Query('item', namespace='ps2', name__en='^Orion')
# Attach the intermediate query to the item
my_join = my_query.join('item_to_weapon', on='item_id', to='weapon_id')
# Attach an inner query to the intermediate one
my_join.join('weapon', on='weapon_id', to='weapon_id')
# Generate the URL and return the response
print(my_query.get())
```

<!--
## Object model

This submodule provides an object-oriented access point where Queries are mostly happening in the background. This is especially useful for cases where a user needs to browse the game data without being familiar with the API and its collections.

Currently, this is only implemented for PlanetSide 2.

**Example:**

```py
import auraxium
from auraxiumm.object_models import ps2

# Get a character by name (case-insensitive by default)
my_char = ps2.Character.get_by_name('auroram')

# Return various attributes of the character
print('Name: ' + my_char.name)
print('Server: ' + my_char.world.name.en)
```

In this example, `my_char.name` access the `name_first` field of the character whereas `my_char.world.name.en` returns the English localization of the server name, which has been quietly retrieved in the background.
-->
## Contributing

If you found a bug or would like to suggest a new feature, feel free to [create an issue](https://github.com/leonhard-s/auraxium/issues).

That said, while I am passionate about this project, the amount of time I can dedicate to it is limited.
So if you are the coding type, feel free to just [fork away](https://github.com/leonhard-s/auraxium/fork) and see how things go. :blush:

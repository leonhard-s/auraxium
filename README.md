# Notice

This wrapper is currently undergoing a near-complete rewrite due to a number of poor decisions. I highly advise you come back in a week or two and see if this message has been removed.

# Auraxium

A Python wrapper meant to facilitate the use of the [Daybreak Game Company Census API](https://census.daybreakgames.com/). While the API is compatible with a number of different DBG titles, this module is currently only being developed and tested for use with [PlanetSide 2](https://www.planetside2.com/).

**Disclaimer: All elements of this repository are still undergoing heavy modification. Using this code for anything more serious than having a play-around with the API is currently not advisable.**

## Overview

Auraxium provides an object-oriented way of generating and performing Census API requests that is easier to work with than the stock API syntax.

It also contains a basic client for the PlanetSide 2 [Event Streaming Service](https://census.daybreakgames.com/#what-is-websocket) (ESS), which can be used to respond to in-game events in next to real time, without the performance problems arising from repeatedly polling the data through standard API requests.

## Requirements

**Python Version**
Auraxium is currently being developed in parallel with a [Discord](https://discordapp.com/) bot and is therefore tested using Python 3.6 for compatibility with bot-specific modules. Run higher versions at your own risk.

**Packages**
The following non-standard packages are required by Auraxium:

- [requests](https://github.com/requests/requests) is always required.
- [websockets](https://github.com/aaugustin/websockets) is only required if you need ESS functionality.

## How to use

This section provides examples for the main uses of Auraxium. More specific examples can be found in the `examples/` subfolder of the repository and are explained in the [examples wiki page](https://github.com/leonhard-s/auraxium/wiki/Examples).

### Basic requests

The core methods used for accessing the API are `find()`, `get()`, and `count()`, used for generating the requests, and `call()`, which performs the request and returns an object containing the server's response.

* `find()` returns a list of all matching entries
* `get()` returns the first (and possibly only) matching entry
* `count()` only returns the number of matching entries

The following example retrieves a character by name and prints basic information about them in the console.

```py
import auraxium as arx

# This is the name of the player we want to look up
character_name = 'Auroram'
# Only show these fields
fields_to_show = ['battle_rank.value', 'faction_id', 'name.first',
                  'prestige_level', 'times.creation_date']

response = arx.get('character',
                   terms=('name.first_lower', character_name.lower()),
                   show=fields_to_show).call()
print(response)
```

The output of the `print` statement is analogous to the following JSON code:

```json
{
	"name": { "first": "Auroram" },
	"faction_id": "1",
	"times": { "creation_date": "2013-05-11 17:06:10.0" },
	"battle_rank": { "value": "41" },
	"prestige_level": "1"
}
```

### Joined queries

The Census API provides the option of joining multiple queries together, even across data types. In Auraxium, this functionality is provided through the `join()` method, which can be used on both basic requests and existing joins.

To illustrate this, we will be looking up an outfit by its tag and print the names of its members. This means looking up the outfit's ID, searching the outfit member collection for matching entries and finally looking up the names of the characters.

```py
import auraxium as arx

# The outfit tag to search by
OUTFIT_TAG = 'L3GN'

# Generate the base request
request = arx.get('outfit',
                  terms=('alias_lower', OUTFIT_TAG.lower()),
                  show=['outfit_id', 'name'])
# Attach the outfit member list to the outfit
inner_join = request.join('outfit_member',
                          list=True,
                          show='character_id',
                          match='outfit_id')
# Attach the name of the outfit member to the joined request
inner_join.join('character_name',
                match='character_id',
                show='name.first')

# Perform the request
response = request.call()

# Print the member list
print('Members of outfit "{}":'.format(response['name']))
print(response['outfit_member_list'])
```

### Event streaming

The following things are required to use the ESS system:
1. Creating a client, thus opening a websocket connection.
2. Subscribe to the in-game events you want to have forwarded to your client.
3. Define code to run whenever such an event is received.

The following snippet creates an ESS client and subscribes to all login and logout events for the Cobalt server. It then prints messages depending on the event type detected.

```py
import asyncio

import auraxium as arx
from auraxium.events import ESSClient

# World 13 = "Cobalt" server
WORLD_ID = '13'

# 1. Create an event streaming client and open a connection
essc = ESSClient(sid='s:example')

# 2. Inform the ESS that we would like to receive login and logoff events
essc.subscribe(events='PlayerStatus', worlds=WORLD_ID)

# 3. Whenever any event is received, run this function
@essc.event
async def on_event(event):
  # Resolve the character id into the player name
  player_name = arx.resolve_player(event.response['character_id'])
  if event.event_name == 'login':
    print('{} logged in.'.format(player_name))
  else:
    print('{} logged out.'.format(player_name))
```

## Further reading

More information, along with proper documentation, can be found in the [Auraxium Wiki](wiki).

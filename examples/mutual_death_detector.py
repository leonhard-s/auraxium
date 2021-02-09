# type: ignore
# pylint: disable=unused-variable
"""Example for detecting mutual deaths between players.

This script showcases using the event client to detect mutual deaths
between players; i.e. two players killing each other at (nearly) the
same time.
"""

import asyncio
import datetime
from typing import Dict, Tuple

import auraxium

# The maximum time difference between kills for them to be considered mutual.
MUTUAL_DEATH_WINDOW = 5.0


async def main() -> None:
    """Main script method."""
    # Instantiate the event client
    client = auraxium.EventClient(service_id='s:example')

    # This dictionary is used to track recent deaths
    cache: Dict[int, Tuple[int, datetime.datetime]] = {}

    @client.trigger(auraxium.EventType.DEATH)
    async def on_death(event: auraxium.Event) -> None:
        """Run whenever a death event is received."""
        now = event.timestamp
        victim_id = event.character_id
        killer_id = event.attacker_character_id

        # Ignore deaths not caused by enemy players
        if killer_id == 0 or victim_id == killer_id:
            return

        # Remove outdated kills from cache
        for cache_killer, cache_data in list(cache.items()):
            cache_victim, cache_timestamp = cache_data
            age = now - cache_timestamp
            if age.total_seconds() > MUTUAL_DEATH_WINDOW:
                del cache[cache_killer]

        # Check remaining cache items for mutual deaths
        for cache_killer, cache_data in cache.items():
            cache_victim, _ = cache_data
            if (cache_killer, cache_victim) == (victim_id, killer_id):
                # Mutual death found!

                # Get the names of the players involved
                ids = ','.join((str(i) for i in (killer_id, victim_id)))
                results = await client.find(
                    auraxium.ps2.Character, character_id=ids)
                if not results:
                    # Ignore events if you cannot resolve the player names
                    return
                victim, killer = results

                # Get the name of the server these players are on
                server = await victim.world()

                print(f'{now}: [{server}] - Mutual death between '
                      f'{victim.name()} and {killer.name()}')

                # Remove cache item as it was "consumed" for this mutual death
                del cache[cache_killer]
                return

        # No match found, add current event to cache instead
        cache[killer_id] = victim_id, now

if __name__ == '__main__':

    # NOTE: Be sure to use `run_forever()` rather than `run_until_complete()`
    # when using the event client, otherwise the client would shut down as soon
    # as the `main()` method finishes.

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

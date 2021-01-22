# type: ignore
# pylint: disable=unused-variable
"""Print whenever any player receives a new battle rank."""

import asyncio
import auraxium


async def main():
    # NOTE: Depending on player activity, this script may exceed the ~6
    # requests per minute and IP address limit for the default service ID.
    client = auraxium.EventClient(service_id='s:example')

    @client.trigger(auraxium.EventType.BATTLE_RANK_UP)
    async def print_levelup(event: auraxium.Event):
        char_id = int(event.payload['character_id'])
        char = await client.get_by_id(auraxium.Character, char_id)

        # NOTE: This value is likely more up-to-date than the one from the
        # char.battle_rank attribute.
        new_battle_rank = int(event.payload['battle_rank'])

        print(f'{await char.name_long()} has reached BR {new_battle_rank}!')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

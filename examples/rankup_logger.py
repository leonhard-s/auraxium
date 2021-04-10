"""Print whenever any player receives a new battle rank."""

import asyncio

import auraxium
from auraxium import event, ps2


async def main():
    # NOTE: Depending on player activity, this script may exceed the ~6
    # requests per minute and IP address limit for the default service ID.
    client = auraxium.EventClient(service_id='s:example')

    @client.trigger(event.BattleRankUp)
    async def print_levelup(evt: event.BattleRankUp):
        char = await client.get_by_id(ps2.Character, evt.character_id)

        # Brand new characters may not be available in the API yet
        if char is None:
            print('Skipping anonymous player')
            return

        # NOTE: This value is likely more up-to-date than the one from the
        # char.battle_rank attribute.
        print(f'{await char.name_long()} has reached BR {evt.battle_rank}!')

    _ = print_levelup

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

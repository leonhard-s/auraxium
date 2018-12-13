# EVENT STREAMING TEST
# --------------------
# This script opens a websocket connection and subscribes to select events for
# a particular outfit's members.

import asyncio
import logging

from auraxium import *

# INITIALIZATION
# --------------

# Create a logger
logger = logging.getLogger('auraxium')
logger.setLevel(logging.DEBUG)
# Create a file handler
fh = logging.FileHandler('auraxium.log')
fh.setLevel(logging.DEBUG)
# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# Create a formatter
fh.setFormatter(logging.Formatter(
    '[%(asctime)s] (%(name)s) - [%(levelname)s] %(message)s'))
# Create a formatter
ch.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# Initialize worksheets
sheet_killspam = sheets.Sheet('Killspam')
sheet_killspam.range(1, 1, 5).values = [
    'Timestamp', 'Victim', 'Killer', 'Weapon', 'Note']

# Set our custom service id
# census.service_id = 's:auraxiumdiscordbot'
census.service_id = 's:MUMSOutfitRoster'

# Instantiate the asyncio loop
loop = asyncio.get_event_loop()

# Create an event streaming client
event_client = events.Client()

# SUBSCRIBE TO EVENTS
# -------------------

OUTFIT_ALIAS = 'MUMS'
# Generate a request for all outfit member names and character ids
request = census.get(collection='outfit',
                     terms={'field': 'alias_lower',
                            'value': OUTFIT_ALIAS.lower()},
                     show=['alias', 'name', 'outfit_id'])
member = request.join('outfit_member', list=True, show='character_id')
member.join('character_name', match='character_id', show='name.first')
# Create a dict of the data returned
member_dict = {
    member['character_name']['name']['first']: member['character_id']
    for member in request.call()['outfit_list'][0]['outfit_member_list']}
# Subscribe to death events using the list generated
event_client.subscribe('Death', character_list=member_dict.values())

# ADD EVENT LISTENERS
# -------------------


@event_client.event
async def on_death(event):
    """Runs when a death event is received."""
    victim = census.get('character_name',
                        terms={'field': 'character_id',
                               'value': event['character_id']}
                        ).call()['character_name_list'][0]['name']['first']
    if event['attacker_character_id'] == "0":
        attacker = 'their own poor life choices'
    else:
        attacker = census.get('character_name',
                              terms={'field': 'character_id',
                                     'value': event['attacker_character_id']}
                              ).call()['character_name_list'][0]['name']['first']
    if event['attacker_weapon_id'] == "0":
        weapon = 'Natural Causes'
    else:
        weapon = census.get('item',
                            terms={'field': 'item_id',
                                   'value': event['attacker_weapon_id']}
                            ).call()['item_list'][0]['name']['en']

    print('{} was killed by {} using {}.'.format(
        victim, attacker, weapon))

    # Check for team kills
    if event['character_id'] in member_dict.values() and event['attacker_character_id'] in member_dict.values():

        if event['character_id'] == event['attacker_character_id']:
            values = [event['timestamp'], victim, attacker, weapon, 'Suicide']

        else:
            values = [event['timestamp'], victim, attacker, weapon, 'Teamkill']

            # Auroram has died to the powers of Newtonian Physics.
            # MegaCakeKnight was brutally stabbed to death by X.
            # Spidey has been farmed by X using Banshee (Mosquito Nose Gun)
            # SOMEONE has been blown up by PERSON using C-4.

    else:
        values = [event['timestamp'], victim, attacker, weapon]

    sheet_killspam.append_row(values)

# RUN EVENT LOOP
# ----------------

# Queue connect and run the loop
loop.create_task(event_client.connect())
try:
    loop.run_forever()
except RuntimeError:
    pass

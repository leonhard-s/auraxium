# EVENT STREAMING TEST
# --------------------
# This script opens a websocket connection and subscribes to select events for
# a particular outfit's members.

import asyncio
import logging

from auraxium import *

# Create a logger
logger = logging.getLogger('auraxium')
logger.setLevel(logging.DEBUG)
# Create a file handler
fh = logging.FileHandler('auraium.log')
fh.setLevel(logging.DEBUG)
# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# Create a formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


# Set our custom service id
# census.service_id = 's:auraxiumdiscordbot'

# Instantiate the asyncio loop
loop = asyncio.get_event_loop()

# The outfit who's members will be tracked
OUTFIT_ALIAS = 'mums'

# Generate a request for an outfit with this alias
request = census.get(collection='outfit',
                     terms={'field': 'alias_lower', 'value': OUTFIT_ALIAS},
                     show=['alias', 'name', 'outfit_id'])
# Attach a request for outfit's member list
member = request.join('outfit_member', list=True, show='character_id')
# Attach a request for the member's name
member.join('character_name', match='character_id', show='name.first')
# Create a dict of all outfit members and their ingame name
member_dict = {
    member['character_name']['name']['first']: member['character_id']
    for member in request.call()['outfit_list'][0]['outfit_member_list']}


# Create an event streaming client
event_client = events.Client()

# Subscribe to all outfit member death events
event_client.subscribe('Death', character_list=member_dict.values())


# @event_client.event
# def on_event(event):
#     """Runs whenever any message is received."""


@event_client.event
def on_death(event):
    """Runs when a death event is received."""
    victim = census.get('character_name',
                        terms={'field': 'character_id',
                               'value': event['character_id']}
                        ).call()['character_name_list'][0]['name']['first']
    attacker = census.get('character_name',
                          terms={'field': 'character_id',
                                 'value': event['attacker_character_id']}
                          ).call()['character_name_list'][0]['name']['first']
    weapon = census.get('item',
                        terms={'field': 'item_id',
                               'value': event['attacker_weapon_id']}
                        ).call()['item_list'][0]['name']['en']

    print('[DEATH] {} was killed by {} using {}.'.format(
        victim, attacker, weapon))


# Queue connect and run the loop
loop.create_task(event_client.connect())
try:
    loop.run_forever()
except RuntimeError:
    pass

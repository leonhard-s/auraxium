import datetime
import logging

import discord

from . import census

# Create a logger
logger = logging.getLogger('auraxium.embed')


def generate_embed(embed_identifier, string):
    if embed_identifier == 'weapon_info':
        embed = discord.Embed(title='Weapon info: {}'.format(
            item['name']['en']), colour=discord.Colour(0x7e49a2))

        embed.set_image(
            url='https://census.daybreakgames.com{}'.format(item['image_path']))
        # Select depending on empire
        embed.set_thumbnail(
            url='https://census.daybreakgames.com/files/ps2/images/static/90.png')
        embed.set_footer(
            text='Embed generated using Planetside 2 Census API data. | Enter ?help for instructions.')

        embed.add_field(name='Description', value=item['description']['en'])
        rpm = round(60000 / int(weapon_datasheet['fire_rate_ms']))
        embed.add_field(name='Damage profile', value='Fires {} rounds per minute, dealing {} damage each.'.format(
            rpm, weapon_datasheet['damage'], ))
        # embed.add_field(name='Accuracy', value='567 rounds per minute')
        embed.add_field(name='Ammunition', value='{} round magazine, {} rounds total. {} s short reload, {} s long reload.'.format(
            weapon_datasheet['clip_size'], weapon_datasheet['capacity'], round(int(weapon_datasheet['reload_ms']) / 1000, 2), round(int(weapon_datasheet['reload_ms_max']) / 1000, 2)))
        # embed.add_field(name='Attachments', value='Flash suppressor, Compensator, Forward grip and High velocity ammunition.')

    # ?outfit
    elif embed_identifier == 'outfit':
        req = census.Request('outfit', contains=string, field='name_lower',
                             hide=['alias_lower', 'time_created_date', 'leader_character_id'])
        req.join('character', inject_at='leader', show=['faction_id'])
        sub = req.join('outfit_member', list=True, inject_at='Members',
                       hide=['outfit_id', 'member_since_date'])
        sub.join('character_name', on='character_id', inject_at='character',
                 show=['name.first'])
        response = req.retrieve()
        logger.debug(response)

        embed = discord.Embed(title="Outfit info: Members of the Utopian Mummy", colour=discord.Colour(
            0xc76ded), description="Members of the Utopian Mummy (MUMS) is a VS outfit on Cobalt. It has 49 members with a median Battle Rank of 38.", timestamp=datetime.datetime.utcfromtimestamp(1540460311))

        embed.set_thumbnail(
            url="https://census.daybreakgames.com/files/ps2/images/static/90.png")
        embed.set_author(name="Auroram requested:",
                         icon_url="https://cdn.discordapp.com/embed/avatars/4.png")
        embed.set_footer(text="Embed generated using current Census API data")

        embed.add_field(name="Mummy", value="MegaCakeKnight")
        embed.add_field(name="Daddy", value="Skyie and Spider")
        embed.add_field(name="Son", value="kaph")
        embed.add_field(
            name="Daughter", value="Auroram, bidul127, factbat, Hopecatcher, jonaspiloot, n00bgobbler, LukeAntras and 7 more")
        embed.add_field(
            name="Newborn", value="Bestwish, lingchi, rampage sniper, sonstwas, WigoJ and 24 more")

    else:
        embed = 0
        logger.warning('Panic!')
    return embed

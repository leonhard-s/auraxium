import asyncio

import discord
from openpyxl import Workbook

# All functions defined this module will be accessible to bot users.

# Initialize Excel worksheets
wb = Workbook()
ws = wb.active


# def online(msg, words, help=False):
#     # if msg, words[0] '-help':
#     #     test = 'Displays a msg, words of all online outfit members. If no tag is ' +
#     #     'specified, the default - MUMS - will be used instead.\n' +
#     #     '?online [OUTFIT]'
#     print('The command "?online" is not yet implemented.')


# def help(msg, words, help=False):
#     if help:
#         return 'Displays a list of available commands.'

# async def census(client, msg, words, help=False):
# """Generic command for looking up information about ingame data."""

# Warn users that more specific commands exist
# (weaponinfo, outfitroster, playerinfo, etc.)

# ?census player/character/char Auroram

# Player name
# Battle rank & ASP
# outfit
# Empire
# Server
# 3 top weapons
# Primary roles (add role if playtime(30d) over 10h?) or just top 2-3

# async def player(client, msg, words, help=False):
#     """Displays basic information about a player."""
#
#     _battle_rank = "17"
#     _asp = " (ASP)"
#     _faction_icon_url = ""
#     _kdr = "2.05"
#
#     _outfit_name =
#     _outfit_tag =
#     _outfit_join_date =
#     _outfit_rank =
#     _outfit_rank_ordinal =
#
#     _top_weapon_1_name =
#     _top_weapon_1_type =
#     _top_weapon_1_kills =
#     _top_weapon_2_name =
#     _top_weapon_2_type =
#     _top_weapon_2_kills =
#     _top_weapon_3_name =
#     _top_weapon_3_type =
#     _top_weapon_3_kills =
#
#     _top_domain_1_name =
#     _top_domain_1_hours =
#     _top_domain_2_name =
#     _top_domain_2_hours =
#     _top_domain_3_name =
#     _top_domain_3_hours =
#
#     embed = discord.Embed(title="Auroram", colour=discord.Colour(
#         0x34f4d6), description="Vanu Sovereignty combatant on Cobalt.")
#
#     embed.set_thumbnail(url=_faction_icon_url)
#     embed.set_author(name="Player information:")
#     embed.set_footer(text="\"Look, Mega - no hands!\"")
#
#     embed.add_field(name="Basic information", value="Battle rank: 17 (ASP)\nKDR: 2.04".format(
#         _battle_rank, _asp, _kdr))
#     embed.add_field(
#         name="Outfit", value="Members of the Utopian Mummy (MUMS)\nJoined 08/10/2018.\nRank: \"Son\" (tier 5).")
#     embed.add_field(name="Top weapons",
#                     value="#1 - C4 - [Explosive] - 2406 kills\n#2 - Force blade - [Knife] - 1206 kills\n#3 - Pulsar LSW - [LMG] - 1202 kills")
#     embed.add_field(name="Most played",
#                     value="Combat Medic - 300 hours\nHeavy Assault - 260 hours\nSunderer - 120 hours")
#
#     await bot.say(content="Here is the information you requested, {}:".format(msg.author.mention), embed=embed)


async def echo(client, msg, words, help=False):
    """Repeats the rest of the user's message."""

    await client.send_message(msg.channel, content=msg.content[5:])


async def juicy(client, msg, words, help=False):
    """Forwards any message send to the user Spidey to the #living-room channel.
    These two values are hard-coded as I do not see any reason to extend this
    functionality.
    """

    # Hard-coding, best coding!
    DEST_CHANNEL = client.get_channel('483582158993096704')
    USER_SPIDEY = await client.get_user_info('243477509520359427')

    # Help text
    if help:
        return ('Any message prefixed with this command will be '
                'forwarded to the {} channel while also mentioning '
                'Spidey.').format(DEST_CHANNEL.mention)

    # If the author does not have an avatar set, use their respective default
    author_icon_url = msg.author.avatar_url
    if author_icon_url == '':
        author_icon_url = msg.author.default_avatar_url

    # Generate the embed
    embed = discord.Embed(colour=discord.Colour(0x8452ae),
                          description=msg.content[6:],
                          timestamp=msg.timestamp)
    embed.set_author(name=msg.author.display_name, icon_url=author_icon_url)
    embed.set_footer(text='# {}'.format(msg.channel.name))

    # Send the message
    await client.send_message(DEST_CHANNEL,
                              content=USER_SPIDEY.mention,
                              embed=embed)

    elif words[0] == 'clear':
        # Clear any notifications for this user
        if < user exist >:
            # Tell them you removed their entry
            pass
        else:
            # Tell them there is nothing to remove
            pass

    else:
        # Complain about usage
        pass


async def steal_that_bastards_avatar(client, msg, words, help=False):
    """Retrieves a user based on their discord name and posts their avatar."""

    help_text = 'Usage: ?steal_that_bastards_avatar CHANNEL_MENTION USER_MENTION'

    # Get the user
    user = words[0]

    # The number of messagesto
    messages = 1000

    # username#discriminator
    name, discriminator = words[0].split('#')

    # Cycle through the messages
    user_hash = ''
    async for message in client.logs_from(msg.channel, limit=messages):
        if message.author.name == name and message.author.discriminator == discriminator:
            user_hash = message.author.id
            break

    # If no user was found
    if user_hash == '':
        content = ('{} I was unable to find a user matching the '
                   'criteria.').format(msg.author.mention)

        await client.send_message(msg.channel, content=content)
        return
    else:
        user = await client.get_user_info(user_hash)
        content = '{} I found a match: {}.'.format(msg.author.mention,
                                                   user.avatar_url)
        await client.send_message(msg.channel, content=content)


async def so_sad(client, msg, words, help=False):
    """Alexa, this is so sad."""

    pass

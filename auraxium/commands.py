import asyncio

import discord


async def echo(client, msg, words, help=False):
    """Repeats the rest of the user's message."""

    await client.send_message(msg.channel, content=msg.content[5:])


async def shutdown(client, msg, words, help=False):
    """Ends the asyncio loop."""

    await client.send_message(msg.channel, content='Shutting down... bye!')
    await client.close()


async def dinnerTime(client, msg, words, help=False):
    """Moves members into the voice channel of the user sending the command.

    Any user that has been mentioned in this message and is connected to a
    voice channel in the current server will be moved to the voice channel of
    the user who sent the command.
    """

    # Check permissions
    role = discord.utils.get(msg.server.roles, name='Son')
    if msg.author.top_role < role:
        content = ('Sorry {}, you need to have the rank of {} or higher to '
                   'use this command.').format(msg.author.mention, role.name)
        await client.send_message(msg.channel, content=content)
        return

    # Get the channel to move members into
    if msg.author.voice.voice_channel == None:
        content = '{} You are not connected to a voice channel.'.format(
            msg.author.mention)
        await client.send_message(msg.channel, content=content)
        return
    else:
        author_channel = msg.author.voice.voice_channel

    # Create a list of all users that have been mentioned in this message
    mentioned_users = [m for m in msg.server.members if m.mentioned_in(msg)]

    # Get a list of all non-afk members in voice channels
    voice_users = [m for c in msg.server.channels if len(
        c.voice_members) > 0 for m in c.voice_members]

    # Get a list of all members that are both mentioned and in voice channels
    members_to_move = [
        m for m in mentioned_users if m in voice_users and not m in author_channel.voice_members and not m.voice.is_afk]

    if len(members_to_move) == 0:
        content = '{} I was unable to find members that can be moved to {}.'.format(
            msg.author.mention, author_channel.name)
        await client.send_message(msg.channel, content=content)
        return
    elif len(members_to_move) == 1:
        content = '{} Moving 1 member to {}.'.format(
            msg.author.mention, author_channel.name)
        await client.send_message(msg.channel, content=content)
    else:
        content = '{} Moving {} members to {}.'.format(
            msg.author.mention, len(members_to_move), author_channel.name)
        await client.send_message(msg.channel, content=content)

    for member in members_to_move:
        await client.move_member(member, author_channel)


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
    embed.set_author(name=msg.author.display_name,
                     icon_url=author_icon_url)
    embed.set_footer(text='# {}'.format(msg.channel.name))

    # Send the message
    await client.send_message(DEST_CHANNEL,
                              content=USER_SPIDEY.mention,
                              embed=embed)


async def ping(client, msg, words, help=False):
    """Useful for testing whether a bot has permission to use a channel.

    If the bot responds "Pong!", it has seen the message and can reply.
    """

    await client.send_message(destination=msg.channel,
                              content='{} Pong!'.format(msg.author.mention))

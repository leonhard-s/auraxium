import asyncio
import logging

import discord

from .sheets import Sheet, base_path

# Initialize worksheets
sheet_notifications = Sheet('Notifications')
sheet_notifications.range(1, 1, 3).values = ['Timestamp', 'Username', 'Value']

# Create a logger
logger = logging.getLogger('auraxium.commands')


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


async def notify(client, msg, words, help=False):
    """Allows discord users to announce their absence."""

    author_fmt = '{}#{}'.format(msg.author.name, msg.author.discriminator)

    user_row = sheet_notifications.find_in_column(column=2, value=author_fmt)

    # Mark as absent
    if len(words) == 0:
        reply = 'Please provide an argument. Usage: `?notify absent|late|list|clear`'

    elif words[0] == 'absent':
        # If the user already has an entry in the worksheet
        if user_row > 0:
            cell = sheet_notifications.cell(row=user_row, column=3)
            if cell.value == 'Notified absent':
                # Tell them that you already marked them
                reply = 'You are already notified absent.'
            else:
                # Overwrite whatever they had
                cell.value = 'Notified absent'
                reply = 'Copy that, I changed you to notified absent.'
        else:
            # Add a new entry for the user
            sheet_notifications.append_row(
                [msg.timestamp, author_fmt, 'Notified absent'])
            reply = 'Copy that, I marked you as notified absent.'

    # Mark as late
    elif words[0] == 'late':
        # If the user already has an entry in the worksheet
        if user_row > 0:
            cell = sheet_notifications.cell(row=user_row, column=3)
            if cell.value == 'Notified late':
                # Tell them that you already marked them
                reply = 'You are already notified late.'
            else:
                # Overwrite whatever they had
                cell.value = 'Notified late'
                reply = 'Copy that, I changed you to notified late.'
        else:
            # Add a new entry for the user
            sheet_notifications.append_row(
                [msg.timestamp, author_fmt, 'Notified late'])
            reply = 'Copy that, I marked you as notified late.'

    # List notifications
    elif words[0] == 'list':
        if user_row != 0:
            # Remove their entry
            cell = sheet_notifications.cell(row=user_row, column=3)
            if cell.value == 'Notified absent':
                reply = 'You have been marked as notified absent.'
            else:
                reply = 'You have been marked as notified late.'
        else:
            # Tell them there is nothing to remove
            reply = 'There are no notifications for you.'

    # Clear notifications
    elif words[0] == 'clear':
        if user_row != 0:
            # Remove their entry
            sheet_notifications.delete_row(user_row)
            reply = 'Copy that, I cleared any notifications for you.'
        else:
            # Tell them there is nothing to remove
            reply = 'There are no notifications for you.'

    # Complain about usage
    else:
        reply = ('Wait, what?\nPlease make sure you only write `?notify '
                 'absent|late|list|clear` and nothing else.')

    await client.send_message(destination=msg.channel,
                              content='{} {}'.format(msg.author.mention, reply))


async def ping(client, msg, words, help=False):
    """Useful for testing whether a bot has permission to use a channel.

    If the bot responds "Pong!", it has seen the message and can reply.
    """

    await client.send_message(destination=msg.channel,
                              content='{} Pong!'.format(msg.author.mention))

import asyncio

import discord

from auraxium import *

# Create the bot
arx = discord.Client()

# Instantiate the asyncio loop
loop = asyncio.get_event_loop()

loop.create_task(
    arx.start('NTAyMTA2NjI4MzAxMTI3Njk2.DqjIUw.2cCUogbo0DXvUZhM9UzhH_707uo'))


# Login message
@arx.event
async def on_ready():
    print('Auraxium bot ready.')


# Member welcome message
@arx.event
async def on_member_join(member):
    # The channel to welcome members in
    channel = arx.get_channel('483579698811764748')
    content = ('Hey there {}, welcome to MUMS!\nDo keep in mind that we hold '
               'Ops at 20:00 CET Friday through Sunday. Ops is a more '
               'serious, tactical platoon for which we do take a register. '
               'So if you cannot attend, please let us know as far ahead as '
               'you can.').format(member.mention)
    await arx.send_message(channel, content)


# Message seen
@arx.event
async def on_message(msg):
    """Runs whenever a message is sent in a channel.

    Only triggers for channels the bot has read permission for.
    """

    # Only respond to strings starting with this string, ignore any others
    _BOT_SIGN = '?'

    # DEBUG: Prints debug information in the console.
    print('Debug: New message by "{}" ({}) in "{}" ({}).'.format(
        msg.author.name, msg.author.id,
        msg.channel.name, msg.channel.id))

    message = msg.content

    # Only continue if the message starts with the bot's command prefix
    if not message.startswith(_BOT_SIGN):
        return
    # Remove the command prefix from the message
    message = message[len(_BOT_SIGN):]

    # The first word is the command
    cmd = message.split()[0]

    # Anything after the command is our remaining input. The "+1" takes care of
    # the whitespace after the command word
    input = message[len(cmd) + 1:].strip()

    # Loop through the remaining input and seperate it into words
    word_list = []
    while len(input) > 0:
        # Get the indexes of the next special character
        index_space = input.find(' ')  # Space
        index_s_quote = input.find('\'')  # Single quote: '
        index_d_quote = input.find('"')  # Double quotes: "

        # If there are no special characters in the remaining string
        if index_space == -1 and index_s_quote == -1 and index_d_quote == -1:
            # Add the remaining text to the word list
            word_list.append(input)
            break

        # If the next special character is a space
        elif (index_space < index_s_quote or index_s_quote == -1) and (
                index_space < index_d_quote or index_d_quote == -1):
            # Add the next word
            word_list.append(input[:index_space])
            input = input[index_space + 1:]

        # If the next special character is a single quote
        elif index_s_quote < index_d_quote or index_d_quote == -1:
            # Find the matching quote
            matching_quote = input.find('\'', index_s_quote + 1)
            if matching_quote != -1:
                # Add the text inbetween quotes
                word_list.append(input[index_s_quote + 1:matching_quote])
            # TODO: Unmatched quote handling and warning
            input = input[matching_quote + 1:].strip()

        # If the next special character is a double quote
        elif index_d_quote != -1:
            # Find the matching quote
            matching_quote = input.find('"', index_d_quote + 1)
            if matching_quote != -1:
                # Add the text inbetween quotes
                word_list.append(input[index_d_quote + 1:matching_quote])
            # TODO: Unmatched quote handling and warning
            input = input[matching_quote + 1:].strip()
        else:
            print('ERROR')
            break

    # Try to find a command with the specified name
    try:
        command = eval('commands.{}'.format(cmd))
    except AttributeError:
        print('Unknown command: "{}".'.format(cmd))
        # Tell the user that this is an invalid command
        return

    # Run the command
    await command(arx, msg, word_list)


# If the loop is not already running, start it
try:
    loop.run_forever()
except RuntimeError:
    pass

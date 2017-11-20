
import asyncio
import os
import json
from datetime import datetime
from tzlocal import get_localzone
import discord
from group import group

client = discord.Client()
groups = []

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith('!b create'):
        yield from create_group(message)
    elif message.content.startswith('!b join'):
        yield from join_group(message)
    elif message.content.startswith('!b list'):
        yield from list_groups(message)


def create_group(message):
    group_type = 0
    yield from client.send_message(message.author, "Group Type? (Raid(R), Trials(T), Nightfall(NF))")
    pc = get_private_channel(message.author)
    print(pc)
    msg = yield from client.wait_for_message(channel=pc, author=message.author)
    print(msg.content)
    if msg.content.lower() == 'r' or msg.content.lower() == 'raid':
        group_type = 0
        raid_name = ''
        raid_time = None
        yield from client.send_message(pc, 'Raid Name?')
        msg = yield from client.wait_for_message(channel=pc, author=message.author)
        raid_name = msg.content
        yield from client.send_message(pc, 'Time? (if today just enter time in 24 hour time (HH:MM) otherwise DD/MM/YYYY HH:MM (24 time)')
        msg = yield from client.wait_for_message(channel=pc, author=message.author)
        if len(msg.content) == 5:
            hour = int(msg.content[0:2])
            minute = int(msg.content[3:])
            today =  datetime.today()
            raid_time = datetime(today.year, today.month, today.day, hour=hour, minute=minute, tzinfo=get_localzone())
        else:
            timestr = msg.content.strip()
            day = int(timestr[0:2])
            month = int(timestr[3:5])
            year = int(timestr[6:10])
            hour = int(timestr[11:13])
            minute = int(timestr[14:16])
            raid_time = datetime(year, month, day, hour, minute, tzinfo=get_localzone())
        print(raid_time.strftime('%A, %d. %B %Y %I:%M%p %z'))
        raid_group = group(raid_name, message.author.id, message.author.display_name, raid_time, 6)
        groups.append(raid_group)
        yield from print_group_info(message.channel, raid_group)
    elif msg.content.lower() == 't' or msg.content.lower() == 'trials':
        pass
    elif msg.content.lower() == 'nf' or msg.content.lower() == 'nightfall':
        pass

def join_group(message):
    user = message.author
    group_name = message.content[8:]
    for g in groups:
        if g.name == group_name:
            for member in group.members:
                if member[0] == user.id:
                    yield from client.send_message(message.channel, 'You are already in this group.')
                    return
            else:
                g.add_member(user.id, user.display_name)
                yield from print_group_info(message.channel, g)
                return
    yield from client.send_message(message.channel, 'Group Not Found.')

def get_private_channel(user):
    for pc in client.private_channels:
        print(len(pc.recipients))
        if len(pc.recipients) == 1 and user in pc.recipients:
            return pc
    return None

def print_group_info(channel, groupObj):
    message = '```md'
    message += groupObj.group_info_string_long()
    message += '```'
    yield from client.send_message(channel, message)
    print('Message Sent')

def list_groups(channel):
    message = '```md'
    for groupObj in groups:
        message += groupObj.group_info_string_short()
    message += '```'
    yield from client.send_message(channel, message)
    print('Message Sent')

if os.path.isfile('apikeys.json'):
    with open('apikeys.json') as json_file:
        token = json.load(json_file)["discord"]
elif(os.environ.get('DISCORD_TOKEN') != None):
    token = os.environ.get('DISCORD_TOKEN')
else:
    token = input("You must specify the discord bot token: ")
    os.environ['DISCORD_TOKEN'] = token


while(True):
    try:
        client.run(token)
    except discord.ConnectionClosed:
        print("ConnectionClosed error. Restarting")


import asyncio
import os
import json
from datetime import datetime
from tzlocal import get_localzone
import discord

client = discord.Client()

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
        raid_name = yield from client.wait_for_message(channel=pc, author=message.author)
        yield from client.send_message(pc, 'Time? (if today just enter time in 24 hour time (HH:MM) otherwise DD/MM/YYYY HH:MM (24 time)')
        msg = yield from client.wait_for_message(channel=pc, author=message.author)
        if len(msg.content) == 5:
            hour = int(msg.content[0:2])
            minute = int(msg.content[3:])
            today =  datetime.today()
            raid_time = datetime(today.year, today.month, today.day, hour=hour, minute=minute, tzinfo=get_localzone())
            print(raid_time.strftime('%A, %d. %B %Y %I:%M%p %Z'))


def get_private_channel(user):
    for pc in client.private_channels:
        print(len(pc.recipients))
        print('%s == %s? %s' % (user, pc.recipients[0], user == pc.recipients[0]))
        if len(pc.recipients) == 1 and user in pc.recipients:
            print('Found PC')
            return pc
    return None

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
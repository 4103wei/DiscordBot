# Work with Python 3.6
import discord
import random
import reddit
import json
import asyncio
import wget

# Reading Token
with open('discordLogin.json', 'r') as f:
    datastore = json.load(f)
TOKEN = datastore['token']
client = discord.Client()

async def bg_task():
    await client.wait_until_ready()
    channel = discord.Object(id=datastore['chat_channel_id'])

    subs = ['worldnews', 'trailers', 'livestreamfail', 'dailyshow']
    last_msg = {}
    for sub in subs:
        last_msg[sub] = ''

    initial = 1 # If bot is initialized, he should not send a message
    while not client.is_closed:
        for sub in subs:
            try:
                new_msg = reddit.Reddit.getTopStory(sub=sub, lim=1)
                if last_msg[sub] != new_msg:
                    if initial == 0:
                        await client.send_message(channel, '**' + sub + '**\n' + new_msg)
                    last_msg[sub] = new_msg
            except:
                print('Exception: Fetching from ' + sub)
        initial = 0
        await asyncio.sleep(300)


@client.event
async def on_message(message):
    inmsg = str(message.author) + " in " + str(message.channel) + ": " + str(message.content)
    print(inmsg)

    if message.content.startswith('order random'):
        msg = "AYES TO THE LEFT " + str(random.randint(1,1000)) + " NOES TO THE RIGHT " + str(random.randint(1,1000))
        await client.send_message(message.channel, msg)
    elif message.content.startswith('order anime wallpaper'):
        try:
            url = reddit.Reddit.getRandomStory('animewallpaper')
            await client.send_message(message.channel, url)
            file = wget.download(url=url,out='files/')
            print('Downloaded: ' + file)
        except:
            print('Exception: Order anime wallpaper')
    elif message.content.startswith('order wallpaper'):
        try:
            url = reddit.Reddit.getRandomStory('wallpapers')
            await client.send_message(message.channel, url)
            file = wget.download(url=url, out='files/')
            print('Downloaded: ' + file)
        except:
            print('Exception: Order wallpaper')


    # delete certain messages after x seconds
    if str(message.content).startswith('order'):
        try:
            print(inmsg + ' DELETED.')
            await client.delete_message(message)
        except:
            print("Exception: Delete order message")
    elif '4413'in str(message.author):
        try:
            await asyncio.sleep(60)
            print(inmsg + ' DELETED.')
            await client.delete_message(message)
        except:
            print("Exception: Delete own message")
    elif message.author == client.user:
        try:
            await asyncio.sleep(3600)
            print(inmsg + ' DELETED.')
            await client.delete_message(message)
        except:
            print("Exception: Delete bot message")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.loop.create_task(bg_task())
client.run(TOKEN)
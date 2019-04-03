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

    subs = ['worldnews', 'trailers', 'livestreamfail']
    last_msg = {}
    for sub in subs:
        last_msg[sub] = ''

    initial = 1 # If bot is initialized, he should not send a message
    while not client.is_closed:
        for sub in subs:
            try:
                new_msg = reddit.Reddit.getTopStory(sub=sub, lim=1)
            except:
                print('Something went wrong, fetching from ' + sub)
            if last_msg[sub] != new_msg:
                if initial == 0:
                    await client.send_message(channel, '**' + sub + '**')
                    await client.send_message(channel, new_msg)
                last_msg[sub] = new_msg
                initial = 1
        await asyncio.sleep(600)


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
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
            await client.send_message(message.channel, 'DIVISSSSIIION!!! something went wrong, try again.')
    elif message.content.startswith('order wallpaper'):
        try:
            url = reddit.Reddit.getRandomStory('wallpapers')
            await client.send_message(message.channel, url)
            file = wget.download(url=url, out='files/')
            print('Downloaded: ' + file)
            #await client.send_file(message.channel, file)
        except:
            await client.send_message(message.channel, 'DIVISSSSIIION!!! something went wrong, try again.')


    #elif message.content.startswith('order intensifies'):
    #    await client.send_file(message.channel, 'order.jpg')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.loop.create_task(bg_task())
client.run(TOKEN)
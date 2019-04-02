# Work with Python 3.6
import discord
import random
import reddit
import json
import threading
import asyncio

# Reading Token
with open('discordLogin.json', 'r') as f:
    datastore = json.load(f)
TOKEN = datastore['token']
client = discord.Client()

async def bg_task():
    await client.wait_until_ready()
    latest_news = ""
    latest_trailer = ""
    latest_livestreamfail = ""
    channel = discord.Object(id=datastore['chat_channel_id'])
    while not client.is_closed:
        news = reddit.Reddit.getTopStory(sub='worldnews', lim=1)
        trailer = reddit.Reddit.getTopStory(sub='trailers', lim=1)
        livestreamfail = reddit.Reddit.getTopStory(sub='livestreamfail', lim=1)
        if latest_news != news:
            await client.send_message(channel, "**News**")
            latest_news = news
            await client.send_message(channel, news)
        if latest_trailer != trailer:
            await client.send_message(channel, "**Trailer**")
            latest_trailer = trailer
            await client.send_message(channel, trailer)
        if latest_livestreamfail != livestreamfail:
            await client.send_message(channel, "**LivestreamFail**")
            latest_livestreamfail = livestreamfail
            await client.send_message(channel, livestreamfail)
        await asyncio.sleep(300)


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('order random'):
        msg = "AYES TO THE LEFT " + str(random.randint(1,1000)) + " NOES TO THE RIGHT " + str(random.randint(1,1000))
        await client.send_message(message.channel, msg)
    elif message.content.startswith('order unleash'):
        msg = "ORDAHHHH I SAID ORDAHHHHH"
        await client.send_message(message.channel, msg)
    elif message.content.startswith('order news'):
        msg = reddit.Reddit.getTopStory(sub='worldnews')
        await client.send_message(message.channel, msg)
    elif message.content.startswith('order trailers'):
        msg = reddit.Reddit.getTopStory(sub='trailers')
        await client.send_message(message.channel, msg)
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
# Work with Python 3.6
import discord
import random
import reddit
import json
import asyncio
import wget
import wikipedia


# Reading Setting
with open('setting.json','r') as s:
    setting = json.load(s)
subs = setting['reddit_sub_tracking']
token = setting['discord_token']
announcement_ch_id = setting['discord_chat_channel_id']
client = discord.Client()
reddit = reddit.Reddit(client_id = setting['reddit_client_id'], client_secret = setting['reddit_client_secret'], user_agent = setting['reddit_user_agent'], username = setting['reddit_username'], password = setting['reddit_password'])

# Messages to be deleted
recorded_msg = []



async def bg_task():
    await client.wait_until_ready()
    channel = discord.Object(id=announcement_ch_id)
    last_msg = {}

    for sub in subs:
        last_msg[sub] = ''

    initial = 1 # If bot is initialized, he should not send a message
    while not client.is_closed:
        for sub in subs:
            try:
                new_msg = reddit.getTopStory(sub=sub, lim=1)
                if last_msg[sub] != new_msg:
                    if initial == 0:
                        await client.send_message(channel, '**' + sub + '**\n' + new_msg)
                    last_msg[sub] = new_msg
            except:
                print('Exception: Fetching from ' + sub)
        initial = 0
        await asyncio.sleep(300)


@client.event
async def on_message_delete(message):
    msg = str(message.author) + " in " + str(message.channel) + ": " + str(message.content)
    print(msg + ' DELETED')
    if message in recorded_msg:
        recorded_msg.remove(message)
        print('Msg deleted, # of msg still to be deleted: ' + str(len(recorded_msg)))


@client.event
async def on_reaction_add(reaction, user):
    if reaction.message in recorded_msg:
        recorded_msg.remove(reaction.message)
        print('Msg removed from deletion, # of msg still to be deleted: ' + str(len(recorded_msg)))


@client.event
async def on_message(message):
    try:
        author = '<@' + str(message.author.id) + '>\n'
        if message.content.startswith('order random'):
            msg = "AYES TO THE LEFT " + str(random.randint(1,1000)) + " NOES TO THE RIGHT " + str(random.randint(1,1000))
            await client.send_message(message.channel, author + msg)
        elif message.content.startswith('order anime wallpaper'):
            url = reddit.getRandomStory('animewallpaper')
            await client.send_message(message.channel, author + url)
            file = wget.download(url=url,out='files/')
            print('Downloaded: ' + file)
        elif message.content.startswith('order wallpaper'):
            url = reddit.getRandomStory('wallpapers')
            await client.send_message(message.channel, author + url)
            file = wget.download(url=url, out='files/')
            print('Downloaded: ' + file)
        elif message.content.startswith('order definition '):
            word = str(message.content)[17:]
            print('Search for... ' + word)
            msg = wikipedia.summary(word, sentences=1)
            await client.send_message(message.channel, author + msg)
        elif message.content.startswith('order show tracking'):
            msg = 'Currently tracking following subreddits: '
            for sub in subs:
                msg = msg + sub + ' '
            await client.send_message(message.channel, author + msg)
        elif message.content.startswith('order help'):
            msg = '```css\n' \
                  '[order help: Possible commands]\n' \
                  '[order random: UK parliament will decide for you]\n' \
                  '[order show tracking: Show currently tracked subreddits]' \
                  '[order wallpaper: Returns a wallpaper]\n' \
                  '[order anime wallpaper: Weeb up]\n' \
                  '[order show tracking: Show currently tracked subreddits]' \
                  '[order definition word: Definition of the word]\n```'
            await client.send_message(message.channel, author + msg)
    except:
        print('Error on command: ' + str(message.author) + " in " + str(message.channel) + ": " + str(message.content))



    # delete certain messages after x seconds, message will be recorded until deletion, because message might get deleted before x second.
    try:
        if str(message.content).startswith('order'):
            recorded_msg.append(message)
            await asyncio.sleep(10)
            if message in recorded_msg:
                await client.delete_message(message)
        elif '4413'in str(message.author):
            recorded_msg.append(message)
            await asyncio.sleep(300)
            if message in recorded_msg:
                await client.delete_message(message)
        elif message.author == client.user:
            recorded_msg.append(message)
            await asyncio.sleep(10)
            if message in recorded_msg:
                await client.delete_message(message)
    except:
        print('Error on delete: ' + str(message.author) + " in " + str(message.channel) + ": " + str(message.content))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.loop.create_task(bg_task())
client.run(token)
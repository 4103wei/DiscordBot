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
async def on_message(message):
    inmsg = str(message.author) + " in " + str(message.channel) + ": " + str(message.content)
    print(inmsg)
    author = '<@' + str(message.author.id) + '>\n'
    if message.content.startswith('order random'):
        msg = "AYES TO THE LEFT " + str(random.randint(1,1000)) + " NOES TO THE RIGHT " + str(random.randint(1,1000))
        await client.send_message(message.channel, author + msg)
    elif message.content.startswith('order anime wallpaper'):
        try:
            url = reddit.getRandomStory('animewallpaper')
            await client.send_message(message.channel, author + url)
            file = wget.download(url=url,out='files/')
            print('Downloaded: ' + file)
        except:
            print('Exception: Order anime wallpaper')
    elif message.content.startswith('order wallpaper'):
        try:
            url = reddit.getRandomStory('wallpapers')
            await client.send_message(message.channel, author + url)
            file = wget.download(url=url, out='files/')
            print('Downloaded: ' + file)
        except:
            print('Exception: Order wallpaper')
    elif message.content.startswith('order definition '):
        try:
            word = str(message.content)[17:]
            print('Search for... ' + word)
            msg = wikipedia.summary(word, sentences=1)
            await client.send_message(message.channel, author + msg)
        except:
            try:
                await client.send_message(message.channel, 'Could not find the definition')
            except:
                print('Exception: Order definition')
    elif message.content.startswith('order show tracking'):
        try:
            msg = 'Currently tracking following subreddits: '
            for sub in subs:
                msg = msg + sub + ' '
            await client.send_message(message.channel, author + msg)
        except:
            print('Exception: Order show tracking')
    elif message.content.startswith('order help'):
        try:
            msg = '```css\n' \
                  '[order help: Possible commands]\n' \
                  '[order random: UK parliament will decide for you]\n' \
                  '[order show tracking: Show currently tracked subreddits]' \
                  '[order wallpaper: Returns a wallpaper]\n' \
                  '[order anime wallpaper: Weeb up]\n' \
                  '[order definition word: Definition of the word]\n```'
            await client.send_message(message.channel, author + msg)
        except:
            print('Exception: Order help')



    # delete certain messages after x seconds
    if str(message.content).startswith('order'):
        try:
            await asyncio.sleep(10)
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
client.run(token)
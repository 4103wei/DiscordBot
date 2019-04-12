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
async  def on_member_update(before, after):
    if (str(before.status) == 'offline' and str(after.status) != 'offline'):
        await client.send_message(discord.Object(id=announcement_ch_id), str(before) + ' online.')
    elif (str(before.status) != 'offline' and str(after.status) == 'offline'):
        await client.send_message(discord.Object(id=announcement_ch_id), str(before) + ' offline.')


@client.event
async def on_message_delete(message):
    msg = str(message.author) + " in " + str(message.channel) + ": " + str(message.content)
    print(msg + ' DELETED')
    if message in recorded_msg:
        recorded_msg.remove(message)
    print('# of msg still to be deleted: ' + str(len(recorded_msg)))


@client.event
async def on_reaction_add(reaction, user):
    msg = str(reaction.message.author) + " in " + str(reaction.message.channel) + ": " + str(reaction.message.content)
    print(msg + ' REACTED')
    if reaction.message in recorded_msg:
        recorded_msg.remove(reaction.message)
    print('# of msg still to be deleted: ' + str(len(recorded_msg)))


@client.event
async def on_message(message):
    # recording part
    # message will be put into a list, recorded_msg, all messages inside the list will be deleted at some point
    if str(message.content).startswith('order') or ('4413' in str(message.author)) or (message.author == client.user):
        recorded_msg.append(message)

    # execution part
    # if the message starts with order, something will be executed
    try:
        author = '<@' + str(message.author.id) + '>\n'
        if message.content.startswith('order random'):
            num = random.randint(0,650)
            msg = "AYES TO THE LEFT " + str(num) + " NOES TO THE RIGHT " + str(650-num)
            await client.send_message(message.channel, author + msg)
        elif message.content.startswith('order roll'):
            num = random.randint(1,6)
            await client.send_message(message.channel, str(num))
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
        elif message.content.startswith('order reaction'):
            url = reddit.getRandomStory('animereactionimages')
            await client.send_message(message.channel, author + url)
        elif message.content.startswith('order game'):
            url = reddit.getRandomStory('webgames')
            await client.send_message(message.channel, author + url)
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
                  '[order roll: Roll a dice]\n' \
                  '[order wallpaper: Returns a wallpaper]\n' \
                  '[order anime wallpaper: Weeb up]\n' \
                  '[order reaction: Reaction image]\n' \
                  '[order game: Web game]\n' \
                  '[order show tracking: Show tracked subreddits]\n' \
                  '[order definition word: Definition of the word]\n```'
            await client.send_message(message.channel, author + msg)
    except:
        print('Error on command: ' + str(message.author) + " in " + str(message.channel) + ": " + str(message.content))



    # auto deletion part
    # messages will be deleted after certain time
    try:
        if str(message.content).startswith('order'):
            await asyncio.sleep(10)
            if message in recorded_msg:
                await client.delete_message(message)
        elif '4413'in str(message.author):
            await asyncio.sleep(120)
            if message in recorded_msg:
                await client.delete_message(message)
        elif message.author == client.user:
            await asyncio.sleep(1800)
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

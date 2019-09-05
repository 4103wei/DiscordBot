#! usr/bin/env python3
import praw
import random

class Reddit:
    def __init__(self, client_id, client_secret, user_agent, username, password):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)


    def getTopStory(self, sub = "worldnews", lim=5, preview = False, type = 'rising'):
        wn = self.reddit.subreddit(sub)

        if (type == 'rising'):
            threads = wn.rising(limit=lim)
        elif(type == 'hot'):
            threads = wn.hot(limit=lim)
        else:
            threads = wn.new(limit=lim)

        titles =""
        for thread in threads:
            if (preview):
                titles = titles + '`' + thread.title + '`' + "\n" + thread.url + "\n"
            else:
                titles = titles + '`' + thread.title + '`' + "\n<" + thread.url + ">\n"
        return titles




    def getRandomStory(self, sub = "worldnews"):
        wn = self.reddit.subreddit(sub)
        hot_subreddit = wn.hot(limit=250)
        r = random.randint(1, 250)
        for i, post in enumerate(hot_subreddit):
            if i == r:
                return post.url

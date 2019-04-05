#! usr/bin/env python3
import praw
import json
import random

class Reddit:
    def __init__(self, client_id, client_secret, user_agent, username, password):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)


    def getTopStory(self, sub = "worldnews", lim=5):
        wn = self.reddit.subreddit(sub)
        hot_subreddit = wn.rising(limit=lim)
        titles =""
        for submission in hot_subreddit:
            titles = titles + '`' + submission.title + '`' + "\n<" + submission.url + ">\n"
        return titles


    def getRandomStory(self, sub = "worldnews"):
        wn = self.reddit.subreddit(sub)
        hot_subreddit = wn.hot(limit=500)
        r = random.randint(1, 500)
        for i, post in enumerate(hot_subreddit):
            if i == r:
                return post.url

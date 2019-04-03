#! usr/bin/env python3
import praw
import json
import random

class Reddit():
    @staticmethod
    def getTopStory(sub = "worldnews", lim=5):
        '''
        fetch the top rising stories from given subreddit
        :param sub: subreddit (string)
        :param lim: int (number of stories)
        :return: titles together with url as a string
        '''
        with open('redditLogin.json', 'r') as f:
            datastore = json.load(f)
        reddit = praw.Reddit(client_id=datastore['client_id'],
                             client_secret=datastore['client_secret'],
                             user_agent=datastore['user_agent'],
                             username=datastore['username'],
                             password=datastore['password'])

        wn = reddit.subreddit(sub)
        hot_subreddit = wn.rising(limit=lim)
        titles =""
        for submission in hot_subreddit:
            titles = titles + '`' + submission.title + '`' + "\n<" + submission.url + ">\n"
        return titles


    @staticmethod
    def getRandomStory(sub = "worldnews"):
        '''
        fetch a random story from given subreddit
        :param sub: subreddit (string)
        :return: url as string
        '''
        with open('redditLogin.json', 'r') as f:
            datastore = json.load(f)
        reddit = praw.Reddit(client_id=datastore['client_id'],
                             client_secret=datastore['client_secret'],
                             user_agent=datastore['user_agent'],
                             username=datastore['username'],
                             password=datastore['password'])

        wn = reddit.subreddit(sub)
        hot_subreddit = wn.hot(limit=500)
        r = random.randint(1, 500)
        for i, post in enumerate(hot_subreddit):
            if i == r:
                return post.url

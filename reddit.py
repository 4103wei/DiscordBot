#! usr/bin/env python3
import praw
import json

class Reddit():
    @staticmethod
    def getTopStory(sub = "worldnews", lim=5):
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
            titles = titles + '`' + submission.title + '`' + "\n" + submission.url + "\n"
        return titles

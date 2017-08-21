#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 15:35:15 2017
Get max. amount of tweets for a specific user
@author: duc
"""

# inspired from https://gist.github.com/yanofsky/5436496, 
# access on 21.08.2017 19:39 

import json
from tweepy import Cursor
from twitter_api_setup import get_twitter_client


def get_max_amount_tweets(user):
    maxTweets = []
    api = get_twitter_client()
    print("fetch tweets")

    # request to get most recent 3200 tweets
    for tweet in Cursor(api.user_timeline, screen_name=user).items(3200):
        maxTweets.append(tweet)

    print("done fetching tweets")
    return maxTweets


if __name__ == '__main__':
    user = 'realDonaldTrump'
    maxTweets = get_max_amount_tweets(user)
    print('last tweet was created at: ' + str(maxTweets[-1].created_at))
    print('latest tweet was created at: ' + str(maxTweets[0].created_at))
    fname = "tweets_{}.json1".format(user)
    
    with open(fname, 'w') as f:
        for tweet in maxTweets:
            f.write(json.dumps(tweet.text)+"\n")
        print('DONE!')
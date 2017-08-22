#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 17:12:00 2017
Linguistic analysis of tweets
@author: duc
"""

import utils
from tweepy import Cursor
from twitter_api_setup import get_twitter_client


def get_max_amount_tweets(user):
    maxTweets = []
    api = get_twitter_client()
    print("fetch tweets")

    # request to get most recent 3200 tweets
    for tweet in Cursor(api.user_timeline, screen_name=user).items(3200):
        maxTweets.append(tweet.text)
        
    print("done fetching tweets")
    return maxTweets

def get_average_word_length(tweets):
    words = sum(tweets, [])
    count = 0
    for word in words:
        count += len(word)
    return count / len(words)

def get_average_word_syllables(tweets):
    words = sum(tweets, [])
    syl = 0
    for word in words:
        syl += utils.get_word_syllables_offline(word)
    return syl / len(words)

def get_average_sentence_length(tweets):
    wordCount = 0
    sentenceCount = 0
    for tweet in tweets:
        for sentence in tweet:
            wordCount += len(sentence)
            sentenceCount += 1
    return wordCount / sentenceCount

def get_average_tweet_length(tweets):
    wordCount = len(sum(tweets, []))
    return wordCount / len(tweets)


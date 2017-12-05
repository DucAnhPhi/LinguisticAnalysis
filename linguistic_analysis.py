#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 17:12:00 2017

Linguistic analysis of tweets

@author: duc
"""

import utils
import re
import json
from nltk.corpus import cmudict
from tweepy import Cursor
from twitter_api_setup import get_twitter_client
from collections import Counter


def get_max_amount_tweets(user):
    maxTweets = []
    api = get_twitter_client()
    print("\nfetch", user,"'s tweets")

    # request to get most recent 3200 tweets and write to a file
    with open(user + '_tweets.json', 'w') as f:
        for tweet in Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items(3200):
            maxTweets.append(tweet.full_text)
        json.dump(maxTweets, f)

    print("done fetching", len(maxTweets),"tweets")
    return maxTweets

def get_tweets_from_file(user):
    tweets = []
    with open(user + '_tweets.json', 'r') as f:
        print('read tweets from file ' + user + '_tweets.json ...')
        tweets = json.load(f)
    print('finish reading')
    return tweets

def get_average_exclamation_marks(tweets):
    count = 0
    for tweet in tweets:
        exclamationMark = re.compile(r"\!")
        count += len(exclamationMark.findall(tweet))
    return count / len(tweets)

def get_exclamation_marks(tweet):
    exclamationMark = re.compile(r"\!")
    return len(exclamationMark.findall(tweet))

def get_average_question_marks(tweets):
    count = 0
    for tweet in tweets:
        questionMark = re.compile(r"\?")
        count += len(questionMark.findall(tweet))
    return count / len(tweets)

#------ functions below require preprocessed and tokenized text ---------------
def get_average_word_characters(tweets):
    charCount = 0
    words = 0
    for tweet in tweets:
        for sentence in tweet:
            for word in sentence:
                words += 1
                charCount += len(word)
    return charCount / words

def get_average_word_syllables(tweets):
    pronouncingDict = cmudict.dict()
    syl = 0
    words = 0
    for tweet in tweets:
        for sentence in tweet:
            for word in sentence:
                words += 1
                syl += utils.get_word_syllables_offline(word, pronouncingDict)
    return syl / words

def get_average_sentence_length(tweets):
    wordCount = 0
    sentenceCount = 0
    for tweet in tweets:
        for sentence in tweet:
            wordCount += len(sentence)
            sentenceCount += 1
    return wordCount / sentenceCount

def get_sentence_length(tweet):
    wordCount = 0
    sentenceCount = 0
    for sentence in tweet:
        wordCount += len(sentence)
        sentenceCount += 1
    return wordCount / sentenceCount

def get_average_tweet_length(tweets):
    wordCount = 0
    for tweet in tweets:
        for sentence in tweet:
            wordCount += len(sentence)
    return wordCount / len(tweets)

def get_average_flesch_grade_level(tweets):
    pronouncingDict = cmudict.dict()
    level = 0
    for tweet in tweets:
        level += utils.get_flesch_grade_level(tweet, pronouncingDict)
    return level / len(tweets)

# inspired from Marco Bonzanini - Mastering Social Media Mining with Python
# p. 74
def get_most_frequent_keywords(tweets):
    tweetsWithoutStopwords = (
        [utils.remove_stopwords(tweet) for tweet in tweets]
    )
    counter = Counter()
    # get rid of sentence structure after tokenization
    newTweets = [ sum(tweet, []) for tweet in tweetsWithoutStopwords ]
    for tweet in newTweets:
        counter.update(tweet)
    return counter.most_common(25)
#------------------------------------------------------------------------------
def get_linguistic_analysis(user, fromFile):
    tweets = []
    if fromFile:
        tweets = get_tweets_from_file(user)
    else:
        tweets = get_max_amount_tweets(user)
    tweets = utils.remove_retweets(tweets)
    norm = [
        utils.preprocess(tweet)
        for tweet in tweets if len(utils.preprocess(tweet))
        if not utils.is_retweet(tweet)
    ]
    print("\nLinguistic Analysis of ", user, "'s tweets\n")
    print(
        "Average word length: ",
        get_average_word_characters(norm),
        " characters"
    )
    print("Average syllables per word: ", get_average_word_syllables(norm))
    print(
        "Average sentence length: ",
        get_average_sentence_length(norm),
        " words"
    )
    print("Average tweet length: ", get_average_tweet_length(norm), " words")
    print(
        "Average question marks per tweet: ",
        get_average_question_marks(tweets)
    )
    print(
        "Average exclamation marks per tweet: ",
        get_average_exclamation_marks(tweets)
    )
    print("Average flesch grade level: ", get_average_flesch_grade_level(norm))
    print("\nMost frequent 25 keywords:")
    for tag,count in get_most_frequent_keywords(norm):
        print("{}: {}".format(tag, count))


if __name__ == '__main__':
    fromFile = True
    user = input(
        "Enter the Twitter username of the person you want to analyse:\n"
    )
    get_linguistic_analysis(user, fromFile)
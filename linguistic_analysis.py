#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 17:12:00 2017

Linguistic analysis of tweets

@author: duc
"""

import utils
import re
import copy
from nltk.corpus import cmudict
from tweepy import Cursor
from twitter_api_setup import get_twitter_client
from collections import Counter
from flesch_kincaid import get_flesch_grade_level

def normalize(tweet):
    normalized = copy.copy(tweet)
    normalized = normalized.lower()

    # remove some emoticons the TweetTokenizer does not know
    normalized = utils.remove_emoticons(normalized)

    # split contractions like "he's" -> "he s", using imported contractions dictionary
    normalized = utils.split_contractions(normalized)

    # split compounds like "next-level" -> "next level"
    normalized = utils.split_compounds(normalized)

    # remove links
    normalized = utils.remove_links(normalized)

    # remove all special characters and return tokenized text
    normalized = utils.remove_special_characters(normalized)

    normalized = utils.remove_empty_sentences(normalized)

    return normalized

def get_max_amount_tweets(user):
    maxTweets = []
    api = get_twitter_client()
    print("fetch tweets")

    # request to get most recent 3200 tweets
    for tweet in Cursor(api.user_timeline, screen_name=user).items(3200):
        maxTweets.append(tweet.text)
        
    print("done fetching tweets")
    return maxTweets

def get_average_exclamation_marks(tweets):
    count = 0
    for tweet in tweets:
        exclamationMark = re.compile(r"\!")
        count += len(exclamationMark.findall(tweet))
    amount = count / len(tweets)
    print("Average exclamation marks per tweet: ", amount)
    return amount

def get_average_question_marks(tweets):
    count = 0
    for tweet in tweets:
        questionMark = re.compile(r"\?")
        count += len(questionMark.findall(tweet))
    amount = count / len(tweets)
    print("Average question marks per tweet: ", amount)
    return amount

#------ functions below require normalized and tokenized text -----------------
def get_average_word_characters(tweets):
    charCount = 0
    words = 0
    for tweet in tweets:
        for sentence in tweet:
            for word in sentence:
                words += 1
                charCount += len(word)
    amount = charCount / words
    print("Average word length: ", amount, " characters")
    return amount

def get_average_word_syllables(tweets):
    pronouncingDict = cmudict.dict()
    syl = 0
    words = 0
    for tweet in tweets:
        for sentence in tweet:
            for word in sentence:
                words += 1
                syl += utils.get_word_syllables_offline(word, pronouncingDict)
    amount = syl / words
    print("Average syllables per word: ", amount)
    return amount

def get_average_sentence_length(tweets):
    wordCount = 0
    sentenceCount = 0
    for tweet in tweets:
        for sentence in tweet:
            wordCount += len(sentence)
            sentenceCount += 1
    amount = wordCount / sentenceCount
    print("Average sentence length: ", amount, " words")
    return amount

def get_average_tweet_length(tweets):
    wordCount = 0
    for tweet in tweets:
        for sentence in tweet:
            wordCount += len(sentence)
    amount = wordCount / len(tweets)
    print("Average tweet length: ", amount, " words")
    return amount

def get_average_flesch_grade_level(tweets):
    pronouncingDict = cmudict.dict()
    level = 0
    for tweet in tweets:
        level += get_flesch_grade_level(tweet, pronouncingDict)
    level = level / len(tweets)
    print("Average flesch grade level: ", level)
    return level

# inspired from Marco Bonzanini - Mastering Social Media Mining with Python
# p. 74
def get_most_frequent_keywords(tweets):
    tweetsWithoutStopwords = [utils.remove_stopwords(tweet) for tweet in tweets]
    counter = Counter()
    # get rid of sentence structure after tokenization
    newTweets = [ sum(tweet, []) for tweet in tweetsWithoutStopwords ]
    for tweet in newTweets:
        counter.update(tweet)
    print("Most frequent keywords:")
    for tag,count in counter.most_common(25):
        print("{}: {}".format(tag, count))
    return counter
#------------------------------------------------------------------------------

if __name__ == '__main__':
    user = "realDonaldTrump"
    tweets = [tweet for tweet in get_max_amount_tweets(user) if not utils.is_retweet(tweet)]
    norm = [ normalize(tweet) for tweet in tweets if len(normalize(tweet)) if not utils.is_retweet(tweet) ]
    print("Linguistic Analysis of ", user)
    get_average_word_characters(norm)
    get_average_word_syllables(norm)
    get_average_sentence_length(norm)
    get_average_tweet_length(norm)
    get_average_question_marks(tweets)
    get_average_exclamation_marks(tweets)
    get_average_flesch_grade_level(norm)
    get_most_frequent_keywords(norm)
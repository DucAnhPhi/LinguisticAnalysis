#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 18:23:39 2017

Prepare datasets for neural_network.py

@author: duc
"""

import numpy as np
import utils
import copy
from nltk.corpus import cmudict
import linguistic_analysis as la
import flesch_kincaid as fk
import neural_network as nn


def get_combined_keywords(tweets1, tweets2):
    # get combined list of top 25 most used keywords
    keywords1 = la.get_most_frequent_keywords(tweets1)
    keywords2 = la.get_most_frequent_keywords(tweets2)

    # get rid of tuples
    for i,tuple in enumerate(keywords1):
        keywords1[i] = tuple[0]
    for i,tuple in enumerate(keywords2):
        keywords2[i] = tuple[0]

    keywords1 = set(keywords1)
    keywords2 = set(keywords2)

    # combined keywords
    combinedKeywords = keywords1.union(keywords2)
    return combinedKeywords

def get_keywords_count(tweet, dictionary):
    keywords = copy.copy(dictionary)
    for sentence in tweet:
        for word in sentence:
            if word in keywords:
                keywords[word] += 1
    return keywords

def extract_features(tweets, preprocessedTweets, keywordsCount, pronDict):
    extracted = []
    for index, tweet in enumerate(preprocessedTweets):
        sentLength = la.get_sentence_length(tweet)
        exclMarks = la.get_exclamation_marks(tweets[index])
        gradeLvl = fk.get_flesch_grade_level(tweet, pronDict)
        keyCount = get_keywords_count(tweet, keywordsCount)

        # put all features together
        features = [ sentLength, exclMarks, gradeLvl ]
        for key in keyCount:
            features.append(keyCount[key])
        extracted.append(features)
    return extracted

def get_tweet_data(person1, person2):
    # get tweets
    tweets1 = la.get_max_amount_tweets(person1)
    tweets2 = la.get_max_amount_tweets(person2)

    # remove retweets
    tweets1 = utils.remove_retweets(tweets1)
    tweets2 = utils.remove_retweets(tweets2)

    # preprocessed tweets
    preprocessedTweets1 = [ utils.preprocess(tweet) for tweet in tweets1 if len(utils.preprocess(tweet)) ]
    preprocessedTweets2 = [ utils.preprocess(tweet) for tweet in tweets2 if len(utils.preprocess(tweet)) ]

    # extract features

    keywords = get_combined_keywords(preprocessedTweets1, preprocessedTweets2)
    keywordsCount = {keyword:0 for keyword in keywords}

    pronouncingDict = cmudict.dict()

    data1 = np.array(extract_features(tweets1, preprocessedTweets1, keywordsCount, pronouncingDict))
    data2 = np.array(extract_features(tweets2, preprocessedTweets2, keywordsCount, pronouncingDict))

    # label data
    data1 = nn.concat_bias(1, data1)
    data2 = nn.concat_bias(0, data2)
    print(data1, "\n")
    print(data2, "\n")

    # concatenate vertically
    data = np.r_[data1, data2]


if __name__ == '__main__':
    np.set_printoptions(threshold = 10000, precision=4, suppress=True)
    get_tweet_data("realDonaldTrump", "HillaryClinton")

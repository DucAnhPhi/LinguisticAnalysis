#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 18:23:39 2017

Prepare datasets for neural_network.py

@author: duc
"""

import numpy as np
import utils as ut
import copy
from random import shuffle
from nltk.corpus import cmudict
import linguistic_analysis as la
import flesch_kincaid as fk
import neural_network as nn


def normalize(data):
    normalized = copy.deepcopy(data)
    # since there are no negative values we can just divide each column
    # elementwise by its maximum, in order to get values between 0 and 1
    # from https://stackoverflow.com/questions/29661574/normalize-numpy-array-columns-in-python
    # access on 27.08.2017 23:27
    normalized = normalized / normalized.max(axis = 0)
    return normalized

def get_positive_negative_amount(data):
    pCount = 0
    nCount = 0
    for element in data:
        label = element[0]
        if label == 1:
            pCount += 1
        elif label == 0:
            nCount += 1
    return (pCount, nCount)

def get_combined_keywords(tweets1, tweets2):
        # preprocess tweets
        preprocTweets1 = [ ut.preprocess(tweet) for tweet in tweets1 if len(ut.preprocess(tweet)) ]
        preprocTweets2 = [ ut.preprocess(tweet) for tweet in tweets2 if len(ut.preprocess(tweet)) ]

        # get combined list of top 25 most used keywords
        keywords1 = la.get_most_frequent_keywords(preprocTweets1)
        keywords2 = la.get_most_frequent_keywords(preprocTweets2)

        # get rid of tuples
        for i,tuple in enumerate(keywords1):
            keywords1[i] = tuple[0]
        for i,tuple in enumerate(keywords2):
            keywords2[i] = tuple[0]

        keywords1 = set(keywords1)
        keywords2 = set(keywords2)

        # combined keywords
        combinedKeywords = keywords1.union(keywords2)
        # return dictionary for counting keywords
        return {keyword:0 for keyword in combinedKeywords}

def get_keywords_count(preprocTweet, dictionary):
    keywords = copy.copy(dictionary)
    for sentence in preprocTweet:
        for word in sentence:
            if word in keywords:
                keywords[word] += 1
    return keywords

def extract_features(tweet, combinedKeywords, pronDict):
    preprocessed = ut.preprocess(tweet)

    # ignore empty preprocessed tweets or retweets
    if len(preprocessed) == 0 or ut.is_retweet(tweet):
        return []
    else:
        sentLength = la.get_sentence_length(preprocessed)
        exclMarks = la.get_exclamation_marks(tweet)
        gradeLvl = fk.get_flesch_grade_level(preprocessed, pronDict)
        keyCount = get_keywords_count(preprocessed, combinedKeywords)

        # put all features together
        features = [ sentLength, exclMarks, gradeLvl ]
        for key in keyCount:
            features.append(keyCount[key])
        # return array
        return features

def divide_data_into_sets(data, trainDataAmount):
    # count positive and negative examples
    pnCounts = get_positive_negative_amount(data)
    pCount = pnCounts[0]
    nCount = pnCounts[1]
    # initialize positive and negative count for training set
    # which contains 50% positive and 50% negative examples
    trainingSetSize = trainDataAmount * len(data)
    pCount = min(pCount, nCount)
    if pCount > trainingSetSize / 2:
        pCount = int(trainingSetSize / 2)
    nCount = copy.copy(pCount)

    origData = data.tolist()
    remainingData = data.tolist()
    trainingSet = []

    # compose training set
    for e in origData:
        label = e[0]
        if label == 1 and pCount != 0:
            pCount -= 1
            trainingSet.append(e)
            remainingData.remove(e)
        elif label == 0 and nCount != 0:
            nCount -= 1
            trainingSet.append(e)
            remainingData.remove(e)

    # shuffle training and remaining data
    shuffle(trainingSet)
    shuffle(remainingData)

    # compose test and cross validation set
    half = int(len(remainingData) / 2)
    testSet = remainingData[0:half]
    cvSet = remainingData[half:len(remainingData)]

    return (np.array(testSet), np.array(cvSet), np.array(trainingSet))


class Dataset:

    def __init__(
        self, user1, user2, trainDataAmount
    ):
        self.user1 = user1
        self.user2 = user2

        self.combinedKeywords = []
        self.pronDict = cmudict.dict()

        data = self.get_prepared_tweet_data()
        dividedData = divide_data_into_sets(data, trainDataAmount)
        self.testSet = dividedData[0]
        self.cvSet = dividedData[1]
        self.trainSet = dividedData[2]

    def get_prepared_tweet_data(self):
        # get tweets and remove retweets
        tweets1 = ut.remove_retweets(la.get_max_amount_tweets(self.user1))
        tweets2 = ut.remove_retweets(la.get_max_amount_tweets(self.user2))

        # extract features
        self.combinedKeywords = get_combined_keywords(tweets1, tweets2)

        data1 = np.array(
            [extract_features(tweet, self.combinedKeywords, self.pronDict) for tweet in tweets1
             if len(extract_features(tweet, self.combinedKeywords, self.pronDict))]
        )
        data2 = np.array(
            [extract_features(tweet, self.combinedKeywords, self.pronDict) for tweet in tweets2
             if len(extract_features(tweet, self.combinedKeywords, self.pronDict))]
        )

        # label data
        data1 = nn.concat_bias(1, data1)
        data2 = nn.concat_bias(0, data2)

        # concatenate vertically
        data = np.r_[data1, data2]

        # normalize all the data
        data = normalize(data)
        # return numpy array
        return data
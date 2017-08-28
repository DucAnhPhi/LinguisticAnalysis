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
    # return set
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
    # return 2D array
    return extracted

def get_prepared_tweet_data(person1, person2):
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

    # concatenate vertically
    data = np.r_[data1, data2]
    # normalize all the data
    data = normalize(data)
    # return numpy array
    return data

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

def divide_data_into_sets(data, testAmount, cvAmount, trainingAmount):
    # count positive and negative examples
    pnCounts = get_positive_negative_amount(data)
    pCount = pnCounts[0]
    nCount = pnCounts[1]
    # initialize positive and negative count for training set
    # which contains 50% positive and 50% negative examples
    trainingSetSize = trainingAmount * len(data)
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

    # return (still) labeled data sets as 2D arrays
    return (np.array(testSet), np.array(cvSet), np.array(trainingSet))


if __name__ == '__main__':
    np.set_printoptions(threshold = 10000, precision=4, suppress=True)

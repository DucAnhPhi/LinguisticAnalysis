#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 13:56:53 2017

Compute Flesch Kincaid readability tests

@author: duc
"""

import copy
import utils

def normalize(text):
    normalizedText = copy.copy(text)

     # remove tweet specific prefix
    normalizedText = utils.remove_tweet_prefix(normalizedText)

    # remove some emoticons the TweetTokenizer does not know
    normalizedText = utils.remove_emoticons(normalizedText)

    # split contractions like "he's" -> "he s", using imported contractions dictionary
    normalizedText = utils.split_contractions(normalizedText)

    # split compounds like "next-level" -> "next level"
    normalizedText = utils.split_compounds(normalizedText)

    # remove links
    normalizedText = utils.remove_links(normalizedText)

    # remove all special characters
    # return normalized text tokenized
    normalizedText = utils.remove_special_characters(normalizedText)

    return normalizedText

def get_flesch_readability_ease(tokenizedText):
    words = sum(tokenizedText, [])
    numberOfWords = len(words)
    numberOfSentences = len(tokenizedText)
    numberOfSyllables = 0
    for word in words:
        numberOfSyllables += utils.get_word_syllables(word)
    return 206.835 - (1.015 * numberOfWords / numberOfSentences) - (84.6 * numberOfSyllables / numberOfWords)

def get_flesch_grade_level(tokenizedText):
    words = sum(tokenizedText, [])
    numberOfWords = len(words)
    numberOfSentences = len(tokenizedText)
    numberOfSyllables = 0
    for word in words:
        numberOfSyllables += utils.get_word_syllables(word)
    return (0.39 * numberOfWords / numberOfSentences) + (11.8 * numberOfSyllables / numberOfWords) - 15.59

if __name__ == '__main__':
    #tweets = utils.get_twitter_corpus()
    #normalizedTweets = [ normalize(tweet) for tweet in tweets ]
    normalized = normalize('The Australian platypus is seemingly a hybrid of a mammal and reptilian creature.')
    print(normalized)
    print(get_flesch_readability_ease(normalized))
    print(get_flesch_grade_level(normalized))

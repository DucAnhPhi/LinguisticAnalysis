#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 14:02:30 2017

Compute word difficulty, scraping http://www.dictionary.com

@author: duc
"""

import re
import copy
import urllib.request
import utils as ut


def normalize(text):
    normalizedText = copy.copy(text)
    # remove tweet specific prefix
    normalizedText = ut.remove_tweet_prefix(normalizedText)

    # remove some emoticons the TweetTokenizer does not know
    normalizedText = ut.remove_emoticons(normalizedText)

    # split contractions like "he's" -> "he s", using imported contractions dictionary
    normalizedText = ut.split_contractions(normalizedText)

    # split compounds like "next-level" -> "next level"
    normalizedText = ut.split_compounds(normalizedText)

    # remove links
    normalizedText = ut.remove_links(normalizedText)

    # remove all special characters
    normalizedText = ut.remove_special_characters(normalizedText)

    # remove stopwords
    normalizedText = ut.remove_stopwords(normalizedText)

    return normalizedText

def get_word_difficulty(word):
    url = 'http://www.dictionary.com/browse/' + word
    request = urllib.request.urlopen(url)
    difficulty = re.search('(?<=data-difficulty=")[0-9]+', request.read().decode('utf-8'))
    if difficulty:
        return difficulty[0]

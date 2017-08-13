#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 10:57:08 2017

Reuseable functions

@author: duc
"""

import re
import urllib.request
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples
from nltk.corpus import cmudict
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import sent_tokenize
from assets.contractions import contractions
from assets.emoticons import emoticons


def split_contractions(text):
    normalizedText = text.lower()
    contractionsPattern = re.compile('({})'.format('|'.join(contractions.keys())), flags=re.IGNORECASE|re.DOTALL)

    def split_match(contraction):
        match = contraction.group(0)
        splitContraction = " ".join(match.split("'"))
        return splitContraction

    return re.sub(contractionsPattern, split_match, normalizedText)

def split_compounds(text):
    compoundPattern = r'\b\w*-\w*\b'

    def split_compound(compound):
        match = compound.group(0)
        return ' '.join(match.split('-'))

    return re.sub(compoundPattern, split_compound, text)

def tokenize(text, tokenizer = TweetTokenizer()):
    return [ tokenizer.tokenize(sentence) for sentence in sent_tokenize(text) ]


"""
BOOLEAN functions
"""
def is_not_link(string):
    linkPattern = re.compile(r"(http(s)?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)")
    if linkPattern.match(string):
        return False
    else:
        return True

def is_not_contraction(string):
    return string.lower() not in contractions

def is_not_compound(string):
    compoundPattern = re.compile(r'\b\w*-\w*\b')
    if compoundPattern.match(string):
        return False
    else:
        return True

def is_not_emoticon(string):
     return string.lower() not in emoticons


"""
REMOVE functions
"""
def remove_tweet_prefix(text):
    cleanedTweet = tokenize(text.lower())
    # Remove prefix 'RT @username:'
    if cleanedTweet[0][0] == 'rt':
        del cleanedTweet[0][:3]
    return " ".join(sum(cleanedTweet, []))

def remove_links(text):
    tokenizedText = tokenize(text)
    filtered = [ [ token for token in sentence if is_not_link(token) ] for sentence in tokenizedText ]
    return " ".join(sum(filtered, []))

def remove_special_characters(text):
    # remove special characters without interfering with other normalization methods
    tokenizedText = tokenize(text)
    alphabetAndDigits = [chr(i) for i in range(97, 123)] + [str(i) for i in range(0, 10)]

    def clean(string):
        cleanedString = ''
        for character in string.lower():
            if character in alphabetAndDigits:
                cleanedString += character
        return cleanedString

    filtered = [ [ clean(token) if all([is_not_link(token), is_not_contraction(token), is_not_compound(token), is_not_emoticon(token)]) else token for token in sentence if len(clean(token)) ] for sentence in tokenizedText ]
    return filtered

def remove_emoticons(text):
    # build regexp with imported emoticon list
    smileys = '|'.join(map(re.escape, emoticons))
    emoticonsPattern = re.compile('({})'.format(smileys), flags=re.IGNORECASE)
    removed = re.sub(emoticonsPattern, '', text)
    # remove unnecessary white spaces utilizing the TweetTokenizer
    removed = tokenize(removed)
    return " ".join(sum(removed, []))

def remove_stopwords(text):
    normalizedText = text.lower()
    normalizedText = split_contractions(normalizedText)
    tokenizedText = tokenize(normalizedText)
    stopwordList = stopwords.words('english')
    filtered = [ [ token for token in sentence if token not in stopwordList ] for sentence in tokenizedText ]
    return " ".join(sum(filtered, []))


"""
GETTER functions
"""
def get_word_syllables(word):
    pronouncingDict = cmudict.dict()
    # returns a list of transcriptions for a word - a word may have alternative pronunciations
    # eg. 'orange' -> [['AO1', 'R', 'AH0', 'N', 'JH'], ['A01', 'R', 'IH0', 'N', 'JH']]
    # vowels are marked with numbers from 0-2
    # by counting the vowels we can get the number of syllables
    try:
        # last element is more common
        pronList = pronouncingDict[word.lower()][-1]
        return len([ syl for syl in pronList if syl[-1].isdecimal() ])
    except KeyError:
        # scrape syllable count
        url = 'http://www.syllablecount.com/syllables/' + word
        request = urllib.request.urlopen(url)
        response = request.read().decode('utf-8')
        # use regex to match desired value
        sylCount = re.search("(?<=<b style='color: #008000'>)[0-9]+", response)
        return sylCount[0];

def get_twitter_corpus():
    tweets = twitter_samples.strings('tweets.20150430-223406.json')
    return tweets

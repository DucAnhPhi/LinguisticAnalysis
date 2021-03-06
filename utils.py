#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 10:57:08 2017

Reuseable functions

@author: duc
"""

import re
import copy
import urllib.request
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import sent_tokenize
from assets.contractions import contractions
from assets.emoticons import emoticons


def split_contractions(text):
    preprocessedText = text.lower()
    contractionsPattern = re.compile(
        '({})'.format('|'.join(contractions.keys())),
         flags=re.IGNORECASE|re.DOTALL
    )

    def split_match(contraction):
        match = contraction.group(0)
        splitContraction = " ".join(match.split("'"))
        return splitContraction

    return re.sub(contractionsPattern, split_match, preprocessedText)

def split_compounds(text):
    compoundPattern = r'\b\w*-\w*\b'

    def split_compound(compound):
        match = compound.group(0)
        return ' '.join(match.split('-'))

    return re.sub(compoundPattern, split_compound, text)

def tokenize(text, tokenizer = TweetTokenizer()):
    return [ tokenizer.tokenize(sentence) for sentence in sent_tokenize(text) ]

def preprocess(tweet):
    preprocessed = copy.copy(tweet)
    preprocessed = preprocessed.lower()

    # remove some emoticons the TweetTokenizer does not know
    preprocessed = remove_emoticons(preprocessed)

    # split contractions like "he's" -> "he s",
    # by using imported contractions dictionary
    preprocessed = split_contractions(preprocessed)

    # split compounds like "next-level" -> "next level"
    preprocessed = split_compounds(preprocessed)

    # remove links
    preprocessed = remove_links(preprocessed)

    # remove all special characters and return tokenized text
    preprocessed = remove_special_characters(preprocessed)

    preprocessed = remove_empty_sentences(preprocessed)

    return preprocessed


"""
BOOLEAN functions
"""
def is_not_link(string):
    linkPattern = re.compile(
        r'(http(s)?:\/\/)?'
        r'(www\.)?'
        r'[-a-zA-Z0-9@:%._\+~#=]{1,256}'
        r'\.'
        r'[a-z]{2,6}'
        r'\b'
        r'([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    )
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

def is_retweet(text):
    rtPattern = re.compile(r'^rt @', flags=re.IGNORECASE)
    if rtPattern.match(text):
        return True
    else:
        return False


"""
REMOVE functions
"""
def remove_retweets(tweets):
    return [ tweet for tweet in tweets if not is_retweet(tweet) ]

def remove_links(text):
    tokenizedText = tokenize(text)
    filtered = [
        [ token for token in sentence if is_not_link(token) ]
        for sentence in tokenizedText
    ]
    return " ".join(sum(filtered, []))

def remove_special_characters(text):
    # remove special characters
    # without interfering with other normalization methods
    tokenizedText = tokenize(text)
    alphabetAndDigits = [
        chr(i) for i in range(97, 123)] + [str(i) for i in range(0, 10)
    ]

    def clean(string):
        cleanedString = ''
        for character in string.lower():
            if character in alphabetAndDigits:
                cleanedString += character
        return cleanedString

    filtered = [
        [
            clean(token) if all([
                is_not_link(token), is_not_contraction(token),
                is_not_compound(token), is_not_emoticon(token)
            ])
            else token for token in sentence if len(clean(token))
        ]
        for sentence in tokenizedText
    ]
    return filtered

def remove_emoticons(text):
    # build regexp with imported emoticon list
    smileys = '|'.join(map(re.escape, emoticons))
    emoticonsPattern = re.compile('({})'.format(smileys), flags=re.IGNORECASE)
    removed = re.sub(emoticonsPattern, '', text)
    # remove unnecessary white spaces utilizing the TweetTokenizer
    removed = tokenize(removed)
    return " ".join(sum(removed, []))

def remove_stopwords(preprocessedText):
    stopwordList = stopwords.words('english')
    filtered = [
        [ token for token in sentence if token not in stopwordList ]
        for sentence in preprocessedText
    ]
    return filtered

def remove_empty_sentences(tokenizedText):
    return [ sentence for sentence in tokenizedText if len(sentence) ]


"""
GETTER functions
"""
def get_word_difficulty(word):
    url = 'http://www.dictionary.com/browse/' + word
    request = urllib.request.urlopen(url)
    difficulty = re.search(
        '(?<=data-difficulty=")[0-9]+', request.read().decode('utf-8')
    )
    if difficulty:
        return difficulty[0]

def get_word_syllables(word, pronouncingDict):
    # returns a list of transcriptions for a word
    # (a word may have alternative pronunciations)
    # eg. 'orange':
    # -> [['AO1', 'R', 'AH0', 'N', 'JH'], ['A01', 'R', 'IH0', 'N', 'JH']]
    # vowels are marked with numbers from 0-2
    # by counting the vowels we can get the number of syllables
    try:
        # last element is more common
        pronList = pronouncingDict[word.lower()][-1]
        sylCount = len([ syl for syl in pronList if syl[-1].isdecimal() ])
        return sylCount
    except KeyError:
        # scrape syllable count
        url = 'http://www.syllablecount.com/syllables/' + word
        request = urllib.request.urlopen(url)
        response = request.read().decode('utf-8')
        # use regex to match desired value
        sylCount = int(
            re.search("(?<=<b style='color: #008000'>)[0-9]+", response)[0]
        )
        return sylCount;

def get_word_syllables_offline(word, pronouncingDict):
    # offline version of get_word_syllables function
    # may be less accurate but more performant
    try:
        pronList = pronouncingDict[word.lower()][-1]
        sylCount = len([ syl for syl in pronList if syl[-1].isdecimal() ])
        return sylCount
    except KeyError:
        # regex from:
        #     https://codegolf.stackexchange.com
        #     /questions/47322/how-to-count-the-syllables-in-a-word
        # access on 16.09.2017, 10:17
        sylCount = len(re.findall(r'[aiouy]+e*|e(?!d$|ly).|[td]ed|le$', word))
        return sylCount

def get_flesch_grade_level(tokenizedText, pronouncingDict):
    words = sum(tokenizedText, [])
    numberOfWords = len(words)
    numberOfSentences = len(tokenizedText)
    numberOfSyllables = 0
    for word in words:
        numberOfSyllables = (
            numberOfSyllables
            + get_word_syllables_offline(word, pronouncingDict)
        )
    return (
        (0.39 * numberOfWords / numberOfSentences)
        + (11.8 * numberOfSyllables / numberOfWords)
        - 15.59
    )

def get_twitter_corpus():
    tweets = twitter_samples.strings('tweets.20150430-223406.json')
    return tweets
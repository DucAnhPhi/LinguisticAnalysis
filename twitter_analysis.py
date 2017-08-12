#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 10:57:08 2017

@author: duc
"""
import copy
import re
import urllib.request
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples
from nltk.corpus import wordnet
from nltk.corpus import cmudict
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import sent_tokenize
from assets.contractions import contractions
from assets.emoticons import emoticons

def remove_tweet_prefix(text):
    cleanedTweet = tokenize_tweet(text.lower())
    # Remove prefix 'RT @username:'
    if cleanedTweet[0][0] == 'rt':
        del cleanedTweet[0][:3]
    return " ".join(sum(cleanedTweet, []))

# modified function from Text Analytics with Python - Dipanjan Sarkar, p.119
#def expand_contractions(text):
#    contractionsPattern = re.compile('({})'.format('|'.join(contractions.keys())), flags=re.IGNORECASE|re.DOTALL)
#    
#    def expand_match(contraction):
#        match = contraction.group(0)
#        expandedContraction = contractions.get(match) if contractions.get(match) else contractions.get(match.lower)
#        return expandedContraction
#    
#    return re.sub(contractionsPattern, expand_match, text)

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

def tokenize_tweet(tweet, tokenizer = TweetTokenizer()):
    return [ tokenizer.tokenize(sentence) for sentence in sent_tokenize(tweet) ]

def remove_emoticons(text):
    # build regexp with imported emoticon list
    smileys = '|'.join(map(re.escape, emoticons))
    emoticonsPattern = re.compile('({})'.format(smileys), flags=re.IGNORECASE)
    removed = re.sub(emoticonsPattern, '', text)
    # remove unnecessary white spaces utilizing the TweetTokenizer
    removed = tokenize_tweet(removed)
    return " ".join(sum(removed, []))

def is_not_link(string):
    linkPattern = re.compile(r"(http(s)?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)")
    if linkPattern.match(string):
        return False
    else:
        return True
    
def remove_links(text):
    tokenizedText = tokenize_tweet(text)
    filtered = [ [ token for token in sentence if is_not_link(token) ] for sentence in tokenizedText ]
    return " ".join(sum(filtered, []))

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

def remove_special_characters(text):
    # remove special characters without interfering with other normalization methods
    tokenizedText = tokenize_tweet(text)
    alphabetAndDigits = [chr(i) for i in range(97, 123)] + [str(i) for i in range(0, 10)]
        
    def clean(string):
        cleanedString = ''
        for character in string.lower():
            if character in alphabetAndDigits:
                cleanedString += character
        return cleanedString
    
    filtered = [ [ clean(token) if all([is_not_link(token), is_not_contraction(token), is_not_compound(token), is_not_emoticon(token)]) else token for token in sentence if len(clean(token)) ] for sentence in tokenizedText ]
    return filtered

def remove_stopwords(text):
    normalizedText = text.lower()
    normalizedText = split_contractions(normalizedText)
    tokenizedText = tokenize_tweet(normalizedText)
    stopwordList = stopwords.words('english')
    filtered = [ [ token for token in sentence if token not in stopwordList ] for sentence in tokenizedText ]
    return " ".join(sum(filtered, []))

# from Text Analytics with Python - Dipanjan Sarkar, p.121-122
def correct_repeating_characters(tokenizedText):
    repeatPattern = re.compile(r'(\w*)(\w)\2(\w*)')
    matchSubstitution = r'\1\2\3'
    def replace(oldWord):
        if wordnet.synsets(oldWord):
            return oldWord
        newWord = repeatPattern.sub(matchSubstitution, oldWord)
        return replace(newWord) if (newWord) != oldWord else newWord
    
    return [ [ replace(word) for word in sentence ] for sentence in tokenizedText ]
        

def get_mean_sentence_length(tweets):
    wordCount = 0
    sentenceCount = 0
    
    for tweet in tweets:
        for sentence in tweet:
            sentenceCount += 1
            for word in sentence:
                wordCount += 1

    return wordCount / sentenceCount

def get_sentence_length(text):
    wordCount = 0
    
    for sentence in text:
        for word in sentence:
            wordCount += 0

    return wordCount

def get_mean_word_length(tweets):
    wordLength = 0
    wordCount = 0
    
    for tweet in tweets:
        for sentence in tweet:
            for word in sentence:
                wordLength += len(word)
                wordCount += 1

    return wordLength / wordCount

def get_word_length(text):
    wordLength = 0
    wordCount = 0
    
    for sentence in text:
        for word in sentence:
            wordLength += len(word)
            wordCount += 1

    return wordLength / wordCount
    

def get_word_difficulty(word):
    url = 'http://www.dictionary.com/browse/' + word
    request = urllib.request.urlopen(url)
    difficulty = re.search('(?<=data-difficulty=")[0-9]+', request.read().decode('utf-8'))
    if difficulty:
        return difficulty[0]

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

def normalize_tweet_for_frequency_analysis(tweet):
    normalizedTweet = copy.copy(tweet)
    
     # remove tweet specific prefix
    normalizedTweet = remove_tweet_prefix(normalizedTweet)
    
    # remove some emoticons the TweetTokenizer does not know
    normalizedTweet = remove_emoticons(normalizedTweet)
    
    # split contractions like "he's" -> "he s", using imported contractions dictionary
    normalizedTweet = split_contractions(normalizedTweet)
    
    # split compounds like "next-level" -> "next level"
    normalizedTweet = split_compounds(normalizedTweet)
    
    # remove links
    normalizedTweet = remove_links(normalizedTweet)
    
    # remove all special characters
    # return normalized tweet tokenized
    normalizedTweet = remove_special_characters(normalizedTweet)
    
    return normalizedTweet

def normalize_tweets_for_frequency_analysis(tweets):
    return [ normalize_tweet_for_frequency_analysis(tweet) for tweet in tweets ]

def normalize_tweet_for_difficulty_analysis(tweet):
    normalizedTweet = copy.copy(tweet)
    # remove tweet specific prefix
    normalizedTweet = remove_tweet_prefix(normalizedTweet)
    
    # remove some emoticons the TweetTokenizer does not know
    normalizedTweet = remove_emoticons(normalizedTweet)
    
    # split contractions like "he's" -> "he s", using imported contractions dictionary
    normalizedTweet = split_contractions(normalizedTweet)
    
    # split compounds like "next-level" -> "next level"
    normalizedTweet = split_compounds(normalizedTweet)
    
    # remove links
    normalizedTweet = remove_links(normalizedTweet)
    
    # remove all special characters
    normalizedTweet = remove_special_characters(normalizedTweet)
    
    # correcting repeating characters - from Text Analytics with Python - Dipanjan Sarkar, p.121-122
    # normalizedTweet = correct_repeating_characters(normalizedTweet)
    
    # remove stopwords
    normalizedTweet = remove_stopwords(normalizedTweet)

    return normalizedTweet

def normalize_tweets_for_difficulty_analysis(tweets):
    return [ normalize_tweet_for_difficulty_analysis(tweet) for tweet in tweets ]

def get_flesch_readability_ease(tokenizedText):
    words = sum(tokenizedText, [])
    numberOfWords = len(words)
    numberOfSentences = len(tokenizedText)
    numberOfSyllables = 0
    for word in words:
        numberOfSyllables += get_word_syllables(word)
    return 206.835 - (1.015 * numberOfWords / numberOfSentences) - (84.6 * numberOfSyllables / numberOfWords)

def get_flesch_grade_level(tokenizedText):
    words = sum(tokenizedText, [])
    numberOfWords = len(words)
    numberOfSentences = len(tokenizedText)
    numberOfSyllables = 0
    for word in words:
        numberOfSyllables += get_word_syllables(word)
    return (0.39 * numberOfWords / numberOfSentences) + (11.8 * numberOfSyllables / numberOfWords) - 15.59

if __name__ == '__main__':
    tweet_tokenizer = TweetTokenizer()
    tweets = twitter_samples.strings('tweets.20150430-223406.json')
#    cleanedTweets = normalize_tweets_for_frequency_analysis(tweets)
#    print(get_mean_sentence_length(cleanedTweets))
#    print(get_mean_word_length(cleanedTweets))
    #cleanedTweets = normalize_tweets_for_difficulty_analysis(tweets)
    #print(cleanedTweets)
    #print(tokenize_tweet("He said: 'Hey, my name is... Tim!' - Tim."))
    #print(get_word_syllables('okokook'))
    #normalized = normalize_tweet_for_frequency_analysis('The Australian platypus is seemingly a hybrid of a mammal and reptilian creature.')
    #print(normalized)
    #print(get_flesch_readability_ease(normalized))
    #print(get_flesch_grade_level(normalized))
 


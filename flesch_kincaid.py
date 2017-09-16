#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 13:56:53 2017

Compute Flesch Kincaid readability tests

@author: duc
"""

import utils


def get_flesch_readability_ease(tokenizedText, pronouncingDict):
    words = sum(tokenizedText, [])
    numberOfWords = len(words)
    numberOfSentences = len(tokenizedText)
    numberOfSyllables = 0
    for word in words:
        numberOfSyllables = (
            numberOfSyllables
            + utils.get_word_syllables_offline(word, pronouncingDict)
        )
    return (
        206.835
        - (1.015 * numberOfWords / numberOfSentences)
        - (84.6 * numberOfSyllables / numberOfWords)
    )

def get_flesch_grade_level(tokenizedText, pronouncingDict):
    words = sum(tokenizedText, [])
    numberOfWords = len(words)
    numberOfSentences = len(tokenizedText)
    numberOfSyllables = 0
    for word in words:
        numberOfSyllables = (
            numberOfSyllables
            + utils.get_word_syllables_offline(word, pronouncingDict)
        )
    return (
        (0.39 * numberOfWords / numberOfSentences)
        + (11.8 * numberOfSyllables / numberOfWords)
        - 15.59
    )

def get_text_with_max_or_min_readability_score(
    corpus, function, pronouncingDict, getMax
):
    maxMinScore = 'init'
    maxMinScoreText = ''
    for text in corpus:
        score = function(text, pronouncingDict)
        if maxMinScore == 'init':
            maxMinScore = score
            maxMinScoreText = text
        else:
            if getMax and score > maxMinScore:
                maxMinScore = score
                maxMinScoreText = text
            elif not getMax and score < maxMinScore:
                maxMinScore = score
                maxMinScoreText = text
    return (maxMinScore, maxMinScoreText)

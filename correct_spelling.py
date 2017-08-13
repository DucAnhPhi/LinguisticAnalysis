#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 14:04:45 2017

@author: duc
"""

import re
from nltk.corpus import wordnet

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
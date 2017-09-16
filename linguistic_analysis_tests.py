#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 18:53:50 2017

Unit test for linguistic_analysis.py

@author: duc
"""

import unittest
import linguistic_analysis as la

tweets = [
    "Is this not a question?! Interactive introduction reference information",
    "Sure! Why not?"
]
norm = [
    [
        ["is", "this", "not", "a", "question"],
        ["interactive", "introduction", "reference", "information"]
    ],
    [["sure", "why", "not"]]
]

class LinguisticAnalysisTests(unittest.TestCase):

    def test_average_question_marks(self):
        self.assertEqual(la.get_average_question_marks(tweets), 1)

    def test_average_exclamation_marks(self):
        self.assertEqual(la.get_average_exclamation_marks(tweets), 1)
    
    def test_average_word_characters(self):
        number = la.get_average_word_characters(norm)
        self.assertEqual(round(number), 6)
    
    def test_average_word_syllables(self):
        number = la.get_average_word_syllables(norm)
        self.assertEqual(round(number), 2)
    
    def test_average_sentence_length(self):
        number = la.get_average_sentence_length(norm)
        self.assertEqual(round(number), 4)
    
    def test_average_tweet_length(self):
        number = la.get_average_tweet_length(norm)
        self.assertEqual(round(number), 6)


if __name__ == '__main__':
    unittest.main()




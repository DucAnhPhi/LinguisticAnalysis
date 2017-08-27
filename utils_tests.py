#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 23:36:17 2017

Unit tests for utils.py

@author: duc
"""

import unittest
import utils as ut
from nltk.corpus import cmudict


def to_string(tokenized):
    return " ".join(sum(tokenized, []))

class UtilTests(unittest.TestCase):

#------ test boolean functions --------------------------
    def test_is_link(self):
        s = "http://t.co/rlqo5xfbul"
        self.assertFalse(ut.is_not_link(s))

    def test_is_not_link(self):
        s = "fake.website"
        self.assertTrue(ut.is_not_link(s))

    def test_is_contraction(self):
        s = "couldn't"
        self.assertFalse(ut.is_not_contraction(s))

    def test_is_not_contraction(self):
        s = "peoples'"
        self.assertTrue(ut.is_not_contraction(s))

    def test_is_compound(self):
        s = "word-compound"
        self.assertFalse(ut.is_not_compound(s))

    def test_is_not_compound(self):
        s = "wordcompound"
        self.assertTrue(ut.is_not_compound(s))

    def test_is_emoticon(self):
        s = "xd"
        self.assertFalse(ut.is_not_emoticon(s))

    def test_is_not_emoticon(self):
        s = "exd"
        self.assertTrue(ut.is_not_emoticon(s))
#--------------------------------------------------------


#------ test ut.remove_special_characters function ------
    def test_no_punctuation(self):
        s = "He said: 'Hey, my name is... Tim!' - Tim."
        self.assertEqual(to_string(ut.remove_special_characters(s)), "he said hey my name is tim tim")

    def test_no_emojis(self):
         s = "💪🔥"
         self.assertEqual(to_string(ut.remove_special_characters(s)), "")

    def test_no_twitter_signs(self):
        s = "#scandal @elonmusk #innovation @here"
        self.assertEqual(to_string(ut.remove_special_characters(s)), "scandal elonmusk innovation here")

    def test_numbers(self):
        s = "1,2 1.2 1,000"
        self.assertEqual(to_string(ut.remove_special_characters(s)), "12 12 1000")

    def test_no_emoticons_without_letters_or_numbers(self):
        s = "Here are some emoticons without letters or numbers in them >:( :) :-)"
        self.assertEqual(to_string(ut.remove_special_characters(s)), "here are some emoticons without letters or numbers in them")
#---------------------------------------------------------


#------ test remove functions ----------------------------
    def test_no_tweet_prefix(self):
        s = "RT @Staircase2: blablabla"
        self.assertEqual(ut.remove_tweet_prefix(s), "blablabla")

    def test_no_emoticons_with_letters_or_numbers(self):
        s = r"here are some emoticons containing letters or numbers :D :d :P :p :'D xd :o which the tokenizer may not know :-3 :3 8) 8-) <3 </3"
        self.assertEqual(ut.remove_emoticons(s), "here are some emoticons containing letters or numbers which the tokenizer may not know")

    def test_no_links(self):
        s = r"some links http://t.co/rlqo5xfbul www.google.com bplaced.homepage.net/article/2221 g.com g.co"
        self.assertEqual(ut.remove_links(s), "some links")

    def test_no_stopwords(self):
        s = [["i", "couldn","t", "wouldn", "t", "to", "do", "this"]]
        self.assertEqual(ut.remove_stopwords(s), [[]])
#---------------------------------------------------------


#------ test split functions -----------------------------
    def test_split_compounds(self):
        s = "e-mail enterprise-level level-14 three-level-building best-in-class"
        self.assertEqual(ut.split_compounds(s), "e mail enterprise level level 14 three level building best in class")

    def test_split_contractions(self):
        s = r"I'm won't we'll can't he's that's there's"
        self.assertEqual(ut.split_contractions(s), "i m won t we ll can t he s that s there s")
#---------------------------------------------------------


#------ test count functions -----------------------------
    def test_count_word_syllables(self):
        pronouncingDict = cmudict.dict()
        strings = {
                "123456789": 0,
                "supercalifragilisticexpialidocious": 14,
                "demagogue": 3,
                "anathema": 4,
                "payday": 2,
                "Syrian": 3,
                "crepuscular": 4,
                "preservative": 4,
                "significantly": 5,
                "embezzlement": 4
        }
        for string in strings:
            sylCount = ut.get_word_syllables(string, pronouncingDict)
            self.assertEqual(sylCount, strings[string])

    def test_count_word_syllables_offline(self):
        # fails at supercalifragilistic..., asserts 13 instead of 14 syllables
        # print accuracy of function instead
        pronouncingDict = cmudict.dict()
        strings = {
                "123456789": 0,
                "supercalifragilisticexpialidocious": 14,
                "demagogue": 3,
                "anathema": 4,
                "payday": 2,
                "Syrian": 3,
                "crepuscular": 4,
                "preservative": 4,
                "significantly": 5,
                "embezzlement": 4
        }
        accuracy = 0
        for string in strings:
            sylCount = ut.get_word_syllables_offline(string, pronouncingDict)
            if sylCount == strings[string]:
                accuracy += 10
        print("\nsyllable counter offline accuracy: " + str(accuracy) + "%")
#---------------------------------------------------------

    def test_preprocessing(self):
        s = r"💪🔥 >:( xd <3 :'D http://t.co/rlqo5xfbul www.google.com e-mail three-level-building I'm wouldn't @trump #bad 1.2 Hi, my name is: Jon!? Next sentence."
        self.assertEqual(to_string(ut.preprocess(s)), "e mail three level building i m wouldn t trump bad 12 hi my name is jon next sentence")


if __name__ == '__main__':
    unittest.main()
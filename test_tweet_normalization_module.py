#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 23:36:17 2017

@author: duc
"""

import unittest
import twitter_analysis as ta

def to_string(tokenized):
    return " ".join(sum(tokenized, []))

class TestTweetNormalization(unittest.TestCase):
    
#------ test boolean functions --------------------------    
    def test_is_link(self):
        s = "http://t.co/rlqo5xfbul"
        self.assertFalse(ta.is_not_link(s))
    
    def test_is_not_link(self):
        s = "fake.website"
        self.assertTrue(ta.is_not_link(s))
    
    def test_is_contraction(self):
        s = "couldn't"
        self.assertFalse(ta.is_not_contraction(s))
    
    def test_is_not_contraction(self):
        s = "peoples'"
        self.assertTrue(ta.is_not_contraction(s))
    
    def test_is_compound(self):
        s = "word-compound"
        self.assertFalse(ta.is_not_compound(s))
        
    def test_is_not_compound(self):
        s = "wordcompound"
        self.assertTrue(ta.is_not_compound(s))
    
    def test_is_emoticon(self):
        s = "xd"
        self.assertFalse(ta.is_not_emoticon(s))
        
    def test_is_not_emoticon(self):
        s = "exd"
        self.assertTrue(ta.is_not_emoticon(s))
#--------------------------------------------------------
        
    
#------ test ta.remove_special_characters function ------
    def test_no_punctuation(self):
        s = "He said: 'Hey, my name is... Tim!' - Tim."
        self.assertEqual(to_string(ta.remove_special_characters(s)), "he said hey my name is tim tim")
        
    def test_no_emojis(self):
         s = "💪🔥"
         self.assertEqual(to_string(ta.remove_special_characters(s)), "")
        
    def test_no_twitter_signs(self):
        s = "#scandal @elonmusk #innovation @here"
        self.assertEqual(to_string(ta.remove_special_characters(s)), "scandal elonmusk innovation here")
    
    def test_numbers(self):
        s = "1,2 1.2 1,000"
        self.assertEqual(to_string(ta.remove_special_characters(s)), "12 12 1000")
    
    def test_no_emoticons_without_letters_or_numbers(self):
        s = "Here are some emoticons without letters or numbers in them >:( :) :-)"
        self.assertEqual(to_string(ta.remove_special_characters(s)), "here are some emoticons without letters or numbers in them")
#---------------------------------------------------------

    def test_no_tweet_prefix(self):
        s = "RT @Staircase2: blablabla"
        self.assertEqual(ta.remove_tweet_prefix(s), "blablabla")
        
    def test_no_emoticons_with_letters_or_numbers(self):
        s = r"here are some emoticons containing letters or numbers :D :d :P :p :'D xd :o which the tokenizer may not know :-3 :3 8) 8-) <3 </3"
        self.assertEqual(ta.remove_emoticons(s), "here are some emoticons containing letters or numbers which the tokenizer may not know")
    
    def test_no_links(self):
        s = r"some links http://t.co/rlqo5xfbul www.google.com bplaced.homepage.net/article/2221 g.com g.co"
        self.assertEqual(ta.remove_links(s), "some links")
        
    def test_split_compounds(self):
        s = "e-mail enterprise-level level-14 three-level-building best-in-class"
        self.assertEqual(ta.split_compounds(s), "e mail enterprise level level 14 three level building best in class")
        
    def test_split_contractions(self):
        s = r"I'm won't we'll can't he's that's there's"
        self.assertEqual(ta.split_contractions(s), "i m won t we ll can t he s that s there s")
        
    def test_no_stopwords(self):
        s = "I couldn't wouldn't to do this"
        self.assertEqual(ta.remove_stopwords(s), "")
        
    def test_normalize_tweet_for_frequency_analysis(self):
        s = r"RT @Staircase2: 💪🔥 >:( xd <3 :'D http://t.co/rlqo5xfbul www.google.com e-mail three-level-building I'm wouldn't @trump #bad 1.2 Hi, my name is: Jon!? Next sentence."
        self.assertEqual(to_string(ta.normalize_tweet_for_frequency_analysis(s)), "e mail three level building i m wouldn t trump bad 12 hi my name is jon next sentence")
         
#    def test_correct_repeating_characters(self):
#        s = "Yesssssss I finalllyyyyyyyy did ittttttttt!"
#        self.assertEqual(ta.correct_repeating_characters(s), "yes i finally did it")
        
if __name__ == '__main__':
    unittest.main()
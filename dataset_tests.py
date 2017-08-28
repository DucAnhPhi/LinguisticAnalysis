#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 16:18:02 2017

Unit tests for dataset.py

@author: duc
"""

import unittest
import dataset as ds
import numpy as np
from flesch_kincaid import get_flesch_grade_level as lvl
from nltk.corpus import cmudict

pronDict = cmudict.dict()


class DatasetTests(unittest.TestCase):

    def test_normalize(self):
        m = np.array([[1, 4, 0.5, 9], [0, 2, 0.2, 2], [0, 1, 0.01, 8], [1, 2.5, 0.3, 3]])
        norm = np.array([[1, 1, 1, 1], [0, 0.5, 0.4, 0.222], [0, 0.25, 0.02, 0.888], [1, 0.625, 0.6, 0.333]])
        decimal = 3
        np.testing.assert_array_almost_equal(ds.normalize(m), norm, decimal)
    
    def test_combined_keywords(self):
        t1 = [[["fake", "media"]], [["fake", "news"]]]
        t2 = [[["women", "hillary"]], [["media", "trump"]]]
        keywords = set(["fake", "media", "news", "women", "hillary", "trump"])
        self.assertEqual(ds.get_combined_keywords(t1, t2), keywords)
        
    def test_keywords_count(self):
        t =  [["make", "america", "great", "again"],["america", "was", "great"]]
        dict = {"make": 0, "america": 0, "great": 0, "again": 0, "was": 0}
        counted = {"make": 1, "america": 2, "great": 2, "again": 1, "was": 1}
        self.assertEqual(ds.get_keywords_count(t, dict), counted)
        
    def test_extract_features(self):
        t =  ["Make america great again!", "America was great! Hillary Clinton"]
        norm = [[["make", "america", "great", "again"]],[["america", "was", "great"], ["hillary", "clinton"]]]
        count = {"make": 0, "america": 0, "great": 0, "again": 0, "was": 0, "hillary": 0, "clinton": 0}
        features = [
                [4, 1, lvl(norm[0], pronDict), 1, 1, 1, 1, 0, 0, 0],
                [2.5, 1, lvl(norm[1], pronDict), 0, 1, 1, 0, 1, 1, 1]
        ]
        print(features)
        self.assertEqual(ds.extract_features(t, norm, count, pronDict), features)
    
    def test_positive_negative_amount(self):
        m = [[0, 1, 0.5, 1, 0.02], [1, 1, 1, 0.3, 0.99], [1, 0, 0, 0, 0]]
        n = np.array(m)
        self.assertEqual(ds.get_positive_negative_amount(m), (2, 1))
        self.assertEqual(ds.get_positive_negative_amount(n), (2, 1))
    
    def test_training_set(self):
        # should have 50% positive and 50% negative examples
        ts = ds.divide_data_into_sets(ds.get_prepared_tweet_data("realDonaldTrump", "HillaryClinton"), 0.1, 0.1, 0.8)[2]
        count = ds.get_positive_negative_amount(ts)
        self.assertEqual(count[0], count[1])
        
if __name__ == '__main__':
    unittest.main()
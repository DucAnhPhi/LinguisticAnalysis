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
        t1 = ["Fake media.", "Fake news."]
        t2 = ["Women Hillary", "Media Trump"]
        keywords = {"fake": 0, "media": 0, "news": 0, "women": 0, "hillary": 0, "trump": 0}
        self.assertEqual(ds.get_combined_keywords(t1, t2), keywords)

    def test_keywords_count(self):
        t =  [["make", "america", "great", "again"],["america", "was", "great"]]
        dictionary = {"make": 0, "america": 0, "great": 0, "again": 0, "was": 0}
        counted = {"make": 1, "america": 2, "great": 2, "again": 1, "was": 1}
        self.assertEqual(ds.get_keywords_count(t, dictionary), counted)

    def test_extract_features(self):
        t =  "Make america great again!"
        norm = [["make", "america", "great", "again"]]
        count = {"make": 0, "america": 0, "great": 0, "again": 0}
        features = [4, 1, lvl(norm, pronDict), 1, 1, 1, 1]
        self.assertEqual(ds.extract_features(t, count, pronDict), features)

    def test_positive_negative_amount(self):
        m = [[0, 1, 0.5, 1, 0.02], [1, 1, 1, 0.3, 0.99], [1, 0, 0, 0, 0]]
        n = np.array(m)
        self.assertEqual(ds.get_positive_negative_amount(m), (2, 1))
        self.assertEqual(ds.get_positive_negative_amount(n), (2, 1))

    def test_training_set(self):
        dataset = ds.Dataset("realDonaldTrump", "HillaryClinton", 0.8)
        # should have 50% positive and 50% negative examples
        trainSet = dataset.trainSet
        count = ds.get_positive_negative_amount(trainSet)
        self.assertEqual(count[0], count[1])


if __name__ == '__main__':
    np.set_printoptions(threshold = 10000, precision=4, suppress=True)
    unittest.main()

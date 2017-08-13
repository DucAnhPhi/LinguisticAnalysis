#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 14:40:24 2017

Unittests for flesch_kincaid.py

@author: duc
"""

import unittest
import flesch_kincaid as fk


def to_string(tokenized):
    return " ".join(sum(tokenized, []))

class FleschKincaidTests(unittest.TestCase):
    
    def test_normalize(self):
        s = r"RT @Staircase2: 💪🔥 >:( xd <3 :'D http://t.co/rlqo5xfbul www.google.com e-mail three-level-building I'm wouldn't @trump #bad 1.2 Hi, my name is: Jon!? Next sentence."
        self.assertEqual(to_string(fk.normalize(s)), "e mail three level building i m wouldn t trump bad 12 hi my name is jon next sentence")

if __name__ == '__main__':
    unittest.main()
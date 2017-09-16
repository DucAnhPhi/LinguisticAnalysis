#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 21:02:22 2017

@author: duc
"""

# a list of emoticons containing letters or numbers,
# which the TweetTokenizer does or may not know
# reason: emoticons without letters or numbers are removed easily
# without the need of tokenization

emoticons = [
    ":-3",
    ":3",
    "8:o)",
    "8=o)",
    "8-)",
    "8)",
    "8=)",
    "b)",
    "b|",
    ":o)",
    ":o",
    ";o",
    "=o",
    ":-o",
    ">:o",
    "o:-)",
    "o:)",
    "0:-)",
    "0:)",
    "3:-)",
    "3:)",
    ":c)",
    ":-c",
    ":c",
    ":-d",
    ":'d",
    ":d",
    ":dd",
    ":ddd",
    "xd",
    "xdd",
    "xddd",
    "xdddd",
    "xddddd",
    "xdddddd",
    "d-':",
    "d:<",
    "d;",
    "d=",
    "8-d",
    "x-d",
    "=d",
    "=dd",
    "=3",
    "b^d",
    ";d",
    ":p",
    ";p",
    "X-p",
    ":-p",
    ":b",
    ":-b",
    "=b",
    "=p",
    ">:p",
    ":l",
    "=l",
    ":S",
    "\o/",
    "v.v",
    "o_o",
    "o-o",
    "<3",
    "<33",
    "<333",
    "<3333",
    "</3"

]

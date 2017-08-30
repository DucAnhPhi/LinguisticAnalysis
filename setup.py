#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 16:09:27 2017

Setup script for downloading all dependencies

@author: duc
"""

import pip
import nltk


dependencies = [
    'certifi==2017.7.27.1',
    'chardet==3.0.4',
    'cycler==0.10.0',
    'idna==2.6',
    'matplotlib==2.0.2',
    'nltk==3.2.4',
    'numpy==1.13.1',
    'oauthlib==2.0.2',
    'pyparsing==2.2.0',
    'python-dateutil==2.6.1',
    'pytz==2017.2',
    'requests==2.18.4',
    'requests-oauthlib==0.8.0',
    'six==1.10.0',
    'tweepy==3.3.0',
    'urllib3==1.22'
]

nltk_data = [
    'cmudict',
    'stopwords',
    'twitter_samples',
    'punkt'
]

def install():
    for d in dependencies:
        pip.main(['install', d])
    
    for data in nltk_data:
        nltk.download(data)


if __name__ == '__main__':
    install()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 18:23:39 2017

Prepare datasets for neural_network.py

@author: duc
"""

import numpy as np


def getXOR():
    input = np.array([[0,0],[1,0],[0,1],[1,1]])
    output = np.array([[0],[1],[1],[0]])
    return(input, output)


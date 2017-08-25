#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 18:23:39 2017

@author: duc
"""

import numpy as np

def getInput():
    input = np.array([[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]])
    output = np.array([[0,0,0],[0,0,1],[0,0,1],[0,0,0],[0,0,0],[0,1,0],[0,1,0],[0,0,0]])
    return(input, output)

def getInput2():
    input = np.array([[0,0],[1,0],[0,1],[1,1]])
    output = np.array([[0],[1],[1],[0]])
    return(input, output)

def getInput3():
    input = np.array([[0.35, 0.9], [0.1, -0.7]])
    output = np.array([[0.5],[0.35]])
    return (input,output)
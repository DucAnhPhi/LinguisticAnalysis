#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 00:24:39 2017

Tests for neural_network.py

@author: duc
"""

import numpy as np
import unittest
import neural_network as nn

class NeuralNetworkTests(unittest.TestCase):
    
    def test_xor(self):
        input = np.array([[0,0],[1,0],[0,1],[1,1]])
        output = np.array([[0.],[1.],[1.],[0.]])
        net = nn.NeuralNetwork(30000,1,2,1,1,(input, output))
        net.train()
        decimal = 1
        np.testing.assert_array_almost_equal(net.forward_pass(input)[-1], output, decimal)
        
if __name__ == '__main__':
    unittest.main()
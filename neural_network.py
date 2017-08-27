#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 20:30:37 2017
Neural network for supervised machine learning
@author: duc
"""

import numpy as np
from numpy import dot
import dataset
   

def concat_bias(bias, x):
    rows = x.shape[0]
    biasMatrix = np.empty(rows)
    biasMatrix.fill(bias)
    # concat both matrices horizontally
    return np.c_[biasMatrix.T, x]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def dsigmoid(x):
    return x * (1.0 - x)

class NeuralNetwork:
    
    bias = 1
    
    def __init__(self, trainingIterations, learnRate, inputNeurons, hiddenLayers, outputNeurons, data):

        self.trainingIterations = trainingIterations
        self.learnRate = learnRate

        # intialize amount of input, output and hidden neurons
        self.inputNeurons = inputNeurons
        self.outputNeurons = outputNeurons
        self.hiddenLayers = hiddenLayers

        # initialize input data
        self.input = data[0]
        print("input:\n",self.input)
        # input nodes
        self.inputColumns = data[0].shape[1]
        # amount of input data
        self.m = data[0].shape[0]
        
        # initialize output data
        self.output = data[1]
        #self.output = np.array([[0.5], [0.35]])
        print("output:\n",self.output)

        # seed random generator
        #np.random.seed(7)

        # initialize weights randomly from -0.5 to 0.5
        self.thetas = []
        for i in range(0, hiddenLayers):
            self.thetas.append(np.random.rand(self.inputColumns + 1, inputNeurons)-0.5)
            print("initial theta", i+1, ":\n", self.thetas[i])
        self.thetas.append(np.random.rand(inputNeurons + 1, outputNeurons)-0.5)
        print("initial theta", hiddenLayers+1,":\n",self.thetas[hiddenLayers])

    def train(self):

        for i in range(0, self.trainingIterations):
            # do forwardpass
            fp = self.forward_pass(self.input)

            # update weights/thetas for next iteration
            self.update_thetas(fp)

        print("Prediction =\n", self.forward_pass(self.input)[-1])

    def forward_pass(self, inputData):
        # store activations
        a = []
        # input layer with bias at index 0
        a.append(inputData)
        for i in range(0, len(self.thetas)):
            # activation of a layer
            a.append(sigmoid(dot(concat_bias(self.bias, a[i]), self.thetas[i])))

        # return activations
        return a

    def update_thetas(self, a):
        ratio = self.learnRate / self.m

        # do backpropagation

        # all thetas transposed without bias except first theta
        tempThetas = []
        for i in range(1, len(self.thetas)):
            tempThetas.append(self.thetas[i].T[:, 1:len(self.thetas[i].T[0])])

        # compute all deltas
        # initialize delta array
        d = [0] * len(self.thetas)
        # initialize first delta at last position
        d[-1] = (a[-1] - self.output) * dsigmoid(a[-1])
        # compute as many deltas as there are thetas
        for j in range(len(self.thetas)-2, -1, -1):
            d[j] = dot(d[j+1], tempThetas[j]) * dsigmoid(a[j+1])

        # compute change and update weights
        for k in range(len(self.thetas)-1, -1, -1):
            self.thetas[k] = self.thetas[k] - (ratio * dot(concat_bias(self.bias, a[k]).T, d[k]))

if __name__ == '__main__':
    np.set_printoptions(threshold = 1000, precision=4, suppress=True)
    nn = NeuralNetwork(3000, 1, 2, 1, 1, dataset.getInput2())
    nn.train()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 20:09:08 2017

@author: duc
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 20:30:37 2017

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
    
    def __init__(self, trainingIterations, learnRate, inputNeurons, outputNeurons):
        
        self.trainingIterations = trainingIterations
        self.learnRate = learnRate
        
        # intialize amount of input and output neurons
        self.inputNeurons = inputNeurons
        self.outputNeurons = outputNeurons

        # initialize input data
        data = dataset.getInput2()
        self.input = data[0]
        # input nodes
        self.inputColumns = data[0].shape[1]
        # amount of input data
        self.m = data[0].shape[0]
        
        # initialize output data
        self.output = data[1]
        
        # seed random generator
        np.random.seed(7)
        
        # initialize weights randomly from -0.5 to 0.5
        self.theta1 = np.random.rand(self.inputColumns + 1, inputNeurons)-0.5
        self.theta2 = np.random.rand(inputNeurons + 1, outputNeurons)-0.5
        print("initial theta1=\n",self.theta1)
        print("initial theta2=\n",self.theta2)
        
    def train(self):
        
        for i in range(0, self.trainingIterations):
            # do forwardpass
            
            # input layer with bias
            vb1 = concat_bias(self.bias, self.input)
            # activation of hidden layer
            a2 = sigmoid(dot(vb1, self.theta1))
            # activation of hidden layer with bias
            ab2 = concat_bias(self.bias, a2)
            # output layer
            a3 = sigmoid(dot(ab2, self.theta2))

            # update weights/thetas for next iteration
            updatedThetas = self.get_updated_thetas(vb1, ab2, a2, a3)
            self.theta1 = updatedThetas[0]
            self.theta2 = updatedThetas[1]
        
#        print("Training complete")
#        print("Theta1:\n", self.theta1)
#        print("Theta2:\n", self.theta2)
#        print("Theta3:\n", self.theta3)
        # input layer with bias
        vb1 = concat_bias(self.bias, self.input)
        # activation of hidden layer
        a2 = sigmoid(dot(vb1, self.theta1))
        # activation of hidden layer with bias
        ab2 = concat_bias(self.bias, a2)
        # output layer
        a3 = sigmoid(dot(ab2, self.theta2))

        print("Prediction =\n", a3)

    def get_updated_thetas(self, vb1, ab2, a2, a3):
        ratio = self.learnRate / self.m
        
        # do backpropagation
        
        # thetas transposed without bias
        theta2 = self.theta2.T[:, 1:len(self.theta2.T[0])]
        
        #reuseable deltas
        delta = ((a3 - self.output) * dsigmoid(a3))
        
        # compute updated weights
        newTheta2 = self.theta2 - (ratio * dot(ab2.T, delta))
        newTheta1 = self.theta1 - (ratio * dot(vb1.T, dot(delta, theta2) * dsigmoid(a2)))
        
        return (newTheta1, newTheta2)
        

if __name__ == '__main__':
    np.set_printoptions(threshold = 1000, precision=4, suppress=True)
    nn = NeuralNetwork(5000, 1, 2, 2)
    nn.train()
#    matrix = np.array([[0,0,0],[1,1,1],[-1,-1,-1]])
#    print(dsigmoid(matrix))
#    print(matrix)
#    bias = np.array([[1],[1],[1]])
#    print(concat_bias(matrix, 1))
#    print(matrix)
    
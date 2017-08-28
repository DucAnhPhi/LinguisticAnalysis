#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 20:30:37 2017
Neural network for supervised machine learning
@author: duc
"""

import numpy as np
from numpy import dot
import matplotlib.pyplot as plt
import dataset as ds


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

def get_binary(prediction):
        def to_binary(a):
            if a > 0.5:
                return 1
            else:
                return 0
        vfunc = np.vectorize(to_binary)
        return vfunc(prediction)

class NeuralNetwork:

    bias = 1

    def __init__(
            self, trainingIterations, learnRate, inputNeurons, hiddenLayers,
            outputNeurons, inputData, outputData, cvInputData, cvOutputData,
            testInputData, testOutputData
    ):

        self.trainingIterations = trainingIterations
        self.learnRate = learnRate

        # intialize amount of input, output and hidden neurons
        self.inputNeurons = inputNeurons
        self.outputNeurons = outputNeurons
        self.hiddenLayers = hiddenLayers

        # initialize training data
        self.input = inputData
        print("input:\n",self.input)
        # input nodes
        self.inputColumns = inputData.shape[1]
        # amount of input data
        self.m = inputData.shape[0]
        self.output = outputData
        #self.output = np.array([[0.5], [0.35]])
        print("output:\n",self.output)

        # initialize cross validation data
        self.cvInput = cvInputData
        self.cvOutput = cvOutputData

        # initialize test data
        self.testInput = testInputData
        self.testOutput = testOutputData

        # initialize train errors
        self.trainErrors = []

        # initialize cross validation errors
        self.cvErrors = []

        # initialize prediction rates
        self.predictionRates = []

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

            # keep track of errors of different data sets
            if len(self.cvInput) and len(self.cvOutput):
                self.set_cv_error()
            self.set_training_error(fp[-1])

            # keep track of how well this network does by using test data
            if len(self.testInput) and len(self.testOutput):
                self.set_prediction_rate()

        print("Prediction =\n", self.forward_pass(self.input)[-1])
        self.plot()

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

    def set_cv_error(self):
        m = self.cvInput.shape[0]
        prediction = self.forward_pass(self.cvInput)[-1]
        cvError = sum(sum(np.square(prediction - self.cvOutput))) / (2 * m)
        self.cvErrors.append(cvError)

    def set_training_error(self, prediction):
        trainError = sum(sum(np.square(prediction - self.output))) / (2 * self.m)
        self.trainErrors.append(trainError)

    def set_prediction_rate(self):
        m = self.testInput.shape[0]
        predictionRate = 0
        prediction = self.forward_pass(self.testInput)[-1]
        # convert to binary data
        prediction = get_binary(prediction)
        for index, e in enumerate(prediction):
            if np.array_equal(e, self.testOutput[index]):
                predictionRate += 1
        self.predictionRates.append(predictionRate / m)

    def plot(self):
        x = np.arange(0, self.trainingIterations, 1)

        #if len(self.trainErrors) and len(self.cvErrors):
        # training error
        plt.figure(1)
        plt.ylabel("error")
        plt.xlabel("iterations")
        if len(self.cvErrors):
            plt.plot(x, self.trainErrors, 'bs', x, self.cvErrors, 'ro')
        else:
            plt.plot(x, self.trainErrors, 'bs')

        if len(self.predictionRates):
            # prediction rate
            plt.figure(2)
            plt.ylabel("prediction rate")
            plt.xlabel("iterations")
            plt.plot(x, self.predictionRates, 'g^')

        plt.show()


if __name__ == '__main__':
    np.set_printoptions(threshold = 1000, precision=4, suppress=True)
    data = ds.divide_data_into_sets(ds.get_prepared_tweet_data("realDonaldTrump", "HillaryClinton"), 0.1, 0.1, 0.8)
    # test data
    testInput = data[0][:, 1:]
    testOutput = data[0][:, [0]]
    # cross validation data
    cvInput = data[1][:, 1:]
    cvOutput = data[1][:, [0]]
    # training data
    input = data[2][:, 1:]
    output = data[2][:, [0]]
    nn = NeuralNetwork(30000,1,input.shape[1],3,1, input, output, cvInput, cvOutput, testInput, testOutput)
    nn.train()
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
from nltk.corpus import cmudict


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
            outputNeurons, inputData, outputData, validationInputData, validationOutputData
    ):

        self.trainingIterations = trainingIterations
        self.learnRate = learnRate

        # intialize amount of input, output and hidden neurons
        self.inputNeurons = inputNeurons
        self.outputNeurons = outputNeurons
        self.hiddenLayers = hiddenLayers

        # initialize training data
        self.input = inputData
        # input nodes
        self.inputColumns = inputData.shape[1]
        # amount of input data
        self.m = inputData.shape[0]
        self.output = outputData

        # initialize validation data
        self.validationInput = validationInputData
        self.validationOutput = validationOutputData

        # initialize train errors
        self.trainErrors = []

        # initialize validation errors
        self.validationErrors = []

        # initialize prediction rates
        self.predictionRates = []

        # seed random generator
        #np.random.seed(7)

        # initialize weights randomly from -0.5 to 0.5
        self.thetas = []
        for i in range(0, hiddenLayers):
            self.thetas.append(np.random.rand(self.inputColumns + 1, inputNeurons)-0.5)
        self.thetas.append(np.random.rand(inputNeurons + 1, outputNeurons)-0.5)

    def train(self):

        for i in range(0, self.trainingIterations):
            # do forwardpass
            fp = self.forward_pass(self.input)

            # update weights/thetas for next iteration
            self.update_thetas(fp)

            # keep track of how well this network performs
            if len(self.validationInput) and len(self.validationOutput):
                self.set_validation_error()
                self.set_prediction_rate()
            self.set_training_error(fp[-1])

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

    def set_validation_error(self):
        m = self.validationInput.shape[0]
        prediction = self.forward_pass(self.validationInput)[-1]
        validationError = sum(sum(np.square(prediction - self.validationOutput))) / (2 * m)
        self.validationErrors.append(validationError)

    def set_training_error(self, prediction):
        trainError = sum(sum(np.square(prediction - self.output))) / (2 * self.m)
        self.trainErrors.append(trainError)

    def set_prediction_rate(self):
        m = self.validationInput.shape[0]
        predictionRate = 0
        prediction = self.forward_pass(self.validationInput)[-1]
        # convert to binary data
        prediction = get_binary(prediction)
        for index, e in enumerate(prediction):
            if np.array_equal(e, self.validationOutput[index]):
                predictionRate += 1
        self.predictionRates.append(predictionRate / m)

    def plot(self):
        x = np.arange(0, self.trainingIterations, 1)

        # training error
        plt.figure(1)
        plt.ylabel("error")
        plt.xlabel("iterations")
        if len(self.validationErrors):
            plt.plot(x, self.trainErrors, 'b-', x, self.validationErrors, 'r-')
        else:
            plt.plot(x, self.trainErrors, 'b-')

        if len(self.predictionRates):
            # prediction rate
            plt.figure(2)
            plt.ylabel("prediction rate")
            plt.xlabel("iterations")
            plt.plot(x, self.predictionRates, 'g-')

        plt.show()


if __name__ == '__main__':
    np.set_printoptions(threshold = 1000, precision=4, suppress=True)
    user1 = input("Enter the first Twitter username:\n")
    user2 = input("Enter the second Twitter username:\n")
    trainDataAmount = float(input("Enter amount of training data (0.8 recommended):\n"))
    rounds = int(input("Enter training iterations:\n"))
    learnRate = float(input("Enter learn rate:\n"))
    hiddenLayers = int(input("Enter amount of hidden layers:\n"))
    data = ds.Dataset(user1, user2, trainDataAmount)
    # validation data
    validationInput = data.validationSet[:, 1:]
    validationOutput = data.validationSet[:, [0]]
    # training data
    trainInput = data.trainSet[:, 1:]
    trainOutput = data.trainSet[:, [0]]
    nn = NeuralNetwork(
        rounds,                     # training iterations
        learnRate,                  # learn rate
        trainInput.shape[1],        # amount of input neurons
        hiddenLayers,               # amount of hidden layers
        1,                          # amount of output neurons
        trainInput,                 # training input data
        trainOutput,                # training output data
        validationInput,            # validation input data
        validationOutput            # validation output data
    )
    nn.train()
    print("The Neural Network has been trained.")
    while True:
        tweet = input("Enter a tweet to get a prediction:\n")
        pronDict = cmudict.dict()
        featureVector = ds.extract_features(tweet, data.combinedKeywords, pronDict)
        if len(featureVector) == 0:
            print("Cannot get a prediction for given tweet.")
        else:
            prediction = nn.forward_pass(np.array([featureVector]))[-1]
            print(prediction)
            if prediction > 0.5:
                print("This tweet is probably written by ", user1)
            else:
                print("This tweet is probably written by ", user2)

import numpy as np
import csv

class NeuralNetwork: #1 Hidden Layer:
    def __init__(self,n_Neurons):
        self.n_Neurons = n_Neurons
      
    def SetX(self,x):
        #ReShape (Matrix representation needed for numpy operations):
        if len(x.shape) == 1:
            self.x = np.expand_dims(x_orgiginal,axis=0).T
        else:
            self.x = np.array(x)
      
        #Add Bias Column for bias (instead of handling the bias as an extra variable)
        self.x = add1(self.x)

    def init(self, x, y):
        self.input      = np.array(x)
        self.weights1   = np.random.rand(self.input.shape[1],4) 
        self.weights2   = np.random.rand(4,1)                   
        self.y          = np.array(y)
        # self.output     = np.zeros(self.y.shape)

    # # def feedforward(self):
    # #     self.layer1 = np.tanh(np.dot(self.input, self.weights1))
    # #     self.output = np.tanh(np.dot(self.layer1, self.weights2))

    # def backprop(self):
    #     # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
    #     d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) * sigmoid_derivative(self.output)))
    #     d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1)))

    #     # update the weights with the derivative (slope) of the loss function
    #     self.weights1 += d_weights1
    #     self.weights2 += d_weights2

    def OpenData(self,textfile,xwr):
        # f = open(textfile,xwr)
        # f.write("Sequences 100\n")
        # f.write("stateIndex|stateFeatures|state|reward|actionIndex|greed\n"))
        x = []
        csv.register_dialect('myDialect', delimiter = '|')

        with open(textfile,xwr) as csvFile:
            reader = csv.reader(csvFile, dialect='myDialect')
            for row in reader:
                x.append(row)
        csvFile.close()
        return x

    #basis functions
        def add1(X):
        bias_column = np.ones((X.shape[0], 1))
        return np.hstack([bias_column, X])

        def dtanh(x):
        x = 1-np.tanh(x)^2
        
        def sumCol(m):
        return [sum(col) for col in zip(*m)]
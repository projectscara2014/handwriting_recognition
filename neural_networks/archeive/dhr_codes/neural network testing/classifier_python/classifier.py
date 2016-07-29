import random
import numpy as np
import pickle
import os

input_layer_neurons = 400
hidden_layer_neurons = 10
output_layer_neurons = 5

WORKING_DIR = os.getcwd()
BIAS_PATH = WORKING_DIR+"\classifier_python\\biases.pkl"
WEIGHT_PATH = WORKING_DIR+"\classifier_python\weights.pkl"

class Network():

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = pickle.load(open(BIAS_PATH))
        self.weights = pickle.load(open(WEIGHT_PATH))

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid_vec(np.dot(w, a)+b)
            # print(a)
        return a

 
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))
sigmoid_vec = np.vectorize(sigmoid)

net = Network([input_layer_neurons,hidden_layer_neurons,output_layer_neurons])

def classifier(image) : 
    global net
    new_image = []
    for row in image : 
        for pixel in row : 
            if(pixel == 255) :
                new_image.append([1])
            else : 
                new_image.append([0])
            # new_image.append(pixel)

    # result = np.argmax(net.feedforward(new_image))
    result = net.feedforward(new_image)
    max_index = 0
    max_value = 0
    # print(result)
    return result
    # for i in range(len(result)) : 
    #     if result[i] > max_value : 
    #         max_index = i
    #         max_value = result[i]
    # return i+10

def pure_result(im):
    global net
    result = net.feedforward(im)
    result = ['%.3f' %i[0] for i in result]
    return result
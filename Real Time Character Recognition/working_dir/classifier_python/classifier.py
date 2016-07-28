"""
    This script acts as a neural network classifier in absence of FPGA.
"""

import random
import numpy as np
import pickle

# input_layer_neurons = 784
# hidden_layer_neurons = 30
# output_layer_neurons = 10

input_layer_neurons = 400
hidden_layer_neurons = 10
output_layer_neurons = 5

import sys

WORKING_DIRECTORY = ''
SPLITTING_CHARACTER = ''
if sys.platform.startswith('win') : 
    SPLITTING_CHARACTER = '\{}'.format('')
elif sys.platform.startswith('darwin') : 
    SPLITTING_CHARACTER = '/'

def setup() : 
    '''
    Sets up the working directory for the entire project
    '''

    def locate_working_directory() : 
        working_directory = ''
        for element in __file__.split(SPLITTING_CHARACTER)[:-2] :
            working_directory += element + '{}'.format(SPLITTING_CHARACTER)
        return working_directory
    
    global WORKING_DIRECTORY
    WORKING_DIRECTORY = locate_working_directory()
    # print('working_directory --> ',WORKING_DIRECTORY)
    sys.path.append(WORKING_DIRECTORY)

class Network():

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = pickle.load(open(WORKING_DIRECTORY+'\classifier_python\\biases.pkl'))
        self.weights = pickle.load(open(WORKING_DIRECTORY+'\classifier_python\weights.pkl'))

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

setup()
net = Network([input_layer_neurons,hidden_layer_neurons,output_layer_neurons])
mapped_list = pickle.load(open(WORKING_DIRECTORY+'\classifier_python\character_map.pkl'))
print(mapped_list)

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

    result = np.argmax(net.feedforward(new_image))
    max_index = 0
    max_value = 0
    # print(result)
    return int(mapped_list[result])
    # for i in range(len(result)) : 
    #     if result[i] > max_value : 
    #         max_index = i
    #         max_value = result[i]
    # return i+10
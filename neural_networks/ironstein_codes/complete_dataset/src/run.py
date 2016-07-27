#------------------------ CONSTANTS ---------------------------
hidden_layer_neurons = 70
input_layer_neurons = 400
output_layer_neurons = 70
eta = 1.0
epochs = 30
mini_batch_size = 15
#--------------------------------------------------------------

#----------------------- INITIALIZATION ------------------------
import sys
SYSTEM_PATH_SEPERATOR = ''
if(sys.platform.startswith('darwin')) : 
	SYSTEM_PATH_SEPERATOR = '/'
elif sys.platform.startswith('win') : 
	SYSTEM_PATH_SEPERATOR = '\\'
else : 
	raise ValueError

def get_saving_directory() : 
	saving_directory = __file__.split(SYSTEM_PATH_SEPERATOR)[:-2]
	saving_directory.append('test_results')
	temp_saving_directory = ''
	for element in saving_directory : 
		temp_saving_directory += element + SYSTEM_PATH_SEPERATOR
	saving_directory = temp_saving_directory
	
	return saving_directory

GRAPHS_SAVING_DIRECTORY = get_saving_directory()

import dataset_loader
import network
import network2
import mnist_loader
import pickle

print('loading dataset ...')
training_data,test_data = dataset_loader.load_data()
# mini_batch_size = len(training_data) - 5
# training_data,test_data,validation_data = mnist_loader.load_data_wrapper()
# print(test_data[0])
print('loading dataset complete')

# print(training_data[0])
#----------------------------------------------------------------
import matplotlib.pyplot as plt

def loop() : 
	global GRAPHS_SAVING_DIRECTORY
	global mini_batch_size
	global epochs
	global hidden_layer_neurons,input_layer_neurons,output_layer_neurons
	
	net = network.Network([input_layer_neurons,hidden_layer_neurons,output_layer_neurons])
	net.SGD(training_data, epochs, mini_batch_size, eta, test_data=test_data)
	# net = network2.Network([input_layer_neurons,hidden_layer_neurons,output_layer_neurons])
	# net.SGD(training_data, epochs, mini_batch_size, eta, 1.0, evaluation_data=test_data)

	print(net.weights)
	print(net.biases)
	pickle.dump(net.weights,open('../test_results/weights.pkl','w'))
	pickle.dump(net.biases,open('../test_results/biases.pkl','w'))

	# for eta in [i*0.1 for i in range(50)][1:] :
	# 	net = network.Network([input_layer_neurons,hidden_layer_neurons,output_layer_neurons])
	# 	print('-------------- eta : ' + str(eta) + ' --------------' )
	# 	performance_list = net.SGD(training_data, epochs, mini_batch_size, eta, test_data=test_data)
	# 	epoch_list = [i for i in range(epochs)]
	# 	plt.plot(epoch_list,performance_list,'b-')
	# 	plt.ylim([0,10000])
	# 	plt.savefig(GRAPHS_SAVING_DIRECTORY + 'eta_' + str(eta) + '.png')
	# 	plt.clf()

loop()

# for i in range(10) : 
# 	# net = network.Network([400,hidden_layer_neurons,5])
# 	net = network.Network([400,hidden_layer_neurons,5])
# 	performance_list = net.SGD(training_data, epochs, mini_batch_size, 1.0, test_data=test_data)
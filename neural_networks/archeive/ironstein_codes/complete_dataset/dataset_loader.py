import numpy as np
import random
import cv2

dataset_file_name = 'all.npy'
percent_test_data = 30

def load_data() : 
	global dataset_file_name,percent_test_data
	data = np.load('../data/' + dataset_file_name).tolist()
	randomized_data = []

	while len(data) != 0 : 
		i = random.randint(0,len(data)-1)
		randomized_data.append(data[i])
		data.pop(i)
		

	def vectorized_result(j) : 
		e = np.zeros((70,1))
		e[j-10] = 1.0
		return e

	test_set_length = (percent_test_data*len(randomized_data))/100
	training_set_length = len(randomized_data) - test_set_length

	training_data = randomized_data[:training_set_length]
	test_data = randomized_data[training_set_length:len(randomized_data)]

	new_training_data = []
	new_test_data = []

	for character in training_data :
		ts1 = np.reshape(character[0],(400,1))
		ts2 = np.zeros((400,1),dtype=np.float32)
		for i in range(len(ts1)) :
			ts2[i] = ts1[i]/255.0
		new_training_data.append((ts2,vectorized_result(character[1])))

	for character in test_data :
		ts1 = np.reshape(character[0],(400,1))
		ts2 = np.zeros((400,1),dtype=np.float32)
		for i in range(len(ts1)) :
			ts2[i] = ts1[i]/255.0
		new_test_data.append((ts2,character[1]-10))

	# for character in randomized_data : 
	# 	new_character = np.reshape(character[0],(400,1))
	# 	new_character_ = np.zeros((400,1))
	# 	for i in range(len(new_character)) :
	# 		new_character_[i] = new_character[i]/255.0
	# 	new_data.append(new_character_)
	# 	new_expected_outputs.append(vectorized_result(character[1]))
	return [new_training_data,new_test_data]

# load_data()
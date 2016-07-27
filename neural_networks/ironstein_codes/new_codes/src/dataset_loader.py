import numpy as np
import random
import cv2

dataset_file_name = 'database_abcde_tilted.npy'
percent_test_data = 10

def load_data() : 
	global dataset_file_name,percent_test_data
	data = np.load('../data/' + dataset_file_name).tolist()
	randomized_data = []
	character_array = []

	while len(data) != 0 : 
		i = random.randint(0,len(data)-1)
		randomized_data.append(data[i])
		if data[i][1] not in character_array : 
			character_array.append(data[i][1])
		data.pop(i)
	# to arrange in ascending order
	character_array.sort()

	def vectorized_result(j) : 
		e = np.zeros((len(character_array),1))
		e[character_array.index(j)] = 1.0
		return e

	test_set_length = (percent_test_data*len(randomized_data))/100
	training_set_length = len(randomized_data) - test_set_length

	training_data = randomized_data[:training_set_length]
	test_data = randomized_data[training_set_length:len(randomized_data)]

	new_training_data = []
	new_test_data = []
	print('\tcompleted data randomization')

	for character in training_data :
		ts1 = np.reshape(character[0],(400,1))
		# ts2 = np.zeros((400,1),dtype=np.float32)
		# for i in range(len(ts1)) :
		# 	ts2[i] = ts1[i]/255.0
		# new_training_data.append((ts2,vectorized_result(character[1])))
		new_training_data.append((ts1,vectorized_result(character[1])))
	print('\tcompleted loading training data')

	for character in test_data :
		ts1 = np.reshape(character[0],(400,1))
		# ts2 = np.zeros((400,1),dtype=np.float32)
		# for i in range(len(ts1)) :
		# 	ts2[i] = ts1[i]/255.0
		# new_test_data.append((ts2,character[1]-10))
		new_test_data.append((ts1,character_array.index(character[1])))
	print('\tcompleted loading test data')

	# for character in randomized_data : 
	# 	new_character = np.reshape(character[0],(400,1))
	# 	new_character_ = np.zeros((400,1))
	# 	for i in range(len(new_character)) :
	# 		new_character_[i] = new_character[i]/255.0
	# 	new_data.append(new_character_)
	# 	new_expected_outputs.append(vectorized_result(character[1]))
	return [new_training_data,new_test_data,character_array]

# load_data()
# training_data,test_data = load_data()
# for i in range(30) : 
# 	print(test_data[i])
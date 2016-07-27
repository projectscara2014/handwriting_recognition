import os
import random
import pickle

working_directory_list = __file__.split('/')[:-1]
working_directory = ''
for element in working_directory_list : 
	working_directory += element + '/'

module_location = working_directory + 'dual_port_ROM.v'

weights_array = pickle.load(open('./weights.pkl','r'))
biases_array = pickle.load(open('./biases.pkl','r'))

weight_array = []

layer_weight_array_count = 0
neuron_weight_array_count = 0
weight_array_count = 0
bias_array_count = 0

# -----------------

# 0_0001_11111010000
#sign magnitude precision 

def integer_to_fixed_point_format(integer) : 

	# print(integer)
	# list_ = str(integer).split('.')

	# precision = float('0.' + list_[1])
	# print(precision)

	# new_precision = bin(int(precision*(2**11)))[:10]
	# new_precision = new_precision.replace('0b','')
	
	# # if(len(new_precision) > 11) : 
	# # 	new_precision = new_precision[:11] 
	# for i in range(11-len(new_precision)):
	# 	new_precision = '0' + new_precision


	# magnitude = int(list_[0])
	# if (magnitude < 0):
	# 	sign = 1
	# else:
	# 	sign = 0


	# magnitude = abs(magnitude)
	# magnitude = bin(int(magnitude))
	# new_magnitude = magnitude.replace("0b","")

	# for i in range(4-len(new_magnitude)) : 
	# 	new_magnitude = '0' + new_magnitude

	# final_string = "16'b" + str(sign) + "_" + str(new_magnitude)+ "_" + str(new_precision)
	# return final_string

	sign = '0'
	if integer < 0 : 
		sign = '1'

	new_integer = bin(int(abs(integer)*(2**11))).replace('0b','')
	new_integer = sign + '0'*(15-len(new_integer)) + new_integer
	return new_integer

# -------------

for layer_weight_array,layer_bias_array in zip(weights_array,biases_array) : 
	layer_weight_array_count += 1
	print('layer_weight_array_count : ' + str(layer_weight_array_count))
	for neuron_weight_array,neuron_bias_array in zip(layer_weight_array,layer_bias_array) : 
		neuron_weight_array_count += 1
		print('neuron_weight_array_count : ' + str(neuron_weight_array_count))
		for element in neuron_weight_array : 
			weight_array_count += 1
			print('weight_array_count : ' + str(weight_array_count))
			if(element > 15) : 
				weight_array.append(integer_to_fixed_point_format(15))
			elif(element < -15) :
				weight_array.append(integer_to_fixed_point_format(-15))
			else : 
				weight_array.append(integer_to_fixed_point_format(element))
		for element in neuron_bias_array :
			bias_array_count += 1
			print('bias_array_count : ' + str(bias_array_count)) 
			if(element > 15) : 
				weight_array.append(integer_to_fixed_point_format(15))
			elif(element < -15) : 
				weight_array.append(integer_to_fixed_point_format(-15))
			else : 
				weight_array.append(integer_to_fixed_point_format(element))

module_string = ''
module_string += 'module ROM(\n\tinput wire clk,'
module_string += '\n\tinput wire enable,'
module_string += '\n\tinput wire [11:0] address,'
module_string += '\n\toutput reg [15:0] data'
module_string += '\n\t);\n\n'
module_string += '\treg [15:0] weights [4050:0x];\n\n'
module_string += '\tinitial begin\n'
for i in range(len(weight_array)) : 
	module_string += '\t\tweights[' + str(i) + '] <= ' + str(weight_array[i]) + ';\n'
module_string += '\tend\n\n'
module_string += '\n\talways @(negedge(clk)) begin'
module_string += '\n\t\tif(enable) begin'
module_string += '\n\t\t\tcase(address)'
for i in range(len(weight_array)) : 
	if(i < 1000) :
		module_string += "\n\t\t\t\t12'd" + str(i) + '\t\t: data <= ' + \
			"weights[" + str(i) + '];'
	else : 
		module_string += "\n\t\t\t\t12'd" + str(i) + '\t: data <= ' + \
			"weights[" + str(i) + '];'
module_string += "\n\t\t\t\tdefault\t\t: data <= 16'd0;"
module_string += '\n\t\t\tendcase'
module_string += '\n\t\tend else begin'
module_string += '\n\t\t\tdata <= data;'
module_string += '\n\t\tend'
module_string += '\n\tend'
module_string += '\n\nendmodule'

with open(module_location,'w') as module : 
	module.write(module_string)
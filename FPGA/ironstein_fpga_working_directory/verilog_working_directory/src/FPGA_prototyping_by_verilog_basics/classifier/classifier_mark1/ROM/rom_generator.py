import os
import random

working_directory_list = __file__.split('/')[:-1]
working_directory = ''
for element in working_directory_list : 
	working_directory += element + '/'

module_location = working_directory + 'dual_port_ROM.v'

for i in range(10) : 
	for j in range(400) : 
		weight_array.append(weights_array[(i*400)+j])
		weight_array.append(biases_array[i])
for i in range(5) : 
	for j in range(10) : 
		weight_array.append(weights_array[4000+(i*10)+j])
		weight_array.append(biases_array[10+i])

weight_array = [random.randint(1,255) for i in range(4051)]

module_string = ''
module_string += 'module ROM(\n\tinput wire clk,'
module_string += '\n\tinput wire enable,'
module_string += '\n\tinput wire [11:0] address,'
module_string += '\n\toutput reg [15:0] data1,'
module_string += '\n\toutput reg [15:0] data2'
module_string += '\n\t);\n\n'
module_string += '\treg [15:0] weights [4050:0];\n\n'
module_string += '\tinitial begin\n'
for i in range(len(weight_array)) : 
	module_string += '\t\tweights[' + str(i) + '] <= ' + str(weight_array[i]) + ';\n'
module_string += '\tend\n\n'
module_string += '\n\talways @(negedge(clk)) begin'
module_string += '\n\t\tif(enable) begin'
module_string += '\n\t\t\tcase(address)'
for i in range(len(weight_array)) : 
	if(i < 1000) :
		module_string += "\n\t\t\t\t12'd" + str(i) + '\t\t: data1 <= ' + \
			"weights[" + str(i) + '];'
	else : 
		module_string += "\n\t\t\t\t12'd" + str(i) + '\t: data1 <= ' + \
			"weights[" + str(i) + '];'


module_string += "\n\t\t\t\tdefault\t\t: data1 <= 16'd0;"
module_string += '\n\t\t\tendcase'
module_string += '\n\t\tend else begin'
module_string += '\n\t\t\tdata1 <= data1;'
module_string += '\n\t\tend'
module_string += '\n\tend'
module_string += '\n\n'

module_string += '\n\talways @(negedge(clk)) begin'
module_string += '\n\t\tif(enable) begin'
module_string += '\n\t\t\tcase(address)'
for i in range(len(weight_array)-1) : 
	if(i < 1000) :
		module_string += "\n\t\t\t\t12'd" + str(i) + '\t\t: data2 <= ' + \
			"weights[" + str(i+1) + '];'
	else : 
		module_string += "\n\t\t\t\t12'd" + str(i) + '\t: data2 <= ' + \
			"weights[" + str(i+1) + '];'
module_string += "\n\t\t\t\tdefault\t\t: data2 <= 16'd0;"
module_string += '\n\t\t\tendcase'
module_string += '\n\t\tend else begin'
module_string += '\n\t\t\tdata2 <= data2;'
module_string += '\n\t\tend'
module_string += '\n\tend'

module_string += '\n\nendmodule'

with open(module_location,'w') as module : 
	module.write(module_string)
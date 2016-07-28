import ccl_utils

def main(dict_space,count_space,coordinates_space,dimensions_space):
	print("dict_space:- "),
	print(dict_space)
	print("count_space:- "),
	print(count_space)
	print("coordinates_space:- "),
	print(coordinates_space)
	print("dimensions_space:- "),
	print(dimensions_space)
	decision_list = []
	length = 0
	height = 0
	for i in (dimensions_space):
		length = length + i[0]
		height = height + i[1]

	avg_length = length*1.0/len(dimensions_space)
	avg_height = height*1.0/len(dimensions_space)
	print (avg_length)
	print (avg_height) 

	for i in range(len(dimensions_space)):
		if (dimensions_space[i][0] > 30 and dimensions_space[i][0] < 50):
			if(dimensions_space[i][1] > 35 and dimensions_space[i][1] < 55):
				decision_list.append(i+1)
	
	print(decision_list)

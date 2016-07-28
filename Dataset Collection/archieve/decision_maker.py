def main(dimensions_space):
	area_list = []
	for dimension in dimensions_space:
		area_list.append(dimension[0]*dimension[1])

	max_area_value = max(area_list)
	max_area_index = area_list.index(max_area_value)

	relative_area_list = []
	for element in area_list:
		relative_area_list.append(element*1.0/max_area_value)

	return_index_list = []
	for i in range(len(relative_area_list)):
		if(relative_area_list[i]>0.6):
			return_index_list.append(i)

	return return_index_list
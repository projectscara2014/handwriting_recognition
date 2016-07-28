"""
	The second/ modified version of the primitive decision_maker.
	The script deals with deciding whether the given object should be allowed or rejected
		based on several parameters:
			> Length of the object
			> Breadth of the object
			> Area of the object
			> Distance from the center
			> Proximity to the Prime(or biggest) object
			> Area with respect to Prime object
	Also, early decision making functionality is added.
"""

if(__name__ == "__main__"):
	import auto_script_2_cropped_to_skin_cropped
	# print("yolo")
	import sys
	sys.exit(0)

def get_distance_from(a,b):
	d = ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5
	if(d == 0):
		d = 1
	return d

def take_early_decision(acceptance_list):
	if(len(acceptance_list) == 1):
		return acceptance_list

	intended_return_list = []
	for i in range(len(acceptance_list)):
		if(acceptance_list[i]>-50):
			intended_return_list.append(i)

	if(len(intended_return_list) == 1):
		return intended_return_list
	return False 

def print_(l):
	print("["),
	for i in range(len(l)):
		element = l[i]
		if(type(element).__name__ == "float"):
			s = str(element)
			s = s.split(".")
			s[1] = s[1][:3]
			s = ".".join(s)
			print(s),
		else:
			print(element),
		if(i != len(l)-1):
			print(","),
	print("]")

def main(image_args):
	image_size = image_args.pop(0)
	image_center = [image_size[2],image_size[3]]
	# print("image_center:- "),
	# print(image_center)
	args_length_list = range(len(image_args))
	
	### CREATE ALL ARRAYS ###
	acceptance_list = [0 for element in image_args]

	decision = take_early_decision(acceptance_list)
	if(decision != False):
		return decision

	length_list = []
	height_list = []
	center_list = []
	area_list = []
	# image_length_ratio = []
	# image_height_ratio = []
	for element in image_args:
		length_list.append(element[0])
		height_list.append(element[1])
		center_list.append([element[2],element[3]])
		area_list.append(element[0]*element[1])
		# image_length_ratio.append(image_size[0]*1.0/element[0])
		# image_height_ratio.append(image_size[1]*1.0/element[1])

	# print ("LENGTHS:-  "),
	# print(length_list)
	# print ("HEIGHTS:-  "),
	# print(height_list)
	# print("CENTERS:-  "),
	# print(center_list)
	# print ("AREA:-  "),
	# print(area_list)
	# print("LENGTH RATIO :-  "),
	# print(image_length_ratio)
	# print ("HEIGHT RATIO :-  "),
	# print(image_height_ratio)

	lr2_list = [] # length * radius squared
	hr2_list = [] # height * radius squared
	lr2_ratio_list = []
	hr2_ratio_list = []
	distance_from_center_list = []
	for i in args_length_list:
		r = get_distance_from(center_list[i],image_center)
		distance_from_center_list.append(r)
		lr2 = length_list[i]*(r**2)
		hr2 = height_list[i]*(r**2)
		lr2_list.append(lr2)
		hr2_list.append(hr2)
		lr2_ratio_list.append(image_center[0]**3/(4.0*lr2))
		hr2_ratio_list.append(image_center[1]**3/(4.0*hr2))

	# print("distance_from_center_list:-  "),
	# print(distance_from_center_list)
	# print("lr2_list:-  "),
	# print(lr2_list)
	# print("hr2_list:-  "),
	# print(hr2_list)
	# print("lr2_ratio_list:-  "),
	# print(lr2_ratio_list)
	# print("hr2_ratio_list:-  "),
	# print(hr2_ratio_list)

	### FILTER BY LENGTH AND HEIGHT ###
	filter_by_length_threshold = 1.0
	filter_by_height_threshold = 1.0
	sure_decision_weight = 100
	for i in args_length_list:
		if(lr2_ratio_list[i]<filter_by_length_threshold or hr2_ratio_list[i]<filter_by_height_threshold):
			acceptance_list[i] = acceptance_list[i] - sure_decision_weight
	# print("FILTER BY LENGTH AND HEIGHT:-  "),
	# print(acceptance_list)

	decision = take_early_decision(acceptance_list)
	if(decision != False):
		return decision

	### FILTER BY CONSTANT AREA COMPARISION ###
	constant_area_comparison_threshold = 9
	constant_area_comparison_threshold2 = 20
	constant_area_comparison_weight = 10

	for i in args_length_list:
		if(area_list[i]<constant_area_comparison_threshold):
			acceptance_list[i] = acceptance_list[i] + -1 * sure_decision_weight
		elif(area_list[i]<constant_area_comparison_threshold2):
			acceptance_list[i] = acceptance_list[i] + -1 * constant_area_comparison_weight
	# print ("FILTER BY CONSTANT AREA COMPARISION:-  "),
	# print(acceptance_list)

	### PRIME FINDER ###
	prime_area_value = 1
	for i in args_length_list:
		if(prime_area_value<area_list[i]*(acceptance_list[i]+1)):
			prime_area_value = area_list[i]
			prime_index = i
	# print ("PRIME INDEX:- "),
	# print(prime_index)

	### CREATE ARRAYS ###
	prime_distance_list = []
	area_distance_ratio_list = []
	length_distance_ratio_list = []
	height_distance_ratio_list = []
	R2 = image_size[0]*image_size[1]/4.0
	for i in args_length_list:
		r = get_distance_from(center_list[i],center_list[prime_index])
		prime_distance_list.append(r)
		factor = R2/(r*distance_from_center_list[i])
		area_distance_ratio_list.append(area_list[i]*factor*1.0/prime_area_value)
		length_distance_ratio_list.append(length_list[i]*factor*1.0/image_args[prime_index][0])
		height_distance_ratio_list.append(height_list[i]*factor*1.0/image_args[prime_index][1])

	# print ("AREA DISTANCE RATIO WRT PRIME:-  "),
	# print_(area_distance_ratio_list)
	# print ("LENGTH DISTANCE RATIO WRT PRIME:-  "),
	# print_(length_distance_ratio_list)
	# print ("HEIGHT DISTANCE RATIO WRT PRIME:-  "),
	# print_(height_distance_ratio_list)
	# print("PRIME DISTANCE:-  "),
	# print_(prime_distance_list)

	for i in args_length_list:
		acceptance_list[i] = acceptance_list[i] + area_distance_ratio_list[i] +\
			length_distance_ratio_list[i] + height_distance_ratio_list[i]

	# print("finel_acceptance_list:-  "),
	# print(acceptance_list)

	output_list = []
	for i in args_length_list:
		if(acceptance_list[i]>2):
			output_list.append(i)
	# print("----->  output_list :-\t"),
	# print(output_list),
	# print("<-----")
	return output_list

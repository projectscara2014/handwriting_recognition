"""
	This script deals with functions to generate masks for cropping out "skin-tight-images".
	A "skin-tight-image" is an image which contains ONLY the character and ignores all other
		noise.
	Crop_mask are made for each object. Decision to KEEP or REJECT an object as a part of the
		character is decided in a 'decision_maker_v2.py'
"""

import cv2
import sys
import numpy as np
import decision_maker_v2
import copy

if(__name__ == "__main__"):
	import auto_script_2_cropped_to_skin_cropped
	# print("yolo")
	sys.exit(0)

def make_mask(im,num_array):
	try:
		num_array[0]
	except:
		num_array = [num_array]
	mask_im = []
	for row in im:
		mask_im.append([])
		for element in row:
			if(element in num_array):
				mask_im[-1].append(1)
			else:
				mask_im[-1].append(0)
	return mask_im

def get_mask_coordinates(mask_im):
	if(mask_im == None):
		return [1,-2,1,-2]
	max_h = 0
	min_h = len(mask_im)
	max_l = 0
	min_l = len(mask_im[0])
	for i in range(len(mask_im)):
		for j in range(len(mask_im[i])):
			if(mask_im[i][j] != 0):
				if(i<min_h):
					min_h = i
				if(i>max_h):
					max_h = i
				if(j>max_l):
					max_l = j
				if(j<min_l):
					min_l = j
	return [min_l,max_l,min_h,max_h]

def place_mask(im,mask_im):
	if(mask_im == None):
		return im
	if(len(mask_im) != len(im) or len(mask_im[0]) != len(im[0])):
		raise OSError
	for i in range(len(im)):
		for j in range(len(im[0])):
			im[i][j] = im[i][j] * mask_im[i][j]
	return im

def get_center(coordinates):
	[min_l,max_l,min_h,max_h] = coordinates
	mid_h = min_h + (max_h-min_h)/2.0
	mid_l = min_l + (max_l-min_l)/2.0
	return [mid_l,mid_h]

def main(ccl_image,ccl_image_properties):
	[dict_space,count_space] = ccl_image_properties
	dict_space = dict_space[1:]
	count_space = count_space[1:]
	ccl_image2 = copy.deepcopy(ccl_image)
	mask_space = []
	for element in dict_space:
		mask_space.append(make_mask(ccl_image2,element))

	coordinates_space = []
	dimensions_space = []
	for element in mask_space:
		coordinates = get_mask_coordinates(element)
		coordinates_space.append(coordinates)
		center = get_center(coordinates)
		dimensions_space.append([coordinates[1]-coordinates[0]+1\
			,coordinates[3]-coordinates[2]+1,center[0],center[1]])
	# print("coordinates = "),
	# print(coordinates_space)
	# print("dimensions  = "),
	# print(dimensions_space)
	l_r = len(ccl_image2)
	l_h = len(ccl_image2[0])
	image_dimensions = [l_r,l_h,l_r/2.0,l_h/2.0]
	dimensions_space.insert(0,image_dimensions)
	########### FOR TESTING ###########
	# try:
	# 	image_mask = mask_space[0]
	# 	# use_image_list = [1]
	# 	# use_image_list = [0,1,2]
	# 	# use_image_list = [1,2,3]
	# 	# use_element_list = [dict_space[x] for x in use_image_list]
	# 	# image_mask = make_mask(ccl_image2,use_element_list)
	# except:
	# 	print("INVALID INDEX")
	# 	image_mask = None
	############# END #################
	use_image_list = decision_maker_v2.main(dimensions_space)
	use_element_list = [dict_space[x] for x in use_image_list]
	image_mask = make_mask(ccl_image2,use_element_list)
	# print(use_element_list)
	ccl_image2 = place_mask(ccl_image2,image_mask)
	return [ccl_image2,get_mask_coordinates(image_mask)]
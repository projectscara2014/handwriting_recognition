"""
	This script uses the MNIST dataset and finds skincropped images and stores in a folder.
	This is not a part of auto script series since it has to be used just once.
"""

import os
import sys
import numpy as np
import cv2
import naming_convention
# import cv2
import lib_image_processing

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

def get_crop_values(list_):
	[min_l,max_l,min_h,max_h] = list_
	l = max_l-min_l+1
	h = max_h-min_h+1
	# print(l,h)
	if(max(l,h) != 20):
		l_pad = 20 - l
		if(l_pad%2==0):
			#even
			min_l -= l_pad/2
			max_l += l_pad/2
		else:
			#odd
			min_l -= l_pad/2 + 1
			max_l += l_pad/2
	
	l = max_l-min_l+1
	h = max_h-min_h+1

	if(l == h):
		pass
	elif(l>h):
		h_pad = 20-h
		if(h_pad%2==0):
			#even
			min_h -= h_pad/2
			max_h += h_pad/2
		else:
			#odd
			min_h -= h_pad/2
			max_h += h_pad/2 + 1
		# print([min_l,max_l,min_h,max_h])
	elif(l<h):
		l_pad = 20-l
		if(l_pad%2==0):
			#even
			min_l -= l_pad/2
			max_l += l_pad/2
		else:
			#odd
			min_l -= l_pad/2
			max_l += l_pad/2 + 1
		# print([min_l,max_l,min_h,max_h])
	return_val = [min_l,max_l,min_h,max_h]
	# checking constraints
	if(max_h-min_h != max_l-min_l):
		print(l,h)
		raise ValueError
	elif(min_l<0 or min_h<0 or max_l>27 or max_h>27):
		print([min_l,max_l,min_h,max_h])
		raise ValueError
	return return_val

def scan_and_crop(im):
	bnw_im = []
	for row in im:
		bnw_im.append([])
		for pixel in row:
			s = int(pixel[0]) + int(pixel[1]) + int(pixel[2])
			if(s<4):
				bnw_im[-1].append(0)
			else:
				bnw_im[-1].append(255)
	[min_l,max_l,min_h,max_h] = get_crop_values(get_mask_coordinates(bnw_im))
	im2 = np.array(bnw_im)[min_h:max_h+1,min_l:max_l+1]
	return im2


WORKING_DIRECTORY = os.getcwd()
INPUT_DIRECTORY = WORKING_DIRECTORY + "\MNIST_dataset\\input\\"
OUTPUT_DIRECTORY = WORKING_DIRECTORY + "\MNIST_dataset\output\\"
DONE_DIRECTORY = WORKING_DIRECTORY + "\MNIST_dataset\done\\"
ERROR_DIRECTORY = WORKING_DIRECTORY + "\MNIST_dataset\error\\"

naming_convention.main2(INPUT_DIRECTORY)

all_files = os.listdir(INPUT_DIRECTORY)

for file in all_files:
	if("MNIST" in file):
		split_name = file.split("_")
		label = split_name[1]
		count = int(split_name[2].split(".")[0])
		FILE_PATH = INPUT_DIRECTORY + file
		OUTPUT_PATH = OUTPUT_DIRECTORY + file
		DONE_PATH = DONE_DIRECTORY + file

		try:
			im = cv2.imread(FILE_PATH)
			cropped_im = scan_and_crop(im)
			m = max(len(cropped_im),len(cropped_im[0]))
			cv2.imwrite(OUTPUT_PATH,cropped_im)
		except:
			DONE_PATH = ERROR_DIRECTORY + file
			# break	
		os.rename(FILE_PATH,DONE_PATH)
"""
	This script is used to compile the database as per the instruction given.
	Options provided are:
		> original / tilted
		> selected letters
		> rejected letters
	Saves single dataset file in "final_dataset_folder".
"""

import os
import sys
import numpy as np

dictionary = {
	62:"<",	63:">",	64:"{",	65:"}",	66:"(",	67:")",	68:"[",\
		69:"]",	70:"$",	71:"#",	72:"@",	73:"&",	74:"%",	75:"=",\
			76:"~",	77:";",	78:"?",	79:"pi"}

def get_letter(name):
	global dictionary
	a = name.split("_")
	a = 7*int(a[1]) + int(a[2]) + 10
	if(a>=10 and a<=35):
		b = chr(a + 87) 
	elif(a>=36 and a<=61):
		b = chr(a + 29)
	else:
		b = dictionary[a]
	return [a,b]

def convert(im):
	# get_vals(im)
	im2 = []
	for row in im:
		for pixel in row:
			im2.append(pixel/255)
	# get_vals(im2)
	# l = j
	return im2

# mode = "original"
mode = "tilted"

OUTPUT_FILE_NAME = "database_shoes"

selected_letters = ['h','o','e','s']
# selected_letters = ['o','n','e','l','a','s','t','i','m','#']
# selected_letters = "all"
# rejected_letters = []

WORKING_DIRECTORY = os.getcwd()

ERROR_DIRECTORY = WORKING_DIRECTORY + "\script4_folders\error_folder"
DONE_DIRECTORY = WORKING_DIRECTORY + "\script4_folders\done_folder"
TILTED_DIRECTORY = WORKING_DIRECTORY + "\\tilted_images_folder"
OUTPUT_DIRECTORY = WORKING_DIRECTORY + "\\final_dataset_folder"

all_files = os.listdir(TILTED_DIRECTORY)

final_list = []
OUTPUT_PATH = OUTPUT_DIRECTORY + "\\" + OUTPUT_FILE_NAME
if("." not in OUTPUT_PATH):
	OUTPUT_PATH = OUTPUT_PATH + ".npy"

for file in all_files:
	split_name = file.split(".")
	if(split_name[1] == "npy"):
		if(mode in split_name[0]):
			NPY_FILE_PATH = TILTED_DIRECTORY + "\\" + file
			# print(len(char_set))
			[index,letter] = get_letter(split_name[0])
			if(selected_letters == "all"):
				if(letter in rejected_letters):
					continue
			elif(letter not in selected_letters):
				continue
			char_set = np.load(NPY_FILE_PATH).tolist()
			for image in char_set:
				image = convert(image)
				final_list.append([image,index])
			print(letter)
			# print(index)
print("\""+OUTPUT_PATH+"\"")
np.save(OUTPUT_PATH,np.array(final_list))
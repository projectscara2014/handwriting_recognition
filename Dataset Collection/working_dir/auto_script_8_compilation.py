"""
	This script compiles the selected characters from the pre-compiled '.npy' file and
		gives a single '.npy' file as an output.
"""

import os
import sys
import numpy as np

dictionary = {
	62:"<",	63:">",	64:"{",	65:"}",	66:"(",	67:")",	68:"[",\
		69:"]",	70:"$",	71:"#",	72:"@",	73:"&",	74:"%",	75:"=",\
			76:"~",	77:";",	78:"?",	79:"pi"}

def get_letter(a):
	if(a<10):
		b = str(a)
	elif(a>=10 and a<=35):
		b = chr(a + 87) 
	elif(a>=36 and a<=61):
		b = chr(a + 29)
	else:
		b = dictionary[a]
	return b

# mode = "original"
mode = "tilted"

# OUTPUT_FILE_NAME = "database_123"
# selected_characters = ['1','2','3']

# OUTPUT_FILE_NAME = "database_tilted_abc123"
# selected_characters = ['a','b','c','1','2','3']

# OUTPUT_FILE_NAME = "database_numbers"
# selected_characters = ['0','1','2','3','4','5','6','7','8','9']

# OUTPUT_FILE_NAME = "database_357"
# selected_characters = ['3','5','7']

# OUTPUT_FILE_NAME = "database_xyz357"
# selected_characters = ['x','y','z','3','5','7']

# OUTPUT_FILE_NAME = "database_wxy357"
# selected_characters = ['x','y','w','3','5','7']

OUTPUT_FILE_NAME = "database_abcde_tilted"
selected_characters = ['a','b','c','d','e']

# selected_characters = ['3','s','h','o','e']
# selected_characters = "all"

rejected_characters = []

WORKING_DIRECTORY = os.getcwd()

INPUT_DIRECTORY = WORKING_DIRECTORY + "\\processed_npy_folder\\"
OUTPUT_DIRECTORY = WORKING_DIRECTORY + "\\final_dataset_folder\\"

all_files = os.listdir(INPUT_DIRECTORY)

n = 0
# n = 10
# n = 80

all_files = all_files[n:]

final_list = []
for file in all_files:
	# print file
	file_name = file.split(".")[0]
	# print(file_name)
	index = int(file_name.split("_")[1])
	# print(index)
	character = get_letter(index)
	# print(character)
	if mode not in file_name and "MNIST" not in file_name:
		continue
	if selected_characters == "all":
		if character in rejected_characters:
			continue
	elif character not in selected_characters:
		continue
	# print(character)
	print file_name
	FILE_PATH = INPUT_DIRECTORY + file_name + ".npy"
	im_list = np.load(FILE_PATH).tolist()
	final_list.extend(im_list)
OUTPUT_PATH = OUTPUT_DIRECTORY + OUTPUT_FILE_NAME + ".npy"
# print(OUTPUT_PATH)
print(len(final_list))
# print(len(final_list[0]))
# print(len(final_list[0][0]))
np.save(OUTPUT_PATH,final_list)
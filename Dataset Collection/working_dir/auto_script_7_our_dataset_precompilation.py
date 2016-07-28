"""
	This script precompiles our dataset in a '.npy' format.
	Basically, this deals with the index for each character and output format 
		required for further processing.
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

WORKING_DIRECTORY = os.getcwd()

TILTED_DIRECTORY = WORKING_DIRECTORY + "\\tilted_images_folder\\"
OUTPUT_DIRECTORY = WORKING_DIRECTORY + "\\processed_npy_folder\\"

all_files = os.listdir(TILTED_DIRECTORY)

for file in all_files:
	print(file)
	prefix = file.split("_")[0]
	[index,letter] = get_letter(file.split(".")[0])
	print(prefix)
	print(index)
	print(type(index))
	main_list = np.load(TILTED_DIRECTORY+file)

	final_list = []
	for im in main_list:
		im2 = np.reshape(im,(400))
		im3 = [i/255 for i in im2]
		final_list.append([im3,index])
	
	OUTPUT_PATH = OUTPUT_DIRECTORY + prefix + "_" + str(index) + ".npy"
	np.save(OUTPUT_PATH,np.array(final_list))
	break
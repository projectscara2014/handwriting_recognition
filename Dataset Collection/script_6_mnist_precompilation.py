"""
	This script precompiles the MNIST dataset in a '.npy' format.
"""

import os
import sys
import numpy as np
import cv2

WORKING_DIRECTORY = os.getcwd()
INPUT_DIRECTORY = WORKING_DIRECTORY + "\MNIST_dataset\\output\\"
OUTPUT_DIRECTORY = WORKING_DIRECTORY + "\MNIST_dataset\\npy_folder\\"
DONE_DIRECTORY = WORKING_DIRECTORY + "\MNIST_dataset\done2\\"
ERROR_DIRECTORY = WORKING_DIRECTORY + "\MNIST_dataset\error\\"

all_files = os.listdir(INPUT_DIRECTORY)

blah = '9'
final_list = []
for file in all_files:
	# print(file)
	split_name = file.split(".")
	file_name = split_name[0]
	# print(file_name)
	split_name2 = file_name.split("_")
	character = split_name2[1]
	index = split_name2[2]
	# print(character)
	if(character != blah):
		continue
	# print(index)
	im = cv2.imread(INPUT_DIRECTORY + file,0)
	im2 = np.reshape(im,(400))
	im3 = [i/255 for i in im2]
	final_list.append([im3,int(character)])

print(len(final_list))
OUTPUT_PATH = OUTPUT_DIRECTORY + "MNIST_" + blah +".npy"
print(OUTPUT_PATH)
np.save(OUTPUT_PATH,np.array(final_list))
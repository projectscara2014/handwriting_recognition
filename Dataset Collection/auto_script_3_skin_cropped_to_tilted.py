"""
	The purpose of this script is to multiply the existing dataset by taking each image from the
		dataset and tilting them by a few degreees in each direction to account for tilted versions
		of the same handwritting.
	Images from the "skin_cropped_images_folder" are taken, rotated, cropped, packed and added to 
		the "tilted_images_folder" in the form of '.npy' files.
"""

import os
import sys
import script3_main
import numpy as np

WORKING_DIRECTORY = os.getcwd()

SKIN_CROPPED_IMAGE_DIRECTORY = WORKING_DIRECTORY + "\skin_cropped_images_folder"
ERROR_DIRECTORY = WORKING_DIRECTORY + "\script3_folders\error_folder"
DONE_DIRECTORY = WORKING_DIRECTORY + "\script3_folders\done_folder"
TILTED_DIRECTORY = WORKING_DIRECTORY + "\\tilted_images_folder"

# for i in range(10):
# 	for j in range(7):
# 		os.makedirs(SKIN_CROPPED_IMAGE_DIRECTORY + "\\" +str(i)+ "_" +str(j))

all_folders = os.listdir(SKIN_CROPPED_IMAGE_DIRECTORY)

# all_folders = [all_folders[0]]
# all_folders = all_folders[:2]

for folder in all_folders:
	print(folder)
	NPY_TILTED_FILE_PATH = TILTED_DIRECTORY + "\\tilted_" + folder + ".npy"
	NPY_ORIGINAL_FILE_PATH = TILTED_DIRECTORY + "\\original_" + folder + ".npy"
	# print(NPY_TILTED_FILE_PATH)

	try:
		original_image_list = np.load(NPY_ORIGINAL_FILE_PATH).tolist()
	except:
		original_image_list = []
	try:
		image_list = np.load(NPY_TILTED_FILE_PATH).tolist()
	except:
		image_list = []
	print("len_image_list:- "),
	print(len(image_list))
	print("len_original_list:- "),
	print(len(original_image_list))
	all_files = os.listdir(SKIN_CROPPED_IMAGE_DIRECTORY + "\\" + folder)
	for file in all_files:
		IMAGE_PATH = SKIN_CROPPED_IMAGE_DIRECTORY + "\\" + folder + "\\" + file
		DESTINATION_PATH = TILTED_DIRECTORY
		# print(file)
		# [og_im,im2] = script3_main.main(IMAGE_PATH,DESTINATION_PATH + "\\" +file)
		# image_list.extend(im2)
		# image_list.append(og_im)
		# original_image_list.append(og_im)
		if(file == "delete"):
			FILE_DESTINATION_PATH = ERROR_DIRECTORY + "\\" + file + "_" + folder
		else:
			try:
				[og_im,im2] = script3_main.main(IMAGE_PATH,DESTINATION_PATH + "\\" +file)
				image_list.extend(im2)
				image_list.append(og_im)
				original_image_list.append(og_im)
			except:
				FILE_DESTINATION_PATH = ERROR_DIRECTORY + "\\" + file
			else:
				FILE_DESTINATION_PATH = DONE_DIRECTORY + "\\" + file
		os.rename(IMAGE_PATH,FILE_DESTINATION_PATH)
		# sys.exit(0
		# break
	print("len_image_list:- "),
	print(len(image_list))
	print("len_original_list:- "),
	print(len(original_image_list))
	np.save(NPY_TILTED_FILE_PATH,image_list)
	np.save(NPY_ORIGINAL_FILE_PATH,original_image_list)
	# break
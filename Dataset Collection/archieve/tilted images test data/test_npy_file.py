import os
import cv2
import numpy as np

WORKING_DIRECTORY = os.getcwd()

all_files = os.listdir(WORKING_DIRECTORY)


def images_to_npy():
	pass

def all_npy_to_images(mode = "png"):
	total_count = 0
	for file in all_files:
		split_name = file.split(".")
		if split_name[1] == "npy":
			im_list = np.load(file)
			count = len(im_list)
			print(count)
			total_count = total_count + count
			if(mode == "lenght_only"):
				continue
			for im in im_list:
				DESTINATION_PATH = WORKING_DIRECTORY + "\\" + split_name[0] + "_npy_" + str(count) + ".png"
				count = count + 1
				cv2.imwrite(DESTINATION_PATH,im)
	print(total_count)

def all_images_to_npy():
	pass

# all_npy_to_images(mode= "lenght_only")
all_npy_to_images()
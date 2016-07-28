import os
import sys
import numpy as np 
import cv2
import get_orientation

def transpose(image):
    temp = []
    for i in range(len(image[0])):
        temp.append([])
        for j in range(len(image)):
            temp[-1].append(image[j][i])
    return np.array(temp)

def sweep_and_detect(im,start_val = 0,fwd = True,inverse = False):
	global background
	global foreground
	l_r = len(im)
	l_c = len(im[0])
	if(fwd): 	parse_list = range(start_val,l_r) 
	else:		parse_list = range(l_r-1,0,-1)
	for i in parse_list:
		if(inverse):
			if(not foreground in im[i]):
				return i
		else:
			if(foreground in im[i]):
				return i
	if(fwd):
		return l_r-1
	else:
		return 0

def scan_and_crop(im):
	global background
	global foreground

	x1 = sweep_and_detect(im)
	x2 = sweep_and_detect(im,start_val = x1,inverse = True)
	im_slice = im[x1:x2]
	im_slice = transpose(im_slice)
	y1 = sweep_and_detect(im_slice)
	y2 = sweep_and_detect(im_slice,start_val = y1,inverse = True)
	cropped_image = im[y1:y2,x1:x2]

	return [cropped_image,remaining]

def main(IMAGE_PATH,TEMP_PATH):
	im = cv2.imread(IMAGE_PATH)
	bnw_im = get_orientation.rgb_to_bnw(im)

	im = bnw_im
	[cropped_image,remaining] = scan_and_crop(im)

	# print(sweep_and_detect(im,fwd = False))
	cv2.imwrite(TEMP_PATH,np.array(cropped_image))

background = 255
foreground = 1
WORKING_DIRECTORY = os.getcwd()

CROPPED_IMAGE_DIRECTORY = WORKING_DIRECTORY + "\other\cropped_images_folder_old"
# CROPPED_IMAGE_DIRECTORY = WORKING_DIRECTORY + "\cropped_images_folder"
SKIN_CROPPED_IMAGE_DIRECTORY = WORKING_DIRECTORY + "\skin_cropped_images_folder"

# for i in range(10):
# 	for j in range(7):
# 		os.makedirs(SKIN_CROPPED_IMAGE_DIRECTORY + "\\" +str(i)+ "_" +str(j))

all_folders = os.listdir(CROPPED_IMAGE_DIRECTORY)

for folder in all_folders:
	all_files = os.listdir(CROPPED_IMAGE_DIRECTORY + "\\" + folder)
	for file in all_files:
		IMAGE_PATH = CROPPED_IMAGE_DIRECTORY + "\\" + folder + "\\" + file
		DESTINATION_PATH = SKIN_CROPPED_IMAGE_DIRECTORY + "\\" + folder + "\\" + file
		TEMP_PATH = WORKING_DIRECTORY + "\other\\" + file
		ret_im = main(IMAGE_PATH,TEMP_PATH)
		# cv2.imwrite(TEMP_PATH,ret_im)
		sys.exit(0)
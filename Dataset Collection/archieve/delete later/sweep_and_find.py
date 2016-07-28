import os
import sys
import cv2
import copy
import numpy as np
import get_orientation

def print_list_dimensions(a):
	try:
		l = len(a)
	except:
		print 1
	else:
		print l
		print_list_dimensions(a[0])

def transpose(image):
    temp = []
    for i in range(len(image[0])):
        temp.append([])
        for j in range(len(image)):
            temp[-1].append(image[j][i])
    return np.array(temp)

def check_row_for_obstruction(im,row,mode=1):
    im_slice = im[row]
    k = im_slice[0]
    for i in range(1,len(im_slice)):
        if(k != im_slice[i]):
            return (mode==1)
    return (mode!=1)

def sweep(image,image_,mode,x1=0):
    if(mode==1):   #Right to left sweep
        for i in range(len(image_)):
            if(check_row_for_obstruction(image_,i)):
                break
        else:
            return True   ## Returns true to show scanning is complete without any obstacles
        return i
    if(mode==2):   #Up to down sweep
        for i in range(len(image)):
            if(check_row_for_obstruction(image,i)):
                break
        else:
            return True
        return i
    if(mode==3):   #Down to up sweep
        for i in range(len(image)):
            if(check_row_for_obstruction(image,len(image)-1-i)):
                break
        else:
        	pass
            # return True
        return len(image)-1-i
    if(mode==4):   #Left to right sweep
        for i in range(x1,len(image_)):
            if(check_row_for_obstruction(image_,i,2)):
                break
        else:
        	pass
            # return True
        return i-1

def crop_out(image,obj_dim):
    border = 2
    obj_dim = [obj_dim[0]-border,obj_dim[1]+border,obj_dim[2]-border,obj_dim[3]+border]
	#     print(obj_dim)
    obj_dim = [max(0,x) for x in obj_dim]
    obj_dim[1] = min(obj_dim[1],len(image[0]))
    obj_dim[3] = min(obj_dim[3],len(image))
	#     print(obj_dim)
    letter_image = image[obj_dim[2]:obj_dim[3]]
    letter_image = np.array([row[obj_dim[0]:obj_dim[1]] for row in letter_image])
	#     letter_image = scale_and_border(letter_image)
    edited_image = copy.deepcopy(image)
    for i in range(obj_dim[0],obj_dim[1]):
        for j in range(obj_dim[2],obj_dim[3]):
            edited_image[j][i] = 0
    edited_image = np.array(edited_image)
	#     display(edited_image)
    return ([letter_image,edited_image])

# t = crop_out(image,[98,242,141,347])

def inverse(image):
	old_black = 1
	old_white = 255
	new_black = 0
	new_white = 255
	for i in range(len(image)):
		for j in range(len(image[i])):
			if(image[i][j] == old_white):
				image[i][j] = new_black
			else:
				image[i][j] = new_white
	return image

def scan_and_crop(image):
    image_ = transpose(image)
    x1 = sweep(image,image_,1)
    x2 = sweep(image,image_,4,x1)
    y1 = sweep(image,image_,2)
    y2 = sweep(image,image_,3)
    print("cropped values are:")
    print(x1,x2,y1,y2)
    object_dimensions = [x1,x2,y1,y2]
    return crop_out(image,object_dimensions)

def take_decision(img_array):
	area_array = []
	for img in img_array:
		area_array.append(len(img) * len(img[0]))
		print(len(img))
		print(len(img[0]))
	print(area_array)
	return img_array[0]

def check_for_object(im):
    im_ = transpose(im)
    if(sweep(im,im_,1) == True): ##Means no object found
        return False
    else:
        return True

def image_array_creator(image):
    image_array=[]
    remaining = copy.deepcopy(image)
    while(check_for_object(remaining)):
	#     for i in range(2):
        [cropped,remaining] = scan_and_crop(remaining)
        image_array.append(cropped)
    return(image_array)

def main(IMAGE_PATH):
	im = cv2.imread(IMAGE_PATH)
	bnw_im = get_orientation.rgb_to_bnw(im)
	wnb_im = inverse(bnw_im)
	image_array = image_array_creator(bnw_im)
	new_image_array = []
	for img in image_array:
		img_array = image_array_creator(img)
		for obj in img_array:
			new_image_array.append(obj)    
	ret_img = take_decision(new_image_array)
	return np.array(ret_img)

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
		print(file)
		ret_im = main(IMAGE_PATH)
		cv2.imwrite(TEMP_PATH,ret_im)
		sys.exit(0)
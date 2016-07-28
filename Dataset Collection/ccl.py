import sys
if(__name__ == "__main__"):
	import auto_script_2_cropped_to_skin_cropped
	# print("yolo")
	sys.exit(0)

import cv2
import numpy as np
import copy
import ccl_to_skin_cropped
import resize

# Global_Variables
COUNT = 1
var_array = []

def time_this_function(function) : 
    try : 
        time
    except : 
        import time
    
    def wrapper_function(*args,**kwargs) : 
        start_time = time.time()
        return_value = function(*args,**kwargs)
        elapsed_time = (time.time() - start_time)*1000
        print(function.__name__ + ' -- elapsed_time -- ' + str(elapsed_time) + ' ms\n')
        return return_value
    return wrapper_function

class Variable:
	def __init__(self,num):
		self.value = num
		# self.name = chr(num+48)
		self.merge_val_list = [num]
	def merge(self,var_name):
		if(var_name.value not in self.merge_val_list):
			self.merge_val_list.append(var_name.value)

def merge_labels(var1,var2):
	var1.merge(var2)
	# var2.merge(var1)

def fuse_recurring(a):
	# print(a)
	## finds maximum
	max_ = 1
	for element in a:
		for num in element:
			max_ = max(max_,num)

	for i in range(1,max_+1):
		remember_list = []
		for element in a:
			if(i in element):
				remember_list.append(element)
		extended_list = []
		# print(remember_list)
		for element in remember_list:
			extended_list.extend(element)
		# print(extended_list)
		for element in remember_list:
			a.remove(element)
		a.append(remove_repeats(extended_list))
		# print(a)
		# break
	return a

def remove_repeats(a):
	ret_array = []
	for element in a:
		if(element not in ret_array):
			ret_array.append(element)
	return ret_array

def merge_variable_values():
	global var_array
	# show_merge_list()
	# print("---------")
	merge_val_list_list = []
	for instance in var_array:
		merge_val_list_list.append(instance.merge_val_list)
	reference_list = fuse_recurring(merge_val_list_list)			
	# print(reference_list)
	for element in reference_list:
		for num in element:
			var_array[num-1].value = min(element)

def show_merge_list():
	global var_array
	for instance in var_array:
		print(instance.name,instance.value ,instance.merge_val_list)

def show_var_array():
	global var_array
	l = []
	for instance in var_array:
		l.append(instance.value)
	print(l)

def show_var_names():
	global var_array
	l = []
	for instance in var_array:
		l.append(instance.name)
	print(l)

def var(i):
	global var_array
	return var_array[i]

def val(i):
	global var_array
	return var_array[i].value

def make_new_var():
	global COUNT 
	global var_array
	obj = Variable(COUNT)
	var_array.append(obj)
	COUNT = COUNT + 1

def rgb_to_bnw(image,threshold = 200,numpy_array = False) : 
    return_image = []
    for row in image : 
        return_image.append([])
        for pixel in row :
            [r,g,b] = pixel
            magnitude= (int(r)+int(g)+int(b))/3
            if(magnitude < threshold) : 
                return_image[-1].append(255)
            else:
                return_image[-1].append(0)
    if(numpy_array):
        return np.array(return_image)
    else:
        return return_image

def rgb_to_greyscale(image,numpy_array = True) : 
    return_image = []
    for row in image : 
        return_image.append([])
        for pixel in row :
            try:
                [r,g,b,s] = pixel
            except ValueError:
                [r,g,b] = pixel
            magnitude= (int(r)+int(g)+int(b))/3
            return_image[-1].append(magnitude)
    if(numpy_array):
        return np.array(return_image)
    else:
        return return_image

def ccl(image):
	background = 0
	foreground = 1
	l_r_ = len(image)
	l_c_ = len(image[0])
	im2 = np.zeros((l_r_ + 2,l_c_ + 2))
	im2 [1:-1,1:-1] = image
	l_r = len(im2)
	l_c = len(im2[0])
	label = [] 
	for i in range(l_r):
		label.append([])
		for j in range(l_c):
			label[-1].append(background)
	for i in range(1,l_r-1):
		for j in range(1,l_c-1):
			# if pixel is not background
			label_value = background
			if (im2[i][j] != background):
				# check neighbours and their labels
				if (im2[i-1][j] != background or im2[i-1][j-1] != background or im2[i-1][j+1] != background or im2 [i][j-1] != background ):
					label_space = [label[i-1][j-1],label[i-1][j],label[i-1][j+1],label[i][j-1]]
					var_label_space = []
					for obj in label_space:
						if(type(obj).__name__ != "int"):
							if(obj not in var_label_space):
								var_label_space.append(obj)
					if(len(var_label_space)==1):
						label_value = var_label_space[0]
					else:
						for m in range(len(var_label_space)-1):
							merge_labels(var_label_space[m],var_label_space[m+1])
						label_value = var_label_space[0]
				else:
					make_new_var()
					label_value = var(-1)
			# if pixel is background
			else:
				label_value = background

			label[i][j] = label_value
	# for i in range(len(image)):
	# 	print im2[i]
	# print("---------------------------------")
	merge_variable_values()
	ccl_image = []
	for i in range(len(label)):
		ccl_image.append([])
		for j in range(len(label[i])):
			try:
				ccl_image[-1].append(label[i][j].value)
			except:
				ccl_image[-1].append(label[i][j])
	# print("---------------------------------")	
	# for i in range(len(label)):
	# 	for j in range(len(label[i])):
	# 		try:
	# 			print(label[i][j].name),
	# 		except:
	# 			print(label[i][j]),
	# 		print(" "),
	# 	print("\n")

	# for i in range(len(ccl_image)):
	# 	print(ccl_image[i])
	# print("---------------------------------")
	return ccl_image

def ccl_image_properties(image):
	dict_space = []
	count_space = []
	for row in image:
		for pixel in row:
			if(pixel not in dict_space):
				dict_space.append(pixel)
				count_space.append(1)
			else:
				count_space[dict_space.index(pixel)] = count_space[dict_space.index(pixel)] + 1
	# Make 0 as first value
	# print(dict_space)
	# print(count_space)
	return [dict_space,count_space]

def show_color(image,dict_space):
	factor = 255/(((len(dict_space)-1)/8)+1)
	color_space = []
	count = 0
	current_factor = factor
	for i in range(len(dict_space)):
		p = [(count/4)%2,(count/2)%2,count%2]
		for j in range(3):
			p[j] = current_factor*p[j]
		color_space.append(p)
		# print(p)
		count = count + 1
		if(count%8 == 0):
			count = 1
			current_factor = current_factor + factor
	# print(color_space)
	for i in range(len(image)):
		for j in range(len(image[i])):
			image[i][j] = color_space[dict_space.index(image[i][j])]
	return image

def show_greyscale(image,dict_space):
	factor = 255/(len(dict_space)-1)
	color_space = [i*factor for i in range(len(dict_space))]
	# print(color_space)
	for i in range(len(image)):
		for j in range(len(image[i])):
			image[i][j] = color_space[dict_space.index(image[i][j])]
	return image

# @time_this_function
def main(IMAGE_PATH,TEMP_PATH,output_type = "Number_array"):
	global COUNT
	global var_array
	var_array = []
	COUNT = 1
	im = cv2.imread(IMAGE_PATH)
	bnw_im = rgb_to_bnw(im,205)
	ccl_image = ccl(bnw_im)
	# for i in range(len(ccl_image)):
	# 	print(ccl_image[i])
	# print("---------------")
	[dict_space,count_space] = ccl_image_properties(ccl_image)
	[ccl_image_new,[xl,xr,yu,yd]] = ccl_to_skin_cropped.main(ccl_image,[dict_space,count_space])
	if(output_type == "color"):
		ccl_image_new = show_color(ccl_image_new,dict_space)
		ccl_image = show_color(ccl_image,dict_space)
	elif(output_type == "grey"):
		ccl_image = show_greyscale(ccl_image,dict_space)
	else:
		pass
	
	# print("---------------")

	##### CCL COMPARISION WITH IMAGE (2 side by side) #####
	# ccl_image_new = np.array(ccl_image_new)
	# # ccl_image_new = ccl_image_new[yu:yd+1,xl:xr+1]
	# ccl_image_new = ccl_image_new[1:-1,1:-1]
	# l_r = len(im)
	# l_c = len(im[0])
	# full_image = np.zeros((l_r,l_c*2,3))
	# full_image [:,l_c:] = ccl_image_new
	# # grey_im = rgb_to_greyscale(im)
	# full_image [:,0:l_c] = im
	# cv2.imwrite(TEMP_PATH,full_image)
	######################## END ##########################
	
	############# 3 side by side ###############
	# ccl_image_new = np.array(ccl_image_new)
	# # ccl_image_new = ccl_image_new[yu:yd+1,xl:xr+1]
	# ccl_image_new = ccl_image_new[1:-1,1:-1]
	# ccl_image = np.array(ccl_image)
	# ccl_image = ccl_image[1:-1,1:-1]
	# l_r = len(im)
	# l_c = len(im[0])
	# full_image = np.zeros((l_r,l_c*3,3))
	# full_image [:,2*l_c:] = ccl_image_new
	# # grey_im = rgb_to_greyscale(im)
	# full_image [:,l_c:2*l_c] = im
	# full_image [:,:l_c] = ccl_image
	# cv2.imwrite(TEMP_PATH,full_image)



	######## CROPPED IMAGES ONLY #########
	ccl_image_new = np.array(ccl_image_new)
	ccl_image_new = ccl_image_new[yu:yd+1,xl:xr+1]
	# cv2.imwrite(TEMP_PATH,ccl_image_new)
	################ END #################

	#### RESIZING ####
	cropped_im = im[yu:yd+1,xl:xr+1]
	bnw_cropped_im = np.array(rgb_to_bnw(cropped_im,200))
	resized_image = resize.main(bnw_cropped_im)
	# TEMP_PATH_2 = TEMP_PATH.split(".")[0] + "_r.png"

	# element_list = []
	# count_list = []
	# for row in resized_image:
	# 	for element in row:
	# 		if(element not in element_list):
	# 			element_list.append(element)
	# 			count_list.append(1)
	# 		else:
	# 			index = element_list.index(element)
	# 			count_list[index] = count_list[index] + 1

	# print(element_list)
	# print(count_list)

	threshold_resize = 50
	for i in range(len(resized_image)):
		for j in range(len(resized_image[i])):
			if(resized_image[i][j]>threshold_resize):
				resized_image[i][j] = 255
			else:
				resized_image[i][j] = 0

	cv2.imwrite(TEMP_PATH,resized_image)

# show_var_array()
# show_var_names()
# show_merge_list()


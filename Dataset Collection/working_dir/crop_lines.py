"""
	This script includes all functions related to:
		Template matching with markers
		Orientation recognition and fixing
		Rotation to correct orientation
		Crop lines generation
		Cropping individual images
		Saving related files
"""

def change_pixel_(*args):
	try:
		change_pixel(*args)
	except:
		pass

def change_pixel(im,x,y):
	sum_ = int(im[y][x][0]) + int(im[y][x][1]) + int(im[y][x][2])
	if(sum_ > 380):
		im[y][x][0] = 0
		im[y][x][1] = 0
		im[y][x][2] = 255
	else:
		im[y][x][0] = 255
		im[y][x][1] = 255
		im[y][x][2] = 0		

import cv2
import os 
import shutil
import get_orientation
import copy

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

@time_this_function
def main(IMAGE_PATH,CROP_LINES_DESTINATION_PATH,CROPPING_INFO):
	im = cv2.imread(IMAGE_PATH)

	# [marker_values,im] = get_marker_positions(im,[[78,65], [12,25], [139,91], [76,62]])
	[marker_values,im] = get_marker_positions(im,show_region=False)
	print(marker_values)
	im = get_rotated_image(im,marker_values)

	## [marker_values,im] = get_marker_positions(im,[[141,67], [10,68], [140,56], [12,60]])
	[marker_values,im] = get_marker_positions(im,show_region=False)

	## im = get_crop_lines(im,marker_values)
	im = get_crop_lines(im,marker_values,CROPPING_INFO)

	# im = get_orientation.rgb_to_bnw(im,200,numpy_array = True)	
	cv2.imwrite(CROP_LINES_DESTINATION_PATH,im)

	print("--------------  DONE  ---------------")

def get_marker_positions(im,offset_values = None,show_region = True):
	##------ GETTING POINTS FOR SLOPE ---------
	kernel = cv2.imread("plus_kernel.png")
	# kernel = cv2.imread("kernel_try.png")

	im_dimensions = [len(im),len(im[0])] # [ht,wd]

	REGION_WIDTH  = 265
	REGION_HEIGHT = 195

	r_u = REGION_HEIGHT
	r_d = im_dimensions[0] - REGION_HEIGHT
	r_l = REGION_WIDTH
	r_r = im_dimensions[1] - REGION_WIDTH

	if(show_region):
		######## DRAW LINES #########
		# TOP-LEFT
		for i in range(r_l+1):
			change_pixel(im,i,r_u)

		for i in range(r_u+1):
			change_pixel(im,r_l,i)

		# TOP-RIGHT
		for i in range(r_r, im_dimensions[1]):
			change_pixel(im,i,r_u)

		for i in range(r_u+1):
			change_pixel(im,r_r,i)

		# BOTTOM-LEFT
		for i in range(r_l+1):
			change_pixel(im,i,r_d)

		for i in range(r_d,im_dimensions[0]):
			change_pixel(im,r_l,i)

		# BOTTOM-RIGHT
		for i in range(r_r, im_dimensions[1]):
			change_pixel(im,i,r_d)

		for i in range(r_d,im_dimensions[0]):
			change_pixel(im,r_r,i)
	#-------------------------------------------

	if(offset_values == None):
		### -------- REGION OF INTERESTS --------

			########## GET REGIONS ########
		# TOP-LEFT
		region_1 = im[0:r_u,0:r_l]
		# cv2.imwrite("region_of_interest1.png",region_1)

		# TOP-RIGHT
		region_2 = im[ 0:r_u, r_r+1 : im_dimensions[1] ]
		# cv2.imwrite("region_of_interest2.png",region_2)

		# BOTTOM-LEFT
		region_3 = im[r_d:im_dimensions[0], 0 : r_l ]
		# cv2.imwrite("region_of_interest3.png",region_3)

		# BOTTOM-RIGHT
		region_4 = im[r_d:im_dimensions[0], r_r+1: im_dimensions[1] ]
		# cv2.imwrite("region_of_interest4.png",region_4)

		offset_1 = get_orientation.main(region_1,kernel)
		offset_2 = get_orientation.main(region_2,kernel)
		offset_3 = get_orientation.main(region_3,kernel)
		offset_4 = get_orientation.main(region_4,kernel)
		#-------------------------------------------
	else:
		[offset_1,offset_2,offset_3,offset_4] = offset_values
		# print(offset_1)
		# print(offset_2)
		# print(offset_3)
		# print(offset_4)

	offset_2[0] = offset_2[0] + r_r
	offset_3[1] = offset_3[1] + r_d
	offset_4[0] = offset_4[0] + r_r
	offset_4[1] = offset_4[1] + r_d

	# print("after changes:-")
	# print(offset_1)
	# print(offset_2)
	# print(offset_3)
	# print(offset_4)

	change_pixel(im,offset_1[0],offset_1[1])
	change_pixel(im,offset_2[0],offset_2[1])
	change_pixel(im,offset_3[0],offset_3[1])
	change_pixel(im,offset_4[0],offset_4[1])

	return [[offset_1,offset_2,offset_3,offset_4],im]

def get_rotated_image(im,offset_values):
	[offset_1,offset_2,offset_3,offset_4] = offset_values
	#--------- ROTATION ----------
	from scipy import ndimage

	angle1 = get_angle_to_be_rotated(offset_1,offset_3)
	angle2 = get_angle_to_be_rotated(offset_2,offset_4)

	angle = (angle1+angle2)/2.0
	print(angle)

	rotated_image = ndimage.rotate(im,-angle)

	return rotated_image
	# cv2.imwrite("rotated_xerox_2.jpg",rotated_image)

def get_angle_to_be_rotated(a,b):
	import math
	try:
		slope = (b[1]-a[1])*1.0/(b[0]-a[0])
		angle = math.degrees(math.atan(slope))
	except:
		angle = 90
	if(angle > 0):
		angle =  90 - angle
	else:
		angle = -90 - angle
	# print(angle)
	return angle

def get_crop_lines(im,offset_values,cropping_info = None):
	[offset_1,offset_2,offset_3,offset_4] = offset_values
	im2 = copy.deepcopy(im)

	h = 1383.0
	v = 890.0
	V_len = ((offset_2[0] - offset_1[0]) + (offset_4[0] - offset_3[0]))/2.0
	H_len = ((offset_3[1] - offset_1[1]) + (offset_4[1] - offset_2[1]))/2.0
	# print("------")
	# print(H_len)
	# print(V_len)
	
	X_OFFSET = -32*H_len/h + offset_1[0]
	Y_OFFSET =  36*V_len/v + offset_1[1] + 1
	X_GAP  	 = 	23*H_len/h
	Y_GAP  	 = 	24*V_len/v - 1
	WIDTH    = 115*H_len/h
	HEIGHT   = 110*V_len/v - 1
	ROWS     = 10
	COLUMNS  = 7

	# print("X_OFFSET = "+str(X_OFFSET))
	# print("Y_OFFSET = "+str(Y_OFFSET))
	# print("X_GAP = "+str(X_GAP))
	# print("Y_GAP = "+str(Y_GAP))
	# print("WIDTH = "+str(WIDTH))
	# print("HEIGHT = "+str(HEIGHT))

	for i in range(ROWS):
		for j in range(COLUMNS):
			yu=int(Y_OFFSET+i*HEIGHT+(i+1)*Y_GAP)
			xl=int(X_OFFSET+j*WIDTH +(j+1)*X_GAP)
			yd=int(yu+HEIGHT)
			xr=int(xl+WIDTH)
			if(cropping_info != None):
				CROPPED_IMAGE_DIRECTORY = cropping_info[0]
				FILE_NAME = cropping_info[1]
				sub_folder_name = str(i)+"_"+str(j)
				DESTINATION_PATH = CROPPED_IMAGE_DIRECTORY + "\\" + sub_folder_name + "\\" + FILE_NAME + "__" + sub_folder_name + ".png"
				# print(DESTINATION_PATH)
				tmp_img=im[yu:yd,xl:xr] #crop
				cv2.imwrite(DESTINATION_PATH,tmp_img) #create image
			for k in range(xl,xr+1):
				for l in [yu,yd]:
					change_pixel_(im2,k,l)

			for l in range(yu,yd+1):
				for k in [xl,xr]:
					change_pixel_(im2,k,l)
			#testing
			#show_=tmp_img
			#if(i==0 and j==0):
				#break
	return im2

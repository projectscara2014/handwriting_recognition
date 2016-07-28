def change_pixel_(*args):
	try:
		change_pixel(*args)
	except:
		print("#")

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

def main(FILE_PATH):
	im = cv2.imread(FILE_PATH)
	# im = cv2.imread('black.png')
	kernel_1 = cv2.imread("kernel_1_final.png")
	kernel_2 = cv2.imread("kernel_2_final.png")

	im_dimensions = [len(im),len(im[0])] # [ht,wd]
	### -------- REGION OF INTERESTS ---------

	REGION_WIDTH  = 225
	REGION_HEIGHT = 165

	for i in range(REGION_WIDTH+1):
		change_pixel(im,i,REGION_HEIGHT)

	for i in range(REGION_HEIGHT+1):
		change_pixel(im,REGION_WIDTH,i)

	region_1 = im[0:REGION_HEIGHT,0:REGION_WIDTH]
	# cv2.imwrite("region_of_interest1.png",region_1)


	for i in range(im_dimensions[1] - REGION_WIDTH, im_dimensions[1]):
		change_pixel(im,i,REGION_HEIGHT)

	for i in range(REGION_HEIGHT+1):
		change_pixel(im,im_dimensions[1] - REGION_WIDTH,i)

	region_2 = im[0:REGION_HEIGHT, im_dimensions[1] + 1 - REGION_WIDTH : im_dimensions[1] ]
	# cv2.imwrite("region_of_interest2.png",region_2)

	##------ GETTING POINTS FOR SLOPE ---------
	import get_orientation
	# import cv2

	# offset_1 = get_orientation.main(region_1,kernel_1)
	# offset_2 = get_orientation.main(region_2,kernel_2)

	offset_1 = [122,44] # [x,y]
	offset_2 = [18,45]

	offset_2[0] = offset_2[0] + im_dimensions[1] - REGION_WIDTH + 1
	print(offset_2)

	change_pixel(im,offset_1[0],offset_1[1])
	change_pixel(im,offset_2[0],offset_2[1])

	##--------- ROTATION ----------
	import math
	from scipy import ndimage

	a = offset_1
	b = offset_2

	slope = (b[1]-a[1])*1.0/(b[0]-a[0])
	angle = math.degrees(math.atan(slope))
	print(angle)

	rotated_image = ndimage.rotate(im,angle)

	im = rotated_image
	# cv2.imwrite("rotated_xerox_2.jpg",rotated_image)


	# # # ##------- GETTING ORIENTATION -------------
	region = im[0:REGION_HEIGHT,0:REGION_WIDTH]
	# offset = get_orientation.main(region,kernel_1)
	offset = [123,45] # [x,y]
	print(offset)

	#global parameters
	WIDTH    = 175
	HEIGHT   = 175
	Y_OFFSET = offset[1] + 57
	X_OFFSET = offset[0] - 49
	# Y_OFFSET = offset[1] + 10
	# X_OFFSET = offset[0] + 6
	X_GAP    = 46
	Y_GAP    = 40
	ROWS     = 10
	COLUMNS  = 7

	for j in range(COLUMNS):
		for i in range(ROWS):
			yu=int(Y_OFFSET+i*HEIGHT+(i+1)*Y_GAP)
			xl=int(X_OFFSET+j*WIDTH +(j+1)*X_GAP)
			yd=yu+HEIGHT
			xr=xl+WIDTH
			# tmp_img=im[yu:yd,xl:xr] #crop
			# img_name='image '+str(i)+','+str(j)+'.jpg' # name
			# show_=cv2.imwrite(os.path.join(dirname,img_name),tmp_img) #create image
			for k in range(xl,xr+1):
				for l in [yu,yd]:
					change_pixel_(im,k,l)

			for l in range(yu,yd+1):
				for k in [xl,xr]:
					change_pixel_(im,k,l)

			#testing
			#show_=tmp_img
			#if(i==0 and j==0):
				#break

	return im

	#testing 
	#cv2.imshow('image',show_)#im[1:500,1:500])
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	print("DONE!!!")
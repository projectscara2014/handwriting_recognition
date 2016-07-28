
import cv2
import numpy as np
import os 
import shutil

#store cropped images in a new folder
dirname='cropped_images'
if(os.path.exists(dirname)):
	shutil.rmtree(dirname)
os.mkdir(dirname)

im = cv2.imread('scanned_images.jpg')

#global parameters
WIDTH    = 185
HEIGHT   = 180
Y_OFFSET = 110
X_OFFSET = 40
X_GAP    = 36
Y_GAP    = 33
ROWS     = 10
COLUMNS  = 7

for j in range(COLUMNS):
	for i in range(ROWS):
		yu=Y_OFFSET+i*HEIGHT+(i+1)*Y_GAP
		xl=X_OFFSET+j*WIDTH +(j+1)*X_GAP
		yd=yu+HEIGHT
		xr=xl+WIDTH
		tmp_img=im[yu:yd,xl:xr]
		img_name='image '+str(i)+','+str(j)+'.jpg'
		show_=cv2.imwrite(os.path.join(dirname,img_name),tmp_img)
		
		
		#testing
		#show_=tmp_img
		#if(i==0 and j==0):
			#break

#testing 
#cv2.imshow('image',show_)#im[1:500,1:500])
#cv2.waitKey(0)
#cv2.destroyAllWindows()
print("DONE!!!")

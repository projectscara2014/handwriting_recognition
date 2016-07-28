# from ccl import rgb_to_bnw
import cv2
import time
import var

var.main()
camera_port = var.camera_port
camera = cv2.VideoCapture(camera_port)
BNW_THRESHOLD = 255
step1= 100
step2= 25
step3= 5

def rgb_to_bnw(image,threshold = 200,numpy_array = False) : 
	try:
		[r,g,b,s] = image[0][0]
		mode = 0
	except:
		mode = 1

	return_image = []
	for row in image : 
		return_image.append([])
		for pixel in row :
			if(mode==1):
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

def get_image():
	retval, im = camera.read()
	return im 

def check_background(im):
	for row in im:
		for element in row:
			if(element != 0):
				return False
	return True

def background_setting(n):
	global BNW_THRESHOLD
	for i in range(200):	
		time.sleep(0.3)
		camera_capture = get_image()
		cv2.imwrite("test.png",camera_capture)
		camera_capture = cv2.imread("test.png")
		bnw_im = rgb_to_bnw(camera_capture,BNW_THRESHOLD)
		flag = 0
		# for row in bnw_im:
		# 	for element in row:
		# 		if(element != 0):
		# 			flag = 1
		# 			break
		# 	if(flag == 1):
		# 		break
		# if(flag == 0):
		# 	break
		print("checking at:- "),
		print(BNW_THRESHOLD)
		bool_val = check_background(bnw_im)

		if(bool_val):
			import numpy as np
			cv2.imwrite("camera_capture_bnw.png",np.array(bnw_im))
			print("True at "),
			print(BNW_THRESHOLD)
			break

		BNW_THRESHOLD -= n
		if(BNW_THRESHOLD < 6):
			BNW_THRESHOLD = BNW_THRESHOLD + n
			break

# background_setting(5)
background_setting(step1)
print("---> "),
print(BNW_THRESHOLD)
BNW_THRESHOLD = BNW_THRESHOLD + step1 - step2
print("---> "),
print(BNW_THRESHOLD)
background_setting(step2)
BNW_THRESHOLD = BNW_THRESHOLD + step2 - step3
print("---> "),
print(BNW_THRESHOLD)
background_setting(step3)
print("---> "),
print(BNW_THRESHOLD)

# BNW_THRESHOLD = BNW_THRESHOLD + 10

if(BNW_THRESHOLD < 6):
	print("THRESHOLD LIMIT EXCEEDED")
	raise OSError

bnw_setting = str(BNW_THRESHOLD)

with open("background_setting.txt",'w') as f:
	f.write(str(bnw_setting))
	# f.write("100")

camera.release()
print("----DONE----")

# from ccl import rgb_to_bnw
import cv2
import time

camera_port = 0
camera = cv2.VideoCapture(camera_port)
BNW_THRESHOLD = 255

def rgb_to_bnw(image,threshold = 200) :
	return_image = []
	# numpy_array = False 
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
	# return return_image

def get_image():
	retval, im = camera.read()
	return im 

# def check_background(im):
# 	for row in im:
# 		for element in row:
# 			if(element != 0):
# 				return False
# 	return True

def background_setting():
	global BNW_THRESHOLD
	for i in range(200):		
		start_time = time.time()
		camera_capture = get_image()
		print("camera_capture:- "),
		print(time.time()-start_time)
		print(len(camera_capture))
		print(len(camera_capture[0]))
		start_time = time.time()

		bnw_im = rgb_to_bnw(camera_capture,BNW_THRESHOLD)
		print("rgb_to_bnw:- "),
		print(time.time()-start_time)
		start_time = time.time()
		flag = 0
		for row in bnw_im:
			for element in row:
				if(element != 0):
					flag = 1
					break
			if(flag == 1):
				break
		if(flag == 0):
			break
		print("loop:- "),
		print(time.time()-start_time)

		# bool_val = check_background(bnw_im)
		# print(bool_val)
		print(BNW_THRESHOLD)
		BNW_THRESHOLD -= 5 
		print(time.time()-start_time)

	return (BNW_THRESHOLD)

bwn_setting = background_setting()
print(bwn_setting)
camera.release()
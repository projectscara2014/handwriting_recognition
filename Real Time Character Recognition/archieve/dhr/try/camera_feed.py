import cv2
import os
import ccl
import numpy as np
import var

# override = True
override = False
DILATION_VALUE = 3


def check_background(im):
	for row in im:
		for element in row:
			if(element != 0):
				return False
	return True

def do(PATH):
	global BNW_THRESHOLD
	global DILATION_VALUE
	import cv2
	print(BNW_THRESHOLD)
	# 
	# ------------ Main
	image = cv2.imread(PATH + 'test_image_1.png')

	bnw_im = ccl.rgb_to_bnw(image,BNW_THRESHOLD)
	cv2.imwrite(PATH + "BNW_image_2.png",np.array(bnw_im))

	print(check_background(bnw_im))

	ccl_image_before_dilation_list = ccl.main(np.array(bnw_im),"color")
	ccl_image_before_dilation = ccl_image_before_dilation_list[0]
	cv2.imwrite(PATH +"ccl_image_before_dilation_3.png", np.array(ccl_image_before_dilation))

	kernel = np.ones((3,3),np.uint8)
	img = cv2.imread(PATH + "BNW_image_2.png")
	dilation = cv2.dilate(img, kernel , iterations = DILATION_VALUE)
	cv2.imwrite(PATH + "dilated_image_4.png",dilation)

	bnw_dilated_im = ccl.rgb_to_bnw(dilation,BNW_THRESHOLD)
	cv2.imwrite(PATH + "BNW_dilated_image_5.png",np.array(bnw_dilated_im))

	dilated_in_binary = []
	for row in dilation:
		dilated_in_binary.append([])
		for pixel in row:
			[r,g,b] = pixel
			dilated_in_binary[-1].append(int(r)+int(g)+int(b))

	dilated_ccl_image_list = ccl.main(dilated_in_binary,"color")
	dilated_ccl_image = dilated_ccl_image_list[0]

	cv2.imwrite(PATH + "dilated_ccl_image_6.png",np.array(dilated_ccl_image))

	ccl.main(dilated_in_binary)	

def get_image_saving_path() : 
	#print(os.getcwd())
	path = (os.getcwd().split('\\'))
	path.append('Pictures')
	return_path = ''
	for element in path : 
		return_path += element + '\\'
	path = return_path
	return path

def get_image(camera):
	retval, im = camera.read()
	return im

def main(queueLock,workQueue):
	global IMAGE_SAVING_PATH
	# camera_port = var.camera_port
	# camera = cv2.VideoCapture(camera_port)
	while (True):
		
		ret, frame = camera.read()
		cv2.imshow('frame', frame)
		camera_capture = get_image(camera)	
		queueLock.acquire()
		workQueue.put(camera_capture)
		queueLock.release()
		if cv2.waitKey(1) & 0xFF == ord('d'):
			camera.release()
			break
		elif cv2.waitKey(1) & 0xFF == ord('l'):
			print(len(camera_capture))

		elif cv2.waitKey(1) & 0xFF == ord('a'):
			camera_capture = get_image()
			try:
				len(camera_capture)
			except:
				print("NO IMAGE FOUND")
				import sys
				sys.exit()
		 	# file = IMAGE_SAVING_PATH + "test_image_1" + ".png"
			camera.release()
			cv2.destroyAllWindows()
		 	return test_image_1

# def get_image():
# 	retval, im = camera.read()
# 	return im

########## INIT #######
def init():
	with open("background_setting.txt" , 'r') as f:
		BNW_THRESHOLD = int(f.read())

	if(override):
	 	do(IMAGE_SAVING_PATH)
	else:
		var.main()
		# main()

init()

if(__name__ == "__main__"):
	import threads
	threads.main()
	import sys
	sys.exit()

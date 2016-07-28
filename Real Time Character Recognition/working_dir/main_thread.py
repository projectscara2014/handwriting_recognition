import Queue
import threading
import time
import var
import cv2
# import ccl
import numpy as np
import lib_image_processing
# import matplotlib.pyplot as plt
import character_identification_utils

class processing_thread (threading.Thread):
	def __init__(self,threadName,func):
		threading.Thread.__init__(self)
		self.name = threadName + " Thread"
		self.func = func
	def run(self):
		print "Starting " + self.name
		self.func(self.name)
		print "Exiting " + self.name

def display_process(name):
	global BNW_THRESHOLD, DILATION_ITERATIONS
	data = cv2.imread("white.png")
	master = "cam"
	while not exitFlag:
	# next frame logic
		if(master == "cam"):
			camera_displayQueueLock.acquire()
			if not camera_displayQueue.empty():
				data = camera_displayQueue.get()
			camera_displayQueueLock.release()
		elif(master == "bnw2"):
			bnw3_displayQueueLock.acquire()
			if not bnw3_displayQueue.empty():
				data = bnw3_displayQueue.get()
			bnw3_displayQueueLock.release()
		elif(master == "dilation"):
			dilation_displayQueueLock.acquire()
			if not dilation_displayQueue.empty():
				data = dilation_displayQueue.get()
			dilation_displayQueueLock.release()
		elif(master == "ccl"):
			ccl_displayQueueLock.acquire()
			if not ccl_displayQueue.empty():
				data = ccl_displayQueue.get()
			ccl_displayQueueLock.release()
		elif(master == "box"):
			box_displayQueueLock.acquire()
			if not box_displayQueue.empty():
				data = box_displayQueue.get()
			box_displayQueueLock.release()

	# update logic
		cv2.imshow('frame',data)
		# plt.imshow(data)
		# plt.show()
		key_press = cv2.waitKey(10)
	# on-keypress events
		if key_press & 0xFF == ord('p'):
			exit_all()
		elif key_press & 0xFF == ord('s'):
			master = "cam"
			print("s pressed")
		elif key_press & 0xFF == ord('d'):
			master = "bnw2"
			print("d pressed")
		elif key_press & 0xFF == ord('f'):
			master = "dilation"
			print("f pressed")
		elif key_press & 0xFF == ord('g'):
			master = "ccl"
			print("g pressed")
		elif key_press & 0xFF == ord('h'):
			master = "box"
			print("h pressed")
		elif key_press & 0xFF == ord('j'):
			print("j pressed")
		elif key_press & 0xFF == ord('e'):
			print("BNW_THRESHOLD => "),
			if(BNW_THRESHOLD<250):
				BNW_THRESHOLD += 1
			print(BNW_THRESHOLD)
		elif key_press & 0xFF == ord('x'):
			print("BNW_THRESHOLD => "),
			if(BNW_THRESHOLD>10):
				BNW_THRESHOLD -= 1
			print(BNW_THRESHOLD)
		elif key_press & 0xFF == ord('t'):
			print("DILATION_ITERATIONS => "),
			if(DILATION_ITERATIONS<10):
				DILATION_ITERATIONS += 1
			print(DILATION_ITERATIONS)
		elif key_press & 0xFF == ord('v'):
			print("DILATION_ITERATIONS => "),
			if(DILATION_ITERATIONS>0):
				DILATION_ITERATIONS -= 1
			print(DILATION_ITERATIONS)

def camera_process(name):
	return_val = var.main()
	camera_port = var.camera_port
	camera = cv2.VideoCapture(camera_port)
	if(not return_val):
		exit_all()
		im = cv2.imread("last_capture.png")
	while not exitFlag:
	# operation
		ret, im = camera.read()
	# camera_display
		camera_displayQueueLock.acquire()
		while not camera_displayQueue.empty():
			camera_displayQueue.get()
		if not camera_displayQueue.full():
			camera_displayQueue.put(im)
		camera_displayQueueLock.release()
	# camera
		cameraQueueLock.acquire()
		while not cameraQueue.empty():
			cameraQueue.get()
		if not cameraQueue.full():
			cameraQueue.put(im)
		cameraQueueLock.release()
	# operation
		ret, im = camera.read()
	# camera2
		camera2QueueLock.acquire()
		while not camera2Queue.empty():
			camera2Queue.get()
		if not camera2Queue.full():
			camera2Queue.put(im)
		camera2QueueLock.release()
	# exit process
	camera.release()
	cv2.imwrite("last_capture.png",im)

def camera2_process(name):
	pass
	
def bnw2_process(name):
	image = cv2.imread("last_capture.png")
	while not exitFlag:
	# camera
		cameraQueueLock.acquire()
		if not cameraQueue.empty():
			image = cameraQueue.get()
		cameraQueueLock.release()
	# operation
		bnw2_im = lib_image_processing.threshold2(image,BNW_THRESHOLD)
	# bnw2
		bnw2QueueLock.acquire()
		if not bnw2Queue.full():
			bnw2Queue.put(bnw2_im)
		bnw2QueueLock.release()
	# bnw2_display
		bnw2_displayQueueLock.acquire()
		while not bnw2_displayQueue.empty():
			bnw2_displayQueue.get()
		if not bnw2_displayQueue.full():
			bnw2_displayQueue.put(bnw2_im)
		bnw2_displayQueueLock.release()
	# exit process
	cv2.imwrite("last_bnw.png",bnw2_im)

def bnw3_process(name):
	image = cv2.imread("last_capture.png")
	while not exitFlag:
	# camera
		cameraQueueLock.acquire()
		if not cameraQueue.empty():
			image = cameraQueue.get()
		cameraQueueLock.release()
	# operation
		bnw3_im = lib_image_processing.threshold3(image,BNW_THRESHOLD)
	# bnw3
		bnw3QueueLock.acquire()
		if not bnw3Queue.full():
			bnw3Queue.put(bnw3_im)
		bnw3QueueLock.release()
	# bnw3_display
		bnw3_displayQueueLock.acquire()
		while not bnw3_displayQueue.empty():
			bnw3_displayQueue.get()
		if not bnw3_displayQueue.full():
			bnw3_displayQueue.put(bnw3_im)
		bnw3_displayQueueLock.release()
	# exit process
	cv2.imwrite("last_bnw.png",bnw3_im)

def dilation_process(name):
	# kernel = np.ones((3,3),np.uint8)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))

	image = cv2.imread("last_bnw.png")
	while not exitFlag:
	# bnw2
		bnw2QueueLock.acquire()
		if not bnw2Queue.empty():
			image = bnw2Queue.get()
		bnw2QueueLock.release()
	# operation
		dilation_im = cv2.dilate(image, kernel , iterations = DILATION_ITERATIONS)
	# dilation
		dilationQueueLock.acquire()
		if not dilationQueue.full():
			dilationQueue.put(dilation_im)
		dilationQueueLock.release()
	# dilation_display
		dilation_displayQueueLock.acquire()
		while not dilation_displayQueue.empty():
			dilation_displayQueue.get()
		if not dilation_displayQueue.full():
			dilation_displayQueue.put(dilation_im)
		dilation_displayQueueLock.release()
	# exit process
	cv2.imwrite("last_dilation.png",dilation_im)

def ccl_process(name):
	while not exitFlag:
		if dilationQueue.empty():
			continue
	# dilation
		dilationQueueLock.acquire()
		while not dilationQueue.empty():
			dilation = dilationQueue.get()
		dilationQueueLock.release()
	# operation
		modified_dilation = lib_image_processing.threshold3(dilation,10)
		im1, contours, hierarchy = cv2.findContours(modified_dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		# final_contour_list = decision_maker.main(contours)
		color_space = character_identification_utils.get_color_space(contours)

		# find biggest parent
		a = 0
		parent_index = 0
		contour_info_list = []
		for i in range(len(contours)):
			[x,y,w,h] = cv2.boundingRect(contours[i])
			# print(hierarchy[0][i])
			contour_info_list.append([x,y,w,h])
			if(w*h>a):
				a = w*h
				parent_index = i

		# print(parent_index)

		# main color
		main_index_list = []
		for i in range(len(contours)):
			if(hierarchy[0][i][3] == parent_index):
				main_index_list.append(i)

		# print(main_index_list)

		# child color
		child_index_list = []
		for i in range(len(contours)):
			if(hierarchy[0][i][3] in main_index_list):
				child_index_list.append(i)

		# print(child_index_list)

		for i in range(len(contours)):
			[x,y,w,h] = contour_info_list[i]

			if i in main_index_list:
				cv2.drawContours(dilation,contours,i,color_space[i],-1)
			if i in child_index_list:
				cv2.drawContours(dilation,contours,i,(0,0,0),-1)		
	# ccl
		cclQueueLock.acquire()
		if not cclQueue.full():
			cclQueue.put([main_index_list,contour_info_list,dilation])
		cclQueueLock.release()
	# ccl_display
		ccl_displayQueueLock.acquire()
		while not ccl_displayQueue.empty():
			ccl_displayQueue.get()
		if not ccl_displayQueue.full():
			ccl_displayQueue.put(dilation)
		ccl_displayQueueLock.release()
	# exit process
	cv2.imwrite("last_ccl.png",dilation)

def box_process(name):
	font = cv2.FONT_HERSHEY_SIMPLEX
	while not exitFlag:
		if cclQueue.empty():
			continue
	# camera2
		while camera2Queue.empty():
			pass
		camera2QueueLock.acquire()
		if not camera2Queue.empty():
			original = camera2Queue.get()
		camera2QueueLock.release()
	# bnw3
		bnw3QueueLock.acquire()
		if not bnw3Queue.empty():
			bnw5 = bnw3Queue.get()
		bnw3QueueLock.release()
	# ccl
		cclQueueLock.acquire()
		while not cclQueue.empty():
			[main_index_list,contour_info_list,ccl] = cclQueue.get()
		cclQueueLock.release()
	# operation
		for i in main_index_list:
			[x,y,w,h] = contour_info_list[i]
			[x,y,w,h] = scan_and_crop(bnw5,[x,y,w,h])
			# discard areas that are too big
			if h>70 and w>70:
				# main_index_list.pop(i)
				continue

			# discard areas that are too small
			if h<20 or w<20:
				# main_index_list.pop(i)
				continue
			# print(color_space[i])
			cv2.rectangle(original,(x,y),(x+w,y+h),(0,0,255),1)
			cropped_im = bnw5[y:y+h,x:x+w]
			return_val = character_identification_utils.identify(cropped_im)
			cv2.putText(original,return_val,(x,y), font, 0.8,(255,0,0),2,cv2.LINE_AA)
	# box
		boxQueueLock.acquire()
		if not boxQueue.full():
			boxQueue.put(original)
		boxQueueLock.release()
	# box_display
		box_displayQueueLock.acquire()
		while not box_displayQueue.empty():
			box_displayQueue.get()
		if not box_displayQueue.full():
			box_displayQueue.put(original)
		box_displayQueueLock.release()
	# exit process
	cv2.imwrite("last_box.png",original)

def scan_and_crop(im,contour_info_list):
	[x,y,w,h] = contour_info_list
	max_h = y
	min_h = y+h
	max_l = x
	min_l = x+w
	for i in range(y,y+h):
		for j in range(x,x+w):
			if(im[i][j] != 0):
				if(i<min_h):
					min_h = i
				if(i>max_h):
					max_h = i
				if(j>max_l):
					max_l = j
				if(j<min_l):
					min_l = j
	# print [x,y,w,h]
	# print [min_l,min_h,max_l-min_l,max_h-min_h]
	# h = lvvds
	return [min_l,min_h,max_l-min_l,max_h-min_h]

def exit_all():
	global exitFlag
	exitFlag = 1
	time.sleep(0.2)
	displayQueueLock.acquire()

def main():
	global exitFlag
	threadID = 1

	# Wait for queue to empty
	while not exitFlag:
		pass
	# # Wait for all threads to complete
	for t in thread_list:
	    t.join()
	print "Exiting Main Thread"
	save_all()

def save_all():
	with open("background_setting.txt",'w') as f:
		c = str(BNW_THRESHOLD) + "\n" + str(DILATION_ITERATIONS)
		f.write(c)
		# f.write(str(BNW_THRESHOLD))

def read_all():
	global BNW_THRESHOLD, DILATION_ITERATIONS
	with open("background_setting.txt" , 'r') as f:
		c = [int(i) for i in f.read().split("\n")]
		BNW_THRESHOLD = c[0]
		DILATION_ITERATIONS = c[1]

# global variables
read_all()
print("BNW_THRESHOLD = "+str(BNW_THRESHOLD))
print("DILATION_ITERATIONS = "+str(DILATION_ITERATIONS))
exitFlag = 0

# threads
thread_name_list = ["Camera","Camera2","BNW3","BNW2","Dilation","CCL","Box"]
# thread_name_list = ["Camera"]
q_val = 4

t = []
for word in thread_name_list:
	t.append(word)
	t.append(word+"_display")
queue_name_list = t
queue_name_list.append("Display")
for name in queue_name_list:
	lower_name = name.lower()
	exec(lower_name+"QueueLock = threading.Lock()")
	exec(lower_name+"Queue = Queue.Queue("+str(q_val)+")")
thread_name_list.append("Display")
thread_list = []
for name in thread_name_list:
	lower_name = name.lower()
	exec(lower_name+"_thread = processing_thread(\""+name+"\","+lower_name+"_process)")
	exec("thread_list.append("+lower_name+"_thread)")
	exec(lower_name+"_thread.start()")

if(__name__ == "__main__"):
	main()
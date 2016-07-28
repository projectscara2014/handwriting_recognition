import cv2 
import sys 
import time

def main():
	global camera_port
	LAPTOP_CAM_VAL = 64
	USB_CAM_VAL = 60

	camera_port = 0

	sat_list = []
	for camera_port in [0,1]:
		camera = cv2.VideoCapture(camera_port)
		time.sleep(0.1)
		# print(camera)
		# print(type(camera))
		sat = camera.get(cv2.CAP_PROP_SATURATION)
		sat_list.append(int(sat))
		camera.release()
	# print(sat_list)

	if(USB_CAM_VAL in sat_list):
		camera_port = sat_list.index(USB_CAM_VAL)
	else:
		print("CAMERA NOT CONNECTED")
		sys.exit(0)

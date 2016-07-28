if(__name__ == "__main__"):
	import auto_script_3_skin_cropped_to_tilted
	import sys
	sys.exit(0)

import resize
from scipy import ndimage
import cv2
import numpy as np
import scan_and_crop

def rotate_and_save(im,angle,DESTINATION_PATH):
	if(angle == 0):
		pass
	else:
		im = ndimage.rotate(im,angle)
	# print(angle)

	DESTINATION_PATH = DESTINATION_PATH.split("\\")
	FILE_NAME = DESTINATION_PATH.pop(-1)
	FILE_NAME = FILE_NAME.split(".")
	FILE_NAME[0] = FILE_NAME[0] + "_" + str(angle)
	FILE_NAME = ".".join(FILE_NAME)
	DESTINATION_PATH.append(FILE_NAME)
	DESTINATION_PATH = "\\".join(DESTINATION_PATH)
	# print(len(im))
	im = scan_and_crop.main(im)
	cv2.imwrite(DESTINATION_PATH,im)

def main(IMAGE_PATH,DESTINATION_PATH):
	# DESTINATION_PATH_ = DESTINATION_PATH.split(".")
	# DESTINATION_PATH_[1] = "npy"
	# DESTINATION_PATH_ = ".".join(DESTINATION_PATH_)

	im = cv2.imread(IMAGE_PATH)
	# rotate_and_save(im,0,DESTINATION_PATH)
	increment_by = 4
	n = 5
	im2 = []
	# im2 = np.load(DESTINATION_PATH_).tolist()
	# print(len(im2))

	for i in range(1,n+1,1):
		pos_rot_im = ndimage.rotate(im,i*increment_by)
		pos_rot_im = scan_and_crop.main(pos_rot_im)
		im2.append(pos_rot_im)
		neg_rot_im = ndimage.rotate(im,-i*increment_by)
		neg_rot_im = scan_and_crop.main(neg_rot_im)
		im2.append(neg_rot_im)
		# rotate_and_save(im,i*increment_by,DESTINATION_PATH)
		# rotate_and_save(im,-i*increment_by,DESTINATION_PATH)
		# print(len(im2))
	# print(DESTINATION_PATH_)
	# print(len(im2))
	im = scan_and_crop.main(im)
	return [im,im2]
	# cv2.imwrite(DESTINATION_PATH,im2)
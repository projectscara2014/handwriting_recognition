if(__name__ == "__main__"):
	import auto_script_3_skin_cropped_to_tilted
	import sys
	sys.exit(0)

import numpy as np
import resize

def rgb_to_bnw(image,threshold = 100,numpy_array = False) : 
    return_image = []
    for row in image : 
        return_image.append([])
        for pixel in row :
            [r,g,b] = pixel
            magnitude= (int(r)+int(g)+int(b))/3
            if(magnitude < threshold) : 
                return_image[-1].append(0)
            else:
                return_image[-1].append(255)
    if(numpy_array):
        return np.array(return_image)
    else:
        return return_image

def main(im):
	# print(len(im))
	x1 = 0
	x2 = len(im)
	y1 = 0
	y2 = len(im)

	for i in range(len(im)):
		for j in range(len(im[i])):
			[r,g,b] = im[i][j]
			magnitude= (int(r)+int(g)+int(b))/3
			if(magnitude != 0):
				if(i<x1):
					x1 = i
				if(i>x2):
					x2 = i
				if(j<y1):
					y1 = j
				if(j>y2):
					y2 = j

	# print(x1,x2,y1,y2)
	im = np.array(im)
	cropped_im = im[y1:y2+1,x1:x2]
	bnw_cropped_im = np.array(rgb_to_bnw(cropped_im,200))
	resized_image = resize.main(bnw_cropped_im)
		
	threshold_resize = 0
	for i in range(len(resized_image)):
		for j in range(len(resized_image[i])):
			if(resized_image[i][j]>threshold_resize):
				resized_image[i][j] = 255
			else:
				resized_image[i][j] = 0

	return resized_image
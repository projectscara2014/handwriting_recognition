import cv2

if __name__ == '__main__':
	import try2
	import sys
	sys.exit(0)

def main(contours):
	im_size = [480,640]
	im_centre = [240,320]
	print("###########################")
	contours_info = []
	radius_squared_list = []
	area_list = []
	ratio_list = []
	for i in range(len(contours)):
		[x,y,w,h] = cv2.boundingRect(contours[i])

		contours_info.append([x,y,w,h])
		rw = im_centre[0]-x
		rh = im_centre[1]-y
		# r2 = ()**2 + ()**2
		# radius_squared_list.append(r2)
		a = w*h
		area_list.append(a)
		ratio_list.append(int(a*2000.0/(rh*rh*rw)))

	print(len(contours_info))
	print(radius_squared_list)
	print(area_list)
	print(ratio_list)
	return_list = []
	for i in range(len(ratio_list)):
		if(ratio_list[i] != 0):
			return_list.append(i)
	print(return_list)

	for i in return_list:
		[x,y,w,h] = contours_info[i]
		# in x direction
		
	print("###########################")
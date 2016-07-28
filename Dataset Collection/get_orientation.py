import numpy as np

def rgb_to_bnw(image,threshold = 200,numpy_array = False) : 
    return_image = []
    for row in image : 
        return_image.append([])
        for pixel in row :
            [r,g,b] = pixel
            magnitude= (int(r)+int(g)+int(b))/3
            if(magnitude < threshold) : 
                return_image[-1].append(1)
            else:
                return_image[-1].append(255)
    if(numpy_array):
        return np.array(return_image)
    else:
        return return_image

def convolution(image,kernel) : 
    # scaling_factor = kernel[0]
    # kernel = kernel[1]
    image_width = len(image[0])
    image_height = len(image)
    kernel_width = len(kernel[0])
    kernel_height = len(kernel)

    def element_wise_matrix_multiplication(matrix1,matrix2,scaling_factor=1) :
        return_value = 0
        for m1_row,m2_row in zip(matrix1,matrix2) :
            for m1_pixel,m2_pixel in zip(m1_row,m2_row) :
                return_value += int(m1_pixel)*int(m2_pixel)
        return (return_value/scaling_factor)

    return_image = []
    for row in range(image_height - kernel_height + 1) :
		return_image.append([])
		for pixel in range(image_width - kernel_width + 1) :
			image_slice = []
			for i in range(row,row + kernel_height):
				image_slice.append([])
				for j in range(pixel,pixel + kernel_width):
					image_slice[-1].append(image[i][j])
			return_image[-1].append(element_wise_matrix_multiplication(image_slice,kernel))
    return (return_image)

def modify_kernel(kernel):
	for i in range(len(kernel)):
		for j in range(len(kernel[i])):
			if(kernel[i][j] == 1):
				kernel[i][j] = -1
			else:
				kernel[i][j] = 1
	return kernel

from lib_image_processing import convolution as convolution_

def main(region,kernel):
    # print("region dimensions")
    # print([len(region),len(region[0])])
    # print("kernel dimensions")
    # print([len(kernel),len(kernel[0])])
    bnw_image   = rgb_to_bnw(region,200)
    bnw_kernel  = rgb_to_bnw(kernel,200)
    kernel = modify_kernel(bnw_kernel)

    orientation = convolution_(bnw_image,[1,kernel])

    # orientation = convolution(bnw_image,kernel)

    s = 0
    # print("orientation dimensions")
    # print([len(orientation),len(orientation[0])])
    for i in range(len(orientation)):
        for j in range(len((orientation[i]))):
            if(orientation[i][j] > s):
                s = orientation[i][j]
                return_list = [j,i] # x,y
    #remove effect of padding
    return_list[0] = return_list[0] - 44
    return_list[1] = return_list[1] - 44
    # print(return_list)
    return return_list
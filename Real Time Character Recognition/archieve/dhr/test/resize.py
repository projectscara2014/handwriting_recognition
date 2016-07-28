
# #----------------------- CONSTANTS ------------------------------
FINAL_IMAGE_SIZE = 20
# #----------------------------------------------------------------

import cv2
import numpy
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def time_this_function(function) : 
    try : 
        time
    except : 
        import time
    
    def wrapper_function(*args,**kwargs) : 
        start_time = time.time()
        return_value = function(*args,**kwargs)
        elapsed_time = (time.time() - start_time)*1000
        print(function.__name__ + ' -- elapsed_time -- ' + str(elapsed_time) + ' ms\n')
        return return_value
    return wrapper_function


class reshape() :	

	def __init__(self) : 
		pass

	def generate_integer_string(self,integer,number_of_characters) :
		l = [str(0) for j in range(number_of_characters-len(str(integer)))]
		if l == [] :
			print('generate_integer_string --> number_of_characters can not be less that the length of the intger')
			raise ValueError
		for element in str(integer) :
			l.append(element)
		string = ''
		for element in l : 
			string += element
		return string

	def generate_expected_output_list(self,i) : 
		return_list = []
		for j in range(1,63) :
			if j == i :
				return_list.append(1)
			else : 
				return_list.append(0)
		return return_list

	def rgb_to_bnw(self,image,mask=None) :
		mask_image = []
		if mask == None :
			mask_image = numpy.ones(image.shape[:-1],dtype=numpy.uint8)
			mask_image *= 255 
		else : 
			mask_image = numpy.zeros(image.shape[:-1],dtype=numpy.uint8)
			for i in range(len(mask)) : 
				for j in range(len(mask[i])) :
					mask_image[i][j] = sum(mask[i][j])/3.0
		return_image = numpy.zeros(image.shape[:-1],dtype=numpy.uint8)
		for i in range(len(image)) : 
			for j in range(len(image[i])) :
				return_image[i][j] = (sum(image[i][j])/3.0)*(mask_image[i][j]/255)
		return return_image

	# @time_this_function
	def reshape(self,image) :
		#asssumes a black and white image as input (will not work with RGB image) 
		
		# @debug()
		def vertical_stack(array_1,array_2) : 
			'''
			emulates functionality of numpy.vstack function
			but works for arrays that are not of excatly the same shape
			only the widths of the 2D arrays should be the same
			'''

			try :
				array_1.shape[1]
				array_2.shape[1]
			except IndexError :
				return array_1
			if array_1.shape[1] != array_2.shape[1] : 
				error_string = 'both arrays should be of same widths\n array_1.shape --> {0}\n array_2.shape --> {1}'.format(array_1.shape,array_2.shape)
				raise ValueError(error_string)
			return_array = numpy.zeros([array_1.shape[0] + array_2.shape[0],array_2.shape[1]],dtype=numpy.uint8)

			row_count = 0
			for row1 in array_1 : 
				return_array[row_count] = row1
				row_count += 1
			for row2 in array_2 : 
				return_array[row_count] = row2
				row_count += 1
			return return_array

		# @debug()
		def horizontal_stack(array_1,array_2) :
			'''
			emulates functionality of numpy.hstack function
			but works for arrays that are not of excatly the same shape
			only the heights of the 2D arrays should be the same
			'''

			try :
				array_1.shape[1]
				array_2.shape[1]
			except IndexError :
				return array_1
			if array_1.shape[0] != array_2.shape[0] :
				error_string = 'both arrays should be of same widths\n array_1.shape --> {0}\n array_2.shape --> {1}'.format(array_1.shape,array_2.shape)
				raise ValueError(error_string) 
			return_array = numpy.zeros([array_2.shape[0],array_1.shape[1] + array_2.shape[1]],dtype=numpy.uint8)
			
			row_count = 0
			for row1,row2 in zip(array_1,array_2) :
				# print(numpy.append(row1,row2).shape) 
				return_array[row_count] = numpy.append(row1,row2)
				row_count += 1
			return return_array

		# @debug()
		def add_rows(image,image_width,image_height,rows_to_add=None,side_to_add=None) :
			'''
			if rows_to_add == None, the side_to_add parameter is ignored
			if rows_to_add != None and side_to_add == None, equal number of columns will
			be added to both the sides of the image (bottom greater thatn ttop by one if odd
			number of columns to add)
			'''
			_rows_to_add_ = image_width - image_height
			_side_to_add_ = None
			allowed_sides = ['Top','Bottom']
			flag = 0
			if rows_to_add != None :
				_rows_to_add_ = rows_to_add
				if side_to_add != None :
					if side_to_add not in allowed_sides :
						raise ValueError('side_to_add should either be "Top" or "Bottom"')
					_side_to_add_ = side_to_add
					flag = 1
			rows_to_add = _rows_to_add_
			side_to_add = _side_to_add_

			concatenating_array_top = numpy.array([])
			concatenating_array_bottom = numpy.array([])
			if flag == 0 :
				concatenating_array_top = numpy.zeros([int(rows_to_add/2),image_width],dtype=numpy.uint8)
				if rows_to_add%2 == 0 : 
					concatenating_array_bottom = concatenating_array_top
				else :
					concatenating_array_bottom = numpy.zeros([int(rows_to_add/2)+1,image_width],dtype=numpy.uint8)
			else :
				if side_to_add == 'Top' :
					concatenating_array_top = numpy.zeros([int(rows_to_add),image_width],dtype=numpy.uint8)
				elif side_to_add == 'Bottom' :
					concatenating_array_bottom = numpy.zeros([int(rows_to_add/2),image_width],dtype=numpy.uint8)
			image = vertical_stack(concatenating_array_top,image)
			image = vertical_stack(image,concatenating_array_bottom)
			return image

		# @debug()
		def add_columns(image,image_width,image_height,columns_to_add=None,side_to_add=None) : 
			'''
			if columns_to_add == None, the side_to_add parameter is ignored
			if columns_to_add != None and side_to_add == None, equal number of columns will
			be added to both the sides of the image (right greater than left by one if odd
			number of columns to add)
			'''

			_columns_to_add_ = image_height - image_width
			_side_to_add_ = None
			allowed_sides = ['Left','Right']
			flag = 0
			if columns_to_add != None :
				_columns_to_add_ = columns_to_add
				if side_to_add != None :
					if side_to_add not in allowed_sides :
						raise ValueError('side_to_add should either be "Left" or "Right"')
					_side_to_add_ = side_to_add
					flag = 1
			columns_to_add = _columns_to_add_
			side_to_add = _side_to_add_

			concatenating_array_left = numpy.array([])
			concatenating_array_right = numpy.array([])

			if flag == 0 :
				concatenating_array_left = numpy.zeros([image_height,int(columns_to_add/2)],dtype=numpy.uint8)
				if columns_to_add%2 == 0 : 
					concatenating_array_right = concatenating_array_left
				else : 
					concatenating_array_right = numpy.zeros([image_height,int(columns_to_add/2)+1],dtype=numpy.uint8)
			else :
				if side_to_add == 'Left' :
					concatenating_array_left = numpy.zeros([image_height,int(columns_to_add)],dtype=numpy.uint8)
				elif side_to_add == 'Right' :
					concatenating_array_right = numpy.zeros([image_height,int(columns_to_add)],dtype=numpy.uint8)
			image = horizontal_stack(concatenating_array_left,image)
			image = horizontal_stack(image,concatenating_array_right)		
			return image

		# @debug()
		def make_square(image) : 

			image_width = image.shape[1]
			image_height = image.shape[0]
			if image_width > image_height : 
				image = add_rows(image,image_width,image_height)
			elif image_width < image_height : 
				image = add_columns(image,image_width,image_height)
				# print(image.shape)
			else : 
				#already square
				pass

			return image

		def fit_to_size(image) : 
			'''
			expects a square image
			converts the square image to a (FINAL_IMAGE_SIZE x FINAL_IMAGE_SIZE) image
			'''

			if image.shape[0] != image.shape[1] : 
				raise ValueError('image should be square')
			global FINAL_IMAGE_SIZE
			image_size = image.shape[0]
			width_to_add = FINAL_IMAGE_SIZE - image_size%FINAL_IMAGE_SIZE
			image = add_rows(image,image_size,image_size,width_to_add)
			image = add_columns(image,image_size,image_size+width_to_add,width_to_add)
			
			return_image = numpy.zeros([FINAL_IMAGE_SIZE,FINAL_IMAGE_SIZE],dtype=numpy.uint8)
			scaling_factor = int(image.shape[0]/FINAL_IMAGE_SIZE)
			if scaling_factor == 1 :
				return image
			else :
				row_number = 0
				while row_number < len(image) :
					temp_image = image[row_number:row_number+scaling_factor]
					temp_return_image = []
					temp_row_number = 0
					while temp_row_number < len(temp_image) :
						row = temp_image[temp_row_number]
						temp_return_image.append([])
						column_number = 0
						while column_number < len(row) :
							temp_return_image[-1].append((sum(row[column_number:column_number+\
								scaling_factor]))/scaling_factor)
							column_number += scaling_factor
						temp_row_number += 1

					for i in range(len(temp_return_image[0])) :
						return_image[int(row_number/scaling_factor)][i] = \
						sum([element[i] for element in temp_return_image])/scaling_factor
					row_number += scaling_factor
			return return_image

		image = make_square(image)
		image = fit_to_size(image)
		return image

def main(image):
	r = reshape()
	reshaped_im = r.reshape(image) 
	return reshaped_im
image = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 255, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 255, 255, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 255, 0, 0, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 255, 255, 0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 255, 0, 0, 255, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def pixel_to_binary(pixel_value) : 
	new_pixel_value = 0
	if(pixel_value == 255) : 
		new_pixel_value = 1
	else : 
		new_pixel_value = 0

	image_bits = ''
	for i in range(4) : 
		image_bits += '0'
	image_bits += str(new_pixel_value)
	for i in range(11) : 
		image_bits += '0'
	return image_bits

def reshape_image(image) :
	new_image = [] 
	for element in image : 
		for pixel in element : 
			new_image.append(pixel)

	reshaped_image = []
	for i in range(len(new_image)) : 
		if i%16 == 0 : 
			reshaped_image.append([])
		reshaped_image[-1].append(new_image[i])
	# print(reshaped_image)
	return reshaped_image

def HEXA(hex_):
	hex_ = hex(int(hex_))

	hex_ = hex_.replace("0x","")

	if (len(hex_) == 1 ):
		hex_ = '0' + str(hex_)

	hex_ = hex_.upper()

	hex_ = "INIT_" + hex_
	# print (hex_)
	return hex_

# pixel_to_hex(255)
reshaped_image = reshape_image(image)
hex_string_list = []
hex_string = ''
for element in reshaped_image : 
	hex_string = ''
	for pixel in element : 
		hex_string += pixel_to_binary(pixel)
	hex_string_list.append(hex_string)

# for element in reshaped_image : 
# 	print(element)

import numpy

for i in range(len(hex_string_list)) :
	element = hex_string_list[i] 
	# print(len(element))
	# print("256'd" + str(int(element,base=2)))
	print('.' + HEXA(i) + "(256'd" + str(int(element,base=2)) + ')')
	string = ''
	for j in range(16) :
		string = element[j*16:(j+1)*16] 
		# print(string)
		# print(int(string,base=2)>>11)


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

# pixel_to_hex(255)
reshaped_image = reshape_image(image)
hex_string_list = []
hex_string = ''
for element in reshaped_image : 
	hex_string = ''
	for pixel in element : 
		hex_string += pixel_to_binary(pixel)
	hex_string_list.append(hex_string)

for element in reshaped_image : 
	print(element)

for element in hex_string_list : 
	print(len(element))
	print("256'd" + str(int(element,base=2)))
	print

def integer_to_hex(integer) : 
	if(integer < 10) : 
		return '0' + str(integer) 
	else : 
		return '0' + chr(55 + integer)

def get_2_string(integer) : 
	return_string = ''
	return_string += integer_to_hex(integer)
	if(len(return_string) != 2) : 
		return_string = '0' + integer_to_hex(integer)
	return return_string

print(get_2_string(11))

print(integer_to_hex(15))

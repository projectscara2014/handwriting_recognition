import cv2
import numpy as np
import copy

# Main
COUNT = 1
var_array = []

class Variable:
	def __init__(self,num):
		self.value = num
		self.name = chr(num+48)
	# def __float__(self):
		# pass
		# return float(0)

def merge_labels(var1,var2):
	a = var1.value 
	b = var2.value
	if(a>b):
		var1.value = var2.value
	else:
		var2.value = var1.value

def show_var_array():
	global var_array
	l = []
	for instance in var_array:
		l.append(instance.value)
	print(l)

def show_var_names():
	global var_array
	l = []
	for instance in var_array:
		l.append(instance.name)
	print(l)

def var(i):
	global var_array
	return var_array[i]

def val(i):
	global var_array
	return var_array[i].value

def make_new_var():
	global COUNT 
	global var_array
	obj = Variable(COUNT)
	var_array.append(obj)
	COUNT = COUNT + 1

def rgb_to_bnw(image,threshold = 200,numpy_array = False) : 
    return_image = []
    for row in image : 
        return_image.append([])
        for pixel in row :
            try:
                [r,g,b,s] = pixel
            except ValueError:
                [r,g,b] = pixel
            magnitude= (int(r)+int(g)+int(b))/3
            if(magnitude < threshold) : 
                return_image[-1].append(255)
            else:
                return_image[-1].append(0)
    if(numpy_array):
        return np.array(return_image)
    else:
        return return_image

def destroyer(image):
	background = 0
	foreground = 1
	l_r_ = len(image)
	l_c_ = len(image[0])
	im2 = np.zeros((l_r_ + 2,l_c_ + 2))
	im2 [1:-1,1:-1] = image
	l_r = len(im2)
	l_c = len(im2[0])
	label = [] 
	for i in range(l_r):
		label.append([])
		for j in range(l_c):
			label[-1].append(background)
	make_new_var()
	for i in range(1,l_r-1):
		for j in range(1,l_c-1):
			# if pixel is not background
			label_value = background
			if (im2[i][j] != background):
				# check neighbours and their labels
				if (im2[i-1][j] != background or im2[i-1][j-1] != background or im2[i-1][j+1] != background or im2 [i][j-1] != background ):
					label_space = [label[i-1][j-1],label[i-1][j],label[i-1][j+1],label[i][j-1]]
					var_label_space = []
					for obj in label_space:
						if(type(obj).__name__ != "int"):
							if(obj not in var_label_space):
								var_label_space.append(obj)
					if(len(var_label_space)==1):
						label_value = var_label_space[0]
					else:
						merge_labels(var_label_space[0],var_label_space[1])
						label_value = var_label_space[0]
				else:
					label_value = var(-1)
					make_new_var()
			# if pixel is background
			else:
				label_value = background

			label[i][j] = label_value
	# for i in range(len(image)):
	# 	print im2[i]
	# print("---------------------------------")
	destroyer_image = []
	for i in range(len(label)):
		destroyer_image.append([])
		for j in range(len(label[i])):
			try:
				destroyer_image[-1].append(label[i][j].value)
			except:
				destroyer_image[-1].append(label[i][j])
	# print("---------------------------------")	
	# for i in range(len(label)):
	# 	for j in range(len(label[i])):
	# 		try:
	# 			print(label[i][j].name),
	# 		except:
	# 			print(label[i][j]),
	# 		print(" "),
	# 	print("\n")

	# for i in range(len(destroyer_image)):
	# 	print(destroyer_image[i])
	# print("---------------------------------")	
	
	return destroyer_image

def destroyer_image_properties(image):
	dict_space = []
	count_space = []
	for row in image:
		for pixel in row:
			if(pixel not in dict_space):
				dict_space.append(pixel)
				count_space.append(1)
			else:
				count_space[dict_space.index(pixel)] = count_space[dict_space.index(pixel)] + 1
	# Make 0 as first value
	count_space.insert(0,count_space.pop(dict_space.index(0)))
	dict_space.insert(0,dict_space.pop(dict_space.index(0)))
	print(dict_space)
	print(count_space)
	return [dict_space,count_space]

def show_color(image,dict_space):
	factor = 255/(((len(dict_space)-1)/7)+1)
	color_space = []
	for i in range(len(dict_space)):
		p = [(i/4)%2,(i/2)%2,i%2]
		for j in range(3):
			p[j] = factor*p[j]
		color_space.append(p)
	# print(color_space)
	for i in range(len(image)):
		for j in range(len(image[i])):
			image[i][j] = color_space[dict_space.index(image[i][j])]
	return image

def show_greyscale(image,dict_space):
	factor = 255/(len(dict_space)-1)
	color_space = [i*factor for i in range(len(dict_space))]
	# print(color_space)
	for i in range(len(image)):
		for j in range(len(image[i])):
			image[i][j] = color_space[dict_space.index(image[i][j])]
	return image

def main(image,output_type = "Number_array"):
	destroyer_image = destroyer(bnw_im)
	# for i in range(len(destroyer_image)):
	# 	print(destroyer_image[i])
	# print("---------------")
	[dict_space,count_space] = destroyer_image_properties(destroyer_image)
	if(output_type == "color"):
		destroyer_image = show_color(destroyer_image,dict_space)
	elif(output_type == "grey"):
		destroyer_image = show_greyscale(destroyer_image,dict_space)
	else:
		pass
	print("---------------")
	destroyer_image = np.array(destroyer_image)
	destroyer_image = destroyer_image[1:-1,1:-1]

	return destroyer_image


# im = [[1,1,0,1,1,1,0,1],[1,1,0,1,0,1,0,1],[1,1,1,1,0,0,0,1],[0,0,0,0,0,0,0,1],[1,1,1,1,0,1,0,1],[0,0,0,1,0,1,0,1],[1,1,1,1,0,0,0,1],[1,1,1,1,0,1,1,1]]
im = cv2.imread("test_og2.png")
bnw_im = rgb_to_bnw(im)
# cv2.imwrite("test_bnw.png",np.array(bnw_im))
return_im = main(bnw_im,output_type = "color")

for i in range(len(im)):
	for j in range(len(im[0])):
		im[i][j] = im[i][j]*255
# cv2.imwrite("test_original.png",np.array(im))
cv2.imwrite("test_dest.png",return_im)

show_var_array()
show_var_names()
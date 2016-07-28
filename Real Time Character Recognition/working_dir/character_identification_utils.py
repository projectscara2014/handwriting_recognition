"""
	This script is a "utils" script for character identification.
"""

import resize
import cv2
from classifier_python.classifier import classifier

dictionary = {
	62:"<",	63:">",	64:"{",	65:"}",	66:"(",	67:")",	68:"[",\
		69:"]",	70:"$",	71:"#",	72:"@",	73:"&",	74:"%",	75:"=",\
			76:"~",	77:";",	78:"?",	79:"pi"}

def get_letter(a):
	global dictionary
	# # a = name.split("_")
	# a = 7*int(a[1]) + int(a[2]) + 10
	if(a<10):
		b = str(a)
	elif(a>=10 and a<=35):
		b = chr(a + 87) 
	elif(a>=36 and a<=61):
		b = chr(a + 29)
	else:
		b = dictionary[a]
	return b

def identify(cropped_im):
	im = resize.main(cropped_im)
	character_code = classifier(im)
	l = get_letter(character_code)
	return l

def get_color_space(contours):
	try:
		factor = 255/(((len(contours)-1)/8)+1)
	except:
		factor = 255
	color_space = []
	count = 0
	current_factor = factor
	for i in range(len(contours)):
		p = [(count/4)%2,(count/2)%2,count%2]
		for j in range(3):
			p[j] = current_factor*p[j]
		color_space.append((p[0],p[1],p[2]))
		# print(p)
		count = count + 1
		if(count%8 == 0):
			count = 1
			current_factor = current_factor + factor
	return color_space
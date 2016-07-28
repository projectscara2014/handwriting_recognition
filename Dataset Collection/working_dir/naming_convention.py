"""
	This script manages the naming convention to be followed for naming of the files.
"""

def main(START_VALUE= 0):
	import os

	WORKING_DIRECTORY = os.getcwd()

	SOURCE_DIRECTORY = WORKING_DIRECTORY + "\source_folder"

	NO_OF_DIGITS = 5
	# START_VALUE = 0

	all_files = os.listdir(SOURCE_DIRECTORY)

	for file in all_files:
		split_name = file.split(".")
		if split_name[1] == "bmp":
			a = split_name[0].split("_")
			# based on scanner convention
			if(a[-1] == ""): a[-1] = '0'
			if(START_VALUE != 0):
				n = (int(a[-1]) + START_VALUE)
				p = []
				while(n!=0):
					p.append(n%10)
					n = n/10
				q = []
				for i in range(len(p)):
					q.append(chr(p[len(p)-i-1] + 48))
				a[-1] = "".join(q)
			a[-1] = "0"*(NO_OF_DIGITS-len(a[-1])) + a[-1]
			a = "_".join(a) + ".bmp"
			OLD_PATH = SOURCE_DIRECTORY + "\\" + file
			NEW_PATH = SOURCE_DIRECTORY + "\\" + a
			os.rename(OLD_PATH,NEW_PATH)

def main2(SOURCE_DIRECTORY,START_VALUE= 0):
	import os

	NO_OF_DIGITS = 5
	# START_VALUE = 0

	all_files = os.listdir(SOURCE_DIRECTORY)

	for file in all_files:
		split_name = file.split(".")
		if split_name[1] == "png":
			a = split_name[0].split("_")
			# based on scanner convention
			if(a[-1] == ""): a[-1] = '0'
			if(START_VALUE != 0):
				n = (int(a[-1]) + START_VALUE)
				p = []
				while(n!=0):
					p.append(n%10)
					n = n/10
				q = []
				for i in range(len(p)):
					q.append(chr(p[len(p)-i-1] + 48))
				a[-1] = "".join(q)
			a[-1] = "0"*(NO_OF_DIGITS-len(a[-1])) + a[-1]
			a = "_".join(a) + ".png"
			OLD_PATH = SOURCE_DIRECTORY + "\\" + file
			NEW_PATH = SOURCE_DIRECTORY + "\\" + a
			os.rename(OLD_PATH,NEW_PATH)
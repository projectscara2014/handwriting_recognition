"""
	This script takes individual scanned-images from the "source_folder" and crops out images of individual characters into "cropped_images_folder".
"""

import os
import crop_lines
import naming_convention

# naming_convention.main()
# naming_convention.main(14)  ## optional_start_value

WORKING_DIRECTORY = os.getcwd()

SOURCE_DIRECTORY = WORKING_DIRECTORY + "\source_folder"
CROP_LINES_DIRECTORY = WORKING_DIRECTORY + "\crop_lines_folder"
DONE_DIRECTORY = WORKING_DIRECTORY + "\done_folder"
CROPPED_IMAGE_DIRECTORY = WORKING_DIRECTORY + "\cropped_images_folder"
ERROR_DIRECTORY = WORKING_DIRECTORY + "\error_folder"

# for i in range(10):
# 	for j in range(7):
# 		os.makedirs(CROPPED_IMAGE_DIRECTORY + "\\" +str(i)+ "_" +str(j))

all_files = os.listdir(SOURCE_DIRECTORY)

print(all_files)

for file in all_files:
	split_name = file.split(".")
	if split_name[1] == "bmp":
		FILE_PATH = SOURCE_DIRECTORY +"\\" +file
		CROP_LINES_DESTINATION_PATH = CROP_LINES_DIRECTORY + "\\" + split_name[0] +"_crop_lines.png"
		CROPPING_INFO = [CROPPED_IMAGE_DIRECTORY,split_name[0]]
		try:
			crop_lines.main(FILE_PATH,CROP_LINES_DESTINATION_PATH,CROPPING_INFO)
		except:
			FILE_DESTINATION_PATH = ERROR_DIRECTORY + "\\" + file
		else:
			FILE_DESTINATION_PATH = DONE_DIRECTORY + "\\" + file
		os.rename(FILE_PATH,FILE_DESTINATION_PATH)
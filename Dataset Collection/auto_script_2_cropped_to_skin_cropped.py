import os
import ccl
import sys
WORKING_DIRECTORY = os.getcwd()

# CROPPED_IMAGE_DIRECTORY = WORKING_DIRECTORY + "\other\cropped_images_folder_Copy"
CROPPED_IMAGE_DIRECTORY = WORKING_DIRECTORY + "\cropped_images_folder"
SKIN_CROPPED_IMAGE_DIRECTORY = WORKING_DIRECTORY + "\skin_cropped_images_folder"
ERROR_DIRECTORY = WORKING_DIRECTORY + "\script2_folders\error_folder"
DONE_DIRECTORY = WORKING_DIRECTORY + "\script2_folders\done_folder"

# for i in range(10):
# 	for j in range(7):
# 		os.makedirs(SKIN_CROPPED_IMAGE_DIRECTORY + "\\" +str(i)+ "_" +str(j))

all_folders = os.listdir(CROPPED_IMAGE_DIRECTORY)

# all_folders = all_folders[34:]

for folder in all_folders:
	# print(folder)
	all_files = os.listdir(CROPPED_IMAGE_DIRECTORY + "\\" + folder)
	for file in all_files:
		IMAGE_PATH = CROPPED_IMAGE_DIRECTORY + "\\" + folder + "\\" + file
		DESTINATION_PATH = SKIN_CROPPED_IMAGE_DIRECTORY + "\\" + folder + "\\" + file
		# TEMP_PATH = WORKING_DIRECTORY + "\other\destroyer_outputs\\" + file

		print(file)
		# ccl.main(IMAGE_PATH,TEMP_PATH,output_type = "color")
		# ccl.main(IMAGE_PATH,DESTINATION_PATH,output_type = "color")
		if(file == "delete"):
			FILE_DESTINATION_PATH = ERROR_DIRECTORY + "\\" + file + "_" + folder
		else:
			try:
				# ccl.main(IMAGE_PATH,TEMP_PATH,output_type = "color")
				ccl.main(IMAGE_PATH,DESTINATION_PATH,output_type = "color")
			except:
				FILE_DESTINATION_PATH = ERROR_DIRECTORY + "\\" + file
			else:
				FILE_DESTINATION_PATH = DONE_DIRECTORY + "\\" + file
		os.rename(IMAGE_PATH,FILE_DESTINATION_PATH)
		# sys.exit(0)
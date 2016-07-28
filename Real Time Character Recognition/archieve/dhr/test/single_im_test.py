import numpy as np
import cv2
import lib_image_processing
import decision_maker
import character_identification_utils

def get_attributes(name,im):
    print(name)
    # print(len(im))
    # print(len(im[0]))
    try:
        print(len(im[0][0]))
    except:
        print(type(im[0][0]))
    else:
        print(type(im[0][0][0]))
    print("---------------------")

def get_color_space(contours):
    factor = 255/(((len(contours)-1)/8)+1)
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

def remove_children(hierarchy,global_parent = -1):
    return_list = []
    for i in range(len(hierarchy)):
        if(hierarchy[i][3] == global_parent):
            return_list.append(i)
    return return_list

# extra
kernel = np.ones((3,3),np.uint8)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
blank = cv2.imread("blank.png")

# original
original = cv2.imread('test_image_1.png')
get_attributes("original",original)

# bnw5
bnw5 = lib_image_processing.threshold3(original,120)
get_attributes("bnw5",bnw5)

# bnw3
bnw3 = lib_image_processing.threshold3(original,120)
get_attributes("bnw3",bnw3)

# bnw2
bnw2 = lib_image_processing.threshold2(original,120)
get_attributes("bnw2",bnw2)

cv2.imwrite("bnw.png",bnw2)
# bnw4
bnw4 = lib_image_processing.threshold2(original,120)
get_attributes("bnw4",bnw4)

# ccl1
im1, contours, hierarchy = cv2.findContours(bnw3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# modified_index_list = remove_children(hierarchy[0])
color_space = get_color_space(contours)
for i in range(len(contours)):
    # if i in modified_index_list:
    cv2.drawContours(bnw4,contours,i,color_space[i],-1)
get_attributes("ccl1",bnw4)
cv2.imwrite("ccl1.png",bnw4)

# dilation
dilation = cv2.dilate(bnw2, kernel , iterations = 2)
get_attributes("dilation",dilation)
cv2.imwrite("dilation.png",dilation)

# modified_dilation
modified_dilation = lib_image_processing.threshold3(dilation,10)
get_attributes("modified_dilation",modified_dilation)

# ccl2
im1, contours, hierarchy = cv2.findContours(modified_dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# final_contour_list = decision_maker.main(contours)

# find biggest parent
a = 0
parent_index = 0
contour_info_list = []
for i in range(len(contours)):
    [x,y,w,h] = cv2.boundingRect(contours[i])
    print(hierarchy[0][i])
    contour_info_list.append([x,y,w,h])
    if(w*h>a):
        a = w*h
        parent_index = i

print(parent_index)

# main color
main_index_list = []
for i in range(len(contours)):
    if(hierarchy[0][i][3] == parent_index):
        main_index_list.append(i)

print(main_index_list)

# child color
child_index_list = []
for i in range(len(contours)):
    if(hierarchy[0][i][3] in main_index_list):
        child_index_list.append(i)

print(child_index_list)

for i in range(len(contours)):
    [x,y,w,h] = contour_info_list[i]

    # # discard areas that are too big
    # if h>70 and w>70:
    #     print("")
    #     continue

    # # discard areas that are too small
    # if h<20 or w<20:
    #     print("")
    #     continue

    if i in main_index_list:
        cv2.drawContours(dilation,contours,i,color_space[i],-1)
    if i in child_index_list:
        cv2.drawContours(dilation,contours,i,(0,0,0),-1)

get_attributes("ccl2",dilation)
cv2.imwrite("ccl2.png",dilation)

# box
for i in main_index_list:
    [x,y,w,h] = contour_info_list[i]
    # print(color_space[i])
    cv2.rectangle(original,(x,y),(x+w,y+h),(0,0,255),1)
    # cv2.imwrite("contour" + contour , img)
cv2.imwrite("contoured.png", original) 

# put text
font = cv2.FONT_HERSHEY_SIMPLEX
for i in main_index_list:
    [x,y,w,h] = contour_info_list[i]
    cropped_im = bnw5[y:y+h,x:x+w]
    return_val = character_identification_utils.identify(cropped_im)
    cv2.putText(original,return_val,(x,y), font, 0.8,(255,0,0),2,cv2.LINE_AA)

cv2.imwrite("output.png", original)

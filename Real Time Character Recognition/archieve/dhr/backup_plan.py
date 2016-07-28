import cv2 
import time

image = cv2.imread("test_image_1.png")
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))

start_time = time.time()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

stop_time = time.time()
print (stop_time - start_time)
start_time = time.time()

_,thresh = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY_INV)
# cv2.imwrite("gray.png", thresh)

stop_time = time.time()
print (stop_time - start_time)
start_time = time.time()

dilated =cv2.dilate(thresh,kernel,iterations = 3)
# cv2.imwrite("dilated.png", dilated)

stop_time = time.time()
print (stop_time - start_time)
start_time = time.time()

image_1, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# _,thresh = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)
print(len(contours))

stop_time = time.time()
print (stop_time - start_time)
start_time = time.time()

bnw = cv2.imwrite("bnw.png", image)
# bnw = cv2.imread("bnw.png")
for contour in contours:
    # get rectangle bounding contour
    [x,y,w,h] = cv2.boundingRect(contour)

    # discard areas that are too large
    if h>70 and w>70:
        continue

    # discard areas that are too small
    if h<20 or w<20:
        continue

    # draw rectangle around contour on original image
    img = cv2.rectangle(gray,(x-2,y-2),(x+w,y+h),(255,0,255),1)
    # cv2.imwrite("contour" + contour , img)
# write original image with added contours to disk 
stop_time = time.time()
print (stop_time - start_time)
cv2.imwrite("contoured.png", img)
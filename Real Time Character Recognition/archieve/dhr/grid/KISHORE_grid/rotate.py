import cv2
import math
from scipy import ndimage

im = cv2.imread('square.png')

a = [191,160]
b = [346,145]

slope = (b[1]-a[1])*1.0/(b[0]-a[0])
angle = math.degrees(math.atan(slope))
print(angle)

rotated_image = ndimage.rotate(im,angle)

cv2.imwrite("rotated_square.png",rotated_image)
# -*- coding: utf-8 -*-
"""pothole.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I92-iQxctsN8iJplokqQUCMi-41ZnIBG
"""

import numpy as np
import cv2 as cv
from google.colab.patches import cv2_imshow

img = cv.imread("road1.jpeg")
gimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

height = img.shape[0]
width = img.shape[1]

# blur based on size of image, tricky bc image gets darker with smaller kernel
kernel = np.ones((6,6),np.float32)/25
bimg = cv.filter2D(gimg,-1,kernel)

cv2_imshow(bimg)
cv.waitKey(0)

print(height, width)

average_color_row = np.average(bimg, axis=0)
average_color = np.average(average_color_row, axis=0)
print(average_color)

# timg = cv.adaptiveThreshold(bimg,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,41,2)

# thresh determined by the lighting of image - maybe do above and below avg - small: 110 -> 90 - large: 144 -> 130
ret, timg = cv.threshold(bimg,average_color-20,255,cv.THRESH_BINARY_INV)
# inv determined by whether it rained or not lol othole is lighter or darker than surrounding road

cv2_imshow(timg)
cv.waitKey(0)

contours, hierarchy = cv.findContours(image=timg, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)
cdimg = gimg.copy()
# cdimg = cv.imread("white.jpeg")

cv.drawContours(cdimg, contours, -1, (255,255,255), -1)

cv2_imshow(cdimg)
cv.waitKey(0)

cdimg2 = gimg.copy()

# area bounds based on size of image and perspective - large: 20000, 100000 - small: 1000, 5000
contours_area = []
for con in contours:
    area = cv.contourArea(con)
    if 20000 < area < 100000:
        contours_area.append(con)

cv.drawContours(cdimg2, contours_area, -1, (255,255,255), -1)

cv2_imshow(cdimg2)
cv.waitKey(0)

cdimg3 = gimg.copy()

new_contours = []
for con in contours_area:
  x,y,w,h = cv.boundingRect(con)
  if x != 0 and y != 0 and x+w != width and y+h != height:
    new_contours.append(con)
    cv.rectangle(cdimg3, (x, y), (x+w, y+h), (255,0,0), 4)
    print("do be hole")

# if height of hole is greater than percent height of image

cv.drawContours(cdimg3, new_contours, -1, (255,255,255), -1)

cv2_imshow(cdimg3)
cv.waitKey(0)
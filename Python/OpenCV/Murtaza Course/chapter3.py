# CHAPTER 3 : RESIZING AND CROPPING

import cv2
import numpy as np

img = cv2.imread("Ressources/lambo.png")
print(img.shape)

img_resized = cv2.resize(img, (300, 200))
print(img_resized.shape)

img_cropped = img[0:200, 200:500]

cv2.imshow("Image", img)
# cv2.imshow("Resized Image", img_resized)
cv2.imshow("Cropped Image", img_cropped)
cv2.waitKey(0)
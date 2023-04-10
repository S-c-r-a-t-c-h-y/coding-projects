# CHAPTER 6 : IMAGE STACKING (JOINING IMAGES)

import cv2
import numpy as np
from useful_functions import stack_images

img = cv2.imread("Ressources/sample_image.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_stack = stack_images(0.5, ([img, img_gray, img], [img, img, img]))

# img_hor = np.hstack((img, img))
# img_ver = np.vstack((img, img))

# cv2.imshow("Horizontal Image", img_hor)
# cv2.imshow("Vertical Image", img_ver)

cv2.imshow("Stacked Image", img_stack)

cv2.waitKey(0)
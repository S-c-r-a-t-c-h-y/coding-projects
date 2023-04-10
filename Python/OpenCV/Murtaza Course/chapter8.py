# CHAPTER 8 : CONTOURS / SHAPE DETECTION

import cv2
import numpy as np
from useful_functions import stack_images, draw_contours

path = "Ressources/shapes.png"

img = cv2.imread(path)
img_contour = img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (7, 7), 1)
img_canny = cv2.Canny(img_blur, 50, 50)
draw_contours(img_canny, img_contour)

img_blank = np.zeros_like(img)
img_stack = stack_images(0.6, ([img, img_gray, img_blur],
                               [img_canny, img_contour, img_blank]))

cv2.imshow("Images", img_stack)
cv2.waitKey(0)
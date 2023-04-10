# CHAPTER 4 : ADDING SHAPES AND TEXT TO AN IMAGE

import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)

# print(img.shape)
# img[:] = 255, 0, 0

# cv2.line(img, (0, 0), (300, 300), (0, 255, 0), 3)
cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)

cv2.rectangle(img, (100, 100), (400, 300), (0, 0, 255), 2)
# cv2.rectangle(img, (100, 100), (400, 300), (0, 0, 255), cv2.FILLED)

cv2.circle(img, (300, 50), 30, (255, 255, 0), 5)

cv2.putText(img, "Sample text", (300, 150), cv2.FONT_HERSHEY_COMPLEX, .8, (255, 255, 255), 2)

cv2.imshow("Image", img)
cv2.waitKey(0)
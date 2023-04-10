# CHAPTER 1 : READ IMAGES, VIDEOS AND WEBCAM

import cv2

# ----------------------------------------------------------
# img = cv2.imread("Ressources/sample_image.png")

# cv2.imshow("Output", img)
# cv2.waitKey(0)
# ----------------------------------------------------------


# ----------------------------------------------------------
# cap = cv2.VideoCapture("Ressources/test_video.mp4")

# while 1:
#     success, img = cap.read()
#     cv2.imshow("Video", img)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# ----------------------------------------------------------


# ----------------------------------------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

while 1:
    success, img = cap.read()
    cv2.imshow("Video", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# ----------------------------------------------------------
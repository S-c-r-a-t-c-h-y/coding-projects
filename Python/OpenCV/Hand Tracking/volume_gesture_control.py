import cv2
import numpy as np
import hand_tracking_module as htm
import time
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

user32 = ctypes.windll.user32

WIDTH, HEIGHT = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

detector = htm.hand_detector(max_hands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
min_vol = volRange[0]
max_vol = volRange[1]
vol = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.find_hands(img, draw=True)
    lm_list = detector.find_position(img, draw=True)

    if len(lm_list) != 0:
        length, img, _ = detector.find_distance(img, 4, 8)
        vol = np.interp(length, [50, 300], [min_vol, max_vol])

        volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow("Image", img)
    if cv2.waitKey(5) & 0xFF == ord("s"):
        break

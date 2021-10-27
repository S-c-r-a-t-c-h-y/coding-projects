import cv2
import numpy as np
import hand_tracking_module as htm
import time
import ctypes
import screeninfo

user32 = ctypes.windll.user32


def get_screen_metrics():
    screens = screeninfo.get_monitors()

    min_x = float("+inf")
    min_y = float("+inf")

    max_x = float("-inf")
    max_y = float("-inf")

    for screen in screens:
        min_x = min(min_x, screen.x)
        min_y = min(min_y, screen.y)

        max_x = max(max_x, (screen.x + screen.width))
        max_y = max(max_y, (screen.y + screen.height))

    return min_x, max_x, min_y, max_y


min_x, max_x, min_y, max_y = get_screen_metrics()
print(min_x, max_x, min_y, max_y)

OFFSET = 40

p_time = 0
c_time = 0

WIDTH, HEIGHT = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

# WIDTH, HEIGHT = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

detector = htm.hand_detector(max_hands=1)

try:
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.find_hands(img, draw=True)
        lm_list = detector.find_position(img, draw=True)

        # c_time = time.time()
        # fps = 1 / (c_time - p_time)
        # p_time = c_time

        if len(lm_list) != 0:
            index_finger_tip = lm_list[8]
            # print(index_finger_tip[1], index_finger_tip[2], WIDTH, HEIGHT)
            x1 = int(np.interp(index_finger_tip[1], (0, WIDTH), (min_x - OFFSET, max_x + OFFSET)))
            y1 = int(np.interp(index_finger_tip[2], (0, HEIGHT), (min_y - OFFSET, max_y + OFFSET)))

            # https://docs.microsoft.com/fr-fr/windows/win32/api/winuser/nf-winuser-mouse_event?redirectedfrom=MSDN
            if detector.finger_is_up(img, 0, 2):
                # user32.mouse_event(2, 0, 0, 0, 0)
                pass
            else:
                user32.mouse_event(4, 0, 0, 0, 0)
            user32.SetCursorPos(x1, y1)

        # cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(5) & 0xFF == ord("s"):
            break

except KeyboardInterrupt:
    pass

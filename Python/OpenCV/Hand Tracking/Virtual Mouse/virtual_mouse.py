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
# print(min_x, max_x, min_y, max_y)

OFFSET = 100

p_time = 0
c_time = 0

WIDTH, HEIGHT = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

SMOOTHENING = 4
plocX, plocY = 0, 0
clocX, clocY = 0, 0


detector = htm.hand_detector(max_hands=1, track_con=0.25, model_complexity=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.find_hands(img, draw=True)
    lm_list = detector.find_position(img, draw=True)

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    if len(lm_list) != 0:
        index_finger_tip = lm_list[8]
        cv2.circle(img, tuple(map(int, index_finger_tip[1:])), 10, (0, 255, 0), cv2.FILLED)

        x1 = np.interp(index_finger_tip[1], (OFFSET, WIDTH - OFFSET), (min_x, max_x))
        y1 = np.interp(index_finger_tip[2], (OFFSET, HEIGHT - OFFSET), (min_y, max_y))

        clocX = plocX + (x1 - plocX) / SMOOTHENING
        clocY = plocY + (y1 - plocY) / SMOOTHENING

        plocX, plocY = clocX, clocY

        # https://docs.microsoft.com/fr-fr/windows/win32/api/winuser/nf-winuser-mouse_event?redirectedfrom=MSDN
        straight, img = detector.finger_is_straight(img, 2, draw=False)
        if straight:
            length, img, _ = detector.find_distance(img, 8, 12)
            if length < 40:
                user32.mouse_event(2, 0, 0, 0, 0)
                time.sleep(0.01)
                user32.mouse_event(4, 0, 0, 0, 0)
                time.sleep(0.1)
        else:
            user32.SetCursorPos(int(clocX), int(clocY))

    cv2.putText(img, str(int(fps)), (10, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
    cv2.putText(img, "Press 's' to exit.", (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    cv2.rectangle(img, (OFFSET, OFFSET), (WIDTH - OFFSET, HEIGHT - OFFSET), (255, 0, 255), 2)
    cv2.imshow("Virtual Mouse", img)

    if cv2.waitKey(5) & 0xFF == ord("s"):
        break

"""
Hand tracking Module
"""

from typing import List
import cv2
import mediapipe as mp
import time
import math


class hand_detector:
    def __init__(
        self,
        mode: bool = False,
        max_hands: int = 2,
        model_complexity: int = 1,
        detection_con: float = 0.5,
        track_con: float = 0.5,
    ) -> None:
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        self.model_complexity = model_complexity

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            self.mode,
            self.max_hands,
            self.model_complexity,
            self.detection_con,
            self.track_con,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw: bool = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no: int = 0, draw: bool = True) -> List[List[int]]:

        self.lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        return self.lmlist

    def finger_is_up(self, img, finger_no: int = 1, hand_no: int = 0, treshold: int = 10) -> bool:
        """Returns True if the finger n°finger_no from the hand n°hand_no is up
        (0=thumb, 1=index finger, 2=middle finger, 3=ring_finger, 4=pinky)
        otherwise returns False.
        The treshold value is the minimum amount of vertical distance required
        between the parts of the finger to count as being up and not down.
        """

        self.find_position(img, hand_no, draw=False)

        if self.lmlist:
            finger = self.lmlist[(finger_no * 4 + 1) : (finger_no * 4 + 5)]
            positions = (mcp, pip, dip, tip) = [(x, y) for _, x, y in finger]

            for i in range(1, 4):
                if abs(positions[i][1] - positions[i - 1][1]) < treshold:
                    return False

            return tip[1] < dip[1] < pip[1] < mcp[1]
        else:
            return False

    def fingers_up(self, img, hand_no: int = 0, treshold: int = 10) -> List[bool]:
        """
        Returns a list of boolean values representing each finger and there state (up or down) on the hand n°hand_no.
        """
        return [self.finger_is_up(img, i, hand_no, treshold) for i in range(5)]

    def find_distance(self, img, joint1: int, joint2: int, draw: bool = True, hand_no: int = 0):

        self.find_position(img, hand_no, draw=draw)

        x1, y1 = self.lmlist[joint1][1:]
        x2, y2 = self.lmlist[joint2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            r, t = 10, 3
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

    def finger_is_straight(self, img, finger_no: int, hand_no: int = 0, treshold: float = 8.0, draw: bool = True):
        """Returns whether or not the finger n°finger_no of the hand n°hand_no
        is straight. The higher the treshold the "less straight" the finger
        needs to be to return True"""

        self.find_position(img, hand_no, draw=draw)

        finger_points = [(x, y) for _, x, y in self.lmlist[(finger_no * 4 + 1) : (finger_no * 4 + 5)]]

        a1, b1 = get_tendancy_curve(
            [finger_points[0][0], finger_points[1][0]], [finger_points[0][1], finger_points[1][1]]
        )
        a2, b2 = get_tendancy_curve(
            [finger_points[0][0], finger_points[3][0]], [finger_points[0][1], finger_points[3][1]]
        )

        if draw:
            x1, y1 = 0, int(b1)
            x2, y2 = int(img.shape[0] * 100), int(a1 * img.shape[0] * 100 + b1)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            x1, y1 = 0, int(b2)
            x2, y2 = int(img.shape[0] * 100), int(a2 * img.shape[0] * 100 + b2)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        angle1 = math.degrees(math.atan(-a1))
        angle2 = math.degrees(math.atan(-a2))

        return abs(angle1 - angle2) < treshold, img


def get_tendancy_curve(x_values, y_values):
    """Returns the tendancy curve of a set of points of coords
    x_values[n], y_values[n]"""

    n = len(x_values)
    try:
        a = (sum(x * y for x, y in zip(x_values, y_values)) - (sum(x_values) * sum(y_values) / n)) / (
            sum(x ** 2 for x in x_values) - (sum(x_values) ** 2) / n
        )
        b = sum(y_values) / n - a * (sum(x_values) / n)
    except ZeroDivisionError:
        a, b = 0, 0

    return a, b


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = hand_detector()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.find_hands(img)
        lmlist = detector.find_position(img)
        if len(lmlist) != 0:
            print(lmlist[8])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()

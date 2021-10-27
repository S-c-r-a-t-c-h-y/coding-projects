"""
Hand tracking Module
Name: Syed
"""

from typing import List
import cv2
import mediapipe as mp
import time


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

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        return lmlist

    def finger_is_up(self, img, hand_no: int = 0, finger_no: int = 1, treshold: int = 10) -> bool:
        """Returns True if the finger n°finger_no from the hand n°hand_no is up
        (0=thumb, 1=index finger, 2=middle finger, 3=ring_finger, 4=pinky)
        otherwise returns False.
        The treshold value is the minimum amount of vertical distance required
        between the parts of the finger to count as being up and not down.
        """

        finger_positions = self.find_position(img, hand_no, draw=False)
        if finger_positions:
            finger = finger_positions[(finger_no * 4 + 1) : (finger_no * 4 + 5)]
            positions = (mcp, pip, dip, tip) = [(x, y) for _, x, y in finger]

            for i in range(1, 4):
                if abs(positions[i][1] - positions[i - 1][1]) < treshold:
                    return False

            return tip[1] < dip[1] < pip[1] < mcp[1]
        else:
            return False

    def nb_finger_up(self, img, hand_no: int = 0, treshold: int = 10) -> int:
        """
        Returns the number of fingers that are up on the hand n°hand_no.
        """
        return [self.finger_is_up(img, hand_no, i, treshold) for i in range(5)].count(True)


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

import pyautogui
import cv2
from mss import mss
import numpy as np


def start_capture(recording=False, resolution=(1920, 1080), filename="__recording.avi", fps=12.0):

    if recording:
        codec = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(filename, codec, fps, resolution)

    sct = mss()

    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Live", resolution[0] // 2, resolution[1] // 2)

    bounding_box = {"top": 0, "left": 0, "width": resolution[0], "height": resolution[1]}

    while True:
        sct_img = sct.grab(bounding_box)

        frame = np.array(sct_img)

        if recording:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
            out.write(frame)

        cv2.imshow("Live", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    if recording:
        out.release()

    cv2.destroyAllWindows()


def stream_capture(resolution=(1920, 1080), preview=False):

    if preview:
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Live", resolution[0] // 2, resolution[1] // 2)

    sct = mss()
    bounding_box = {"top": 0, "left": 0, "width": resolution[0], "height": resolution[1]}

    while True:
        sct_img = sct.grab(bounding_box)

        frame = np.array(sct_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        yield frame

        if preview:
            cv2.imshow("Live", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


class ScreenRecorder:
    def __init__(self, resolution=(1920, 1080), to_bytes=False, preview=False):
        self.RESOLUTION = resolution
        self.PREVIEW = preview
        self.TO_BYTES = to_bytes

        self.BOUNDING_BOX = {"top": 0, "left": 0, "width": resolution[0], "height": resolution[1]}

        if preview:
            cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Live", resolution[0] // 2, resolution[1] // 2)

    def __iter__(self):
        self.sct = mss()
        return self

    def __next__(self):
        sct_img = self.sct.grab(self.BOUNDING_BOX)

        frame = np.array(sct_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        if self.PREVIEW:
            cv2.imshow("Live", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                raise StopIteration

        return frame.tobytes() if self.TO_BYTES else frame


if __name__ == "__main__":

    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Live", 1920 // 2, 1080 // 2)

    for frame in stream_capture():
        cv2.imshow("Live", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

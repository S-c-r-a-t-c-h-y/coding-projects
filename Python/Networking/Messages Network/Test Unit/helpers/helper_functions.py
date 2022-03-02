from .constants import *

import os
import re
import socket
import datetime
import io
from PIL import Image

from github import Github

# for the screen capture
import cv2
from mss import mss
import numpy as np


def encapsulate(data: bytes, header: bytes, fill_car: str = " ", capsule_size=CAPSULE_SIZE) -> bytes:
    while len(header) != capsule_size:
        header += bytes(fill_car, ENCODING)
    return header + data


def decapsulate(data: bytes, capsule_size=CAPSULE_SIZE) -> tuple[bytes, bytes]:
    return data[:CAPSULE_SIZE], data[capsule_size:]


def get_ip_addresses():
    """Returns a list of all the ip adresses of the local network"""
    addresses = []
    for device in os.popen("arp -a"):
        device = re.search("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", device, re.M | re.I)
        if device is not None:
            addresses.append(device.group(0))
    return addresses


def get_servers(port, timeout=0.5):
    """Returns a list of all servers you can connect to.
    A shorter timeout value can reduce the operation time but may cause some available servers to be forgotten."""

    available = []

    for ip in get_ip_addresses():

        s = socket.socket()
        s.settimeout(timeout)
        try:
            s.connect((ip, port))
        except (ConnectionRefusedError, OSError):
            continue
        except socket.timeout:
            continue

        available.append(ip)

    return available


def get_time():
    """Returns the current time as such: HH:MM"""
    return datetime.datetime.now().strftime("%H:%M")


def get_full_time():
    """Returns the current date and time as such: DD/MM/YYYY, HH:MM"""
    return datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")


def array_to_bytes(x: np.ndarray) -> bytes:
    """Converts a numpy array to bytes."""
    np_bytes = io.BytesIO()
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()


def bytes_to_array(b: bytes) -> np.ndarray:
    """Converts bytes to a numpy array."""
    np_bytes = io.BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)


def constrain_image(img_path: str, new_path: str = "", max_width: int = MAX_IMG_WIDTH, max_height: int = MAX_IMG_HEIGHT) -> None:
    new_path = new_path or img_path

    img = Image.open(img_path)
    width, height = img.size

    if width <= max_width and height <= max_height:
        ratio = 1
    else:
        ratio = min(max_width / width, max_height / height)

    new_width, new_height = int(width * ratio), int(height * ratio)

    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    img.save(new_path, img.format)


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

        return array_to_bytes(frame) if self.TO_BYTES else frame


def push_to_github(token: str, github_file_name: str, local_file_name: str, repo_name: str = "S-c-r-a-t-c-h-y/MessageNetworkData"):
    g = Github(token)

    with open(local_file_name, "r") as f:
        content = "".join(f.readlines())

    # user = g.get_user()
    repo = g.search_repositories(repo_name)[0]

    if is_in_repo := any(content.path == github_file_name for content in repo.get_contents("")):
        contents = repo.get_contents(github_file_name)
        repo.update_file(contents.path, "autocommit", content, contents.sha)
    else:
        repo.create_file(github_file_name, "autocommit", content)

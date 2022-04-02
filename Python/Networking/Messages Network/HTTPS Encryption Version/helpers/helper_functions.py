from .constants import *

import os
import re
import socket
import datetime
import io
from itertools import cycle
import random
import string
from math import sqrt

# for the screen capture
import cv2
from mss import mss
import numpy as np

from typing import Tuple


def encapsulate(data: bytes, header: bytes, fill_car: str = " ", capsule_size=CAPSULE_SIZE) -> bytes:
    while len(header) != capsule_size:
        header += bytes(fill_car, ENCODING)
    return header + data


def decapsulate(data: bytes, capsule_size=CAPSULE_SIZE) -> Tuple[bytes, bytes]:
    return data[:CAPSULE_SIZE], data[capsule_size:]


def byte_xor(data: bytes, key: bytes) -> bytes:
    return bytes(_a ^ _b for _a, _b in zip(data, cycle(key)))


def encode_xor_key(xor_key: bytes, rsa_key: str) -> str:
    key = xor_key.decode(ENCODING)
    e, n = rsa_key.split(",")
    return " ".join(str((ord(car) ** int(e)) % int(n)) for car in key)


def decode_xor_key(encoded_key: str, e: int, n: int) -> str:
    return "".join(chr((int(car) ** e) % n) for car in encoded_key.split(" "))


def generate_random_xor_key(length: int = 100) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))


def generate_random_rsa(prime_min: int = 100, prime_max: int = 1000) -> Tuple[int, int, int]:
    """generates a random rsa key pair (e, d, n)"""

    def random_prime(min_prime=0, max_prime=1000):
        def is_prime(n):
            return False if n < 2 else all(n % i != 0 for i in range(2, int(sqrt(n)) + 1))

        return random.choice([i for i in range(min_prime, max_prime + 1) if is_prime(i)])

    def pgcd(a, b):
        return max(a, b) if 0 in {a, b} else pgcd(b, a % b)

    def mod_inverse(x, m):
        def eucl(a, b):
            if b == 0:
                return a, 1, 0
            d, u, v = eucl(b, a % b)
            return d, v, u - (a // b) * v

        return eucl(x, m)[1] % m

    def phi(p, q):
        return (p - 1) * (q - 1)

    d = e = n = 1

    while (((1000 ** e) % n) ** d) % n != 1000:
        p, q = random_prime(prime_min, prime_max), random_prime(prime_min, prime_max)

        n = p * q
        phi_n = phi(p, q)

        for i in range(max(p, q) + 1, phi_n):
            if pgcd(i, phi_n) == 1:
                e = i
                break

        d = mod_inverse(e, phi_n)
    return e, d, n


def get_ip_addresses():
    """Returns a list of all the ip adresses of the local network"""
    addresses = []
    for device in os.popen("arp -a"):
        device = re.search("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", device, re.M | re.I)
        if device is not None:
            addresses.append(device.group(0))
    addresses.append("127.0.0.1")  # adds localhost
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

import cv2

INVALID_PASSWORD = "Invalid password."
BANNED_MESSAGE = "Connection to the server impossible, you are banned from the chat."

DEFAULT_SERVER_MSG = "No servers available. Try scanning for servers."

DEFAULT_PORT = 8008

ENCODING = "utf-16le"
ENCODING_ERROR_TYPE = "backslashreplace"
VIDEO_CODEC = cv2.VideoWriter_fourcc(*"XVID")

MSG_DATATYPE = "1"
IMG_STREAM_DATATYPE = "2"
STREAM_END_DATATYPE = "3"

CAPSULE_SIZE = 500
NAME_MAX_LENGTH = 100

START_STREAM_UI_MSG = "Start Stream"
STOP_STREAM_UI_MSG = "Stop Stream"

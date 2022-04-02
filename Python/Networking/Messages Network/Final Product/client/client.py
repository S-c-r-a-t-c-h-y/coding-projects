from helpers import *
import threading
import socket
import cv2

from PyQt5.QtWidgets import QMessageBox


class Client:
    def __init__(self, ui, host_address: str, host_port: int, name: str, password: str, chat, debug: bool = False):
        self.debug = debug
        self.alive = True

        self.host_address = host_address
        self.host_port = host_port
        self.username = name
        self.chat = chat
        self.ui = ui

        self.password = password or " "

        self.closed_streams = []
        self.stream_windows = {}
        self.streaming = False
        self.streamcount = 0

        self.accepted = False

        self.message_thread = threading.Thread(target=self.message_reception_thread, daemon=True)

        self.establish_client_connection()

    def establish_client_connection(self):
        try:
            self.denied = False
            self.client = socket.create_connection((self.host_address, self.host_port))

            if (response := self.client.recv(1024).decode(ENCODING)) == "1":  # server has a password
                self.client.send(self.password.encode(ENCODING, ENCODING_ERROR_TYPE))
                self.chat.print_to_chat(response := self.client.recv(1024).decode(ENCODING))
                if response == INVALID_PASSWORD:
                    self.close_chat()
                    self.ui.show_popup(
                        "Error !",
                        f"Your access to the following server : {self.host_address}:{self.host_port} has been denied due to an invalid password.",
                        icon=QMessageBox.Warning,
                    )

            elif response == BANNED_MESSAGE:
                self.close_chat()
                self.ui.show_popup(
                    "Error !",
                    f"Your access to the following server : {self.host_address}:{self.host_port} has been denied because you are banned from this server.",
                    icon=QMessageBox.Critical,
                )

            self.client.send(self.username.encode(ENCODING, ENCODING_ERROR_TYPE))
            self.username = self.client.recv(1024).decode(ENCODING)

            self.ui.show_popup("Success !", f"You successfully connected to the following server : {self.host_address}:{self.host_port}", icon=QMessageBox.Information)

            self.message_thread.start()

        except socket.error as e:
            self.chat.print_to_chat(e)
        # self.chat.print_to_chat()

    def message_reception_thread(self):
        self.accepted = True

        while self.client.fileno() != -1:
            try:
                header, res = decapsulate(self.client.recv(10_000_000))
                header = header.decode(ENCODING).strip()

                data_type = header.split(" ")[0]

                if data_type == MSG_DATATYPE:
                    self.chat.print_to_chat(res.decode(ENCODING))

                elif data_type == IMG_STREAM_DATATYPE:
                    frame = bytes_to_array(res)
                    streamer, id = header.split(" ")[1], header.split(" ")[2]

                    self.stream_windows[streamer] = f"{streamer} - press 'q' to close the stream"

                    if f"{streamer}{id}" not in self.closed_streams:
                        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) == 0:
                            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                            cv2.resizeWindow(window_name, 1920 // 2, 1080 // 2)

                        cv2.imshow(window_name, frame)
                        if cv2.waitKey(1) & 0xFF == ord("q"):
                            self.closed_streams.append(f"{streamer}{id}")
                            cv2.destroyWindow(window_name)

                elif data_type == STREAM_END_DATATYPE:
                    cv2.destroyWindow(f"{res.decode(ENCODING)} - press 'q' to close the stream")

            except ConnectionError:
                self.close_chat()
                self.alive = False
                break

            except Exception as e:
                if self.debug:
                    self.chat.print_to_chat(e)
                continue

    def handle_input(self, inp: str):
        """Callback called every time an keyboard input is sent that evaluates that input
        and does actions accordingly."""

        if inp == "!leave":
            self.client.close()
            self.close_chat()
            return

        try:
            header = bytes(MSG_DATATYPE, ENCODING, ENCODING_ERROR_TYPE)
            msg = str.encode(inp, ENCODING, ENCODING_ERROR_TYPE)
            self.client.send(encapsulate(msg, header))

        except (ConnectionError, OSError):
            pass

    def stream(self):
        self.streaming = True
        self.streamcount += 1

        for frame in ScreenRecorder(to_bytes=True):
            if self.streaming:
                header = f"{IMG_STREAM_DATATYPE} {self.username} {self.streamcount}"
                header = bytes(header, ENCODING, ENCODING_ERROR_TYPE)
                frame = encapsulate(frame, header)
                try:
                    self.client.send(frame)
                except ConnectionError:
                    self.streaming = False
                    break
            else:
                break

    def start_stream(self):
        threading.Thread(target=self.stream, daemon=True).start()
        self.ui.show_popup("Stream info", "You started streaming !", icon=QMessageBox.Information)

    def stop_stream(self):
        self.streaming = False

        header = bytes(STREAM_END_DATATYPE, ENCODING, ENCODING_ERROR_TYPE)
        self.client.send(encapsulate(b"", header))

        self.ui.show_popup("Stream info", "You stopped streaming !", icon=QMessageBox.Information)

    def close_chat(self):
        self.chat.setParent(None)
        self.ui.tab_widget.setCurrentIndex(0)

    def is_alive(self):
        return self.alive

from helpers import *
import threading
import socket
import cv2
import os

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt


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
                    self.receive_stream(res, header)

                elif data_type == STREAM_END_DATATYPE:
                    cv2.destroyWindow(res.decode(ENCODING))

                elif data_type == IMAGE_DATATYPE:
                    self.receive_image(res, header)

            except ConnectionError:
                self.close_chat()
                self.alive = False
                break

            except Exception as e:
                if self.debug:
                    self.chat.print_to_chat(e)
                continue

    def receive_stream(self, res: bytes, header: str):
        frame = bytes_to_array(res)
        streamer, id = header.split(" ")[1], header.split(" ")[2]

        if f"{streamer}{id}" not in self.closed_streams:
            if cv2.getWindowProperty(streamer, cv2.WND_PROP_VISIBLE) == 0:
                cv2.namedWindow(streamer, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(streamer, 1920 // 2, 1080 // 2)

            cv2.imshow(streamer, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.closed_streams.append(f"{streamer}{id}")
                cv2.destroyWindow(streamer)

    def receive_image(self, res: bytes, header: str):
        name = header.split(" ")[1]
        filename = " ".join(header.split(" ")[2:])

        file_name = f"{name}_{filename.split('/')[-1]}"
        folder_name = f"{os.sep}".join(os.path.abspath(__file__).split(os.sep)[:-2])

        img_path = os.path.join(folder_name, "data", file_name)

        with open(img_path, "ab") as f:
            f.write(res)

        constrain_image(img_path)

        # self.chat.print_to_chat(f'<strong>{get_time()} - <font color=blue>{name}</font></strong><br><img src="{img_path}">')
        self.chat.print_to_chat(f"<strong>{get_time()} - <font color=blue>{name}</font></strong><br>")
        # self.chat.insert_image(img_path)
        self.chat.print_to_chat(f"<img src='{img_path}'>")

        os.remove(img_path)

    def handle_input(self, inp: str) -> None:
        """Callback called every time an keyboard input is sent that evaluates that input
        and does actions accordingly."""

        if inp == "!leave":
            self.client.close()
            self.close_chat()
            return

        elif inp == "!stream":
            if self.streaming:
                self.chat.print_to_chat("You are already streaming, close old stream with !stopstream to start a new one.")
            else:
                self.chat.print_to_chat("Stream started.")
                threading.Thread(target=self.stream, daemon=True).start()
            return

        elif inp == "!stopstream":
            self.stopstream()
            return

        try:
            header = bytes(MSG_DATATYPE, ENCODING, ENCODING_ERROR_TYPE)
            msg = str.encode(inp, ENCODING, ENCODING_ERROR_TYPE)
            self.client.send(encapsulate(msg, header))

        except (ConnectionError, OSError):
            pass

    def send_file(self, filename: str, filter: str) -> None:
        with open(filename, "rb") as f:
            if filter == IMAGES_FILTER:
                header = f"{IMAGE_DATATYPE} {self.username} {filename}"

                folder_name = f"{os.sep}".join(os.path.abspath(__file__).split(os.sep)[:-2])
                file_name = f"{filename.split('/')[-1]}"
                img_path = os.path.join(folder_name, "data", file_name)

                constrain_image(filename, img_path)
                self.chat.print_to_chat(f"<strong><font color=purple>you</font> - {get_time()}</strong><br>", Qt.AlignRight)
                self.chat.print_to_chat(f"<img src='{img_path}'>")
                # self.chat.print_to_chat(f"<img src='{img_path}'>", Qt.AlignRight)
                # self.chat.insert_image(img_path)
                os.remove(img_path)

            else:
                header = f"{FILE_DATATYPE} {self.username} {filename}"

            header = bytes(header, ENCODING, ENCODING_ERROR_TYPE)
            while True:
                bytes_read = f.read(2 ** 23)
                if not bytes_read:
                    break

                data = encapsulate(bytes_read, header)
                self.client.sendall(data)
            # self.client.sendall(encapsulate(header, ""))

    def stream(self):
        self.streaming = True
        self.streamcount += 1

        header = f"{IMG_STREAM_DATATYPE} {self.username} {self.streamcount}"
        header = bytes(header, ENCODING, ENCODING_ERROR_TYPE)

        for frame in ScreenRecorder(to_bytes=True):
            if self.streaming:
                frame = encapsulate(frame, header)
                try:
                    self.client.sendall(frame)
                except ConnectionError:
                    self.streaming = False
                    break
            else:
                break

    def stopstream(self):
        if self.streaming:
            self.streaming = False
            header = bytes(STREAM_END_DATATYPE, ENCODING, ENCODING_ERROR_TYPE)
            self.client.send(encapsulate(b"", header))

            self.chat.print_to_chat("Stream ended.")
        else:
            self.chat.print_to_chat("You aren't streaming at the moment.")

    def close_chat(self):
        self.chat.setParent(None)
        self.ui.tab_widget.setCurrentIndex(0)

    def is_alive(self):
        return self.alive

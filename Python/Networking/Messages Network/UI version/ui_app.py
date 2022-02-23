# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ IMPORTS --------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import socket
import threading

import os
import re
import io

import datetime
from typing import Optional, Union

# for the screen capture
import cv2
from mss import mss
import numpy as np

try:
    from requests import get
except ImportError:
    print("Package installing...")
    os.system("pip install requests")
    print("Package installed !")
    print("Relaunch the programm now.")


# -----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- CONSTANTS -------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- HELPER FUNCTIONS ---------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


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


# -----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------- SERVER SIDE ------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


class Connection:
    """Class representing a connection from the server side, wich is a couple client-address-name"""

    def __init__(self, client: socket.SocketType, address: str, name: Optional[str] = None):
        self.name = name
        self.client = client
        self.address = address

        self.streaming = False
        self.stream_count = 0

    def send(self, data: Union[str, bytes], encode: bool = False):
        """Send a message to the client side of the connection.
        There is option to encode or not the message."""

        data = data.encode(ENCODING, ENCODING_ERROR_TYPE) if encode else data
        try:
            self.client.sendall(data)
        except ConnectionError:
            return

    def send_msg(self, msg: Union[str, bytes], encode: bool = True):
        """Send a message to the client side of the connection.
        There is option to encode or not the message."""

        msg = msg.encode(ENCODING, ENCODING_ERROR_TYPE) if encode else msg
        msg = encapsulate(msg, bytes(MSG_DATATYPE, ENCODING))
        self.client.sendall(msg)

    def receive(self, packet_size: int = 2048, decode: bool = True) -> Union[str, bytes]:
        """Receives a message to the client side of the connection.
        There is option to decode or not the message."""
        try:
            return self.client.recv(packet_size).decode(ENCODING) if decode else self.client.recv(packet_size)
        except ConnectionError:
            return None

    def is_up(self) -> bool:
        """Returns whether or not the client is still running."""
        return self.client.fileno() != -1

    def close(self):
        """Force closes the connection with the client side."""
        try:
            self.client.close()
        except Exception as e:
            print(f"Error while closing client {self.name} :\n{e}")


class Server:
    def __init__(self, host_address: str, host_port: str, password: str, max_connections: int = 50):
        self.alive = True

        self.host_address = host_address
        self.host_port = host_port
        self.password = password
        self.password_protected = password != ""

        self.max_connections = max_connections
        self.connections = []
        self.blacklist = []

        self.video_logers = {}

        self.establish_server_connection()

        self.auth_thread = threading.Thread(target=self.authentification_thread, daemon=False)
        self.auth_thread.start()

    def establish_server_connection(self):
        """Creates the server with the provided ip and port number."""
        try:
            self.server: socket.SocketType = socket.create_server((self.host_address, self.host_port))
        except socket.error as e:
            ui.print_to_admin(e)

        self.server.listen(self.max_connections)

    def authentification_thread(self):
        """Thread that takes care of handling any new incoming connections to the server."""

        while self.alive:
            try:
                client, address = self.server.accept()
            except OSError:
                break
            connection = Connection(client, address)
            if connection not in self.connections:
                if address[0] in self.blacklist:  # ip has been banned and is on the blacklist
                    connection.send(BANNED_MESSAGE, encode=True)
                    connection.close()
                    del connection
                    continue

                if self.password_protected:  # server has a password
                    connection.send("1", encode=True)
                    password = connection.receive()
                    if password != self.password:  # client did not provide the right password
                        connection.send(INVALID_PASSWORD, encode=True)
                        connection.close()
                        del connection
                        continue
                    connection.send("Password correct.", encode=True)
                else:  # server is password free
                    connection.send("0", encode=True)

                name = connection.receive()
                if name is None:
                    continue

                while name in [conn.name for conn in self.connections if conn != connection]:
                    name = f"{name}_"

                connection.send(name, encode=True)
                connection.name = name

                self.connections.append(connection)

                # starts a thread to handle the communication between the server and the client.
                thread = threading.Thread(target=self.connection_handler, args=(connection,), daemon=True)
                thread.start()

                thread.name = connection.name

                ui.print_to_admin(msg := f"<font color=red>Server message</font> : '{connection.name}' ({connection.address[0]}:{connection.address[1]}) connected to the server.")
                date = get_full_time()
                self.log(f"{date} - {msg}")

                self.send_everyone(f"<font color=blue>{connection.name}</font> joined the chat !")

        ui.print_to_admin("Authentification thread stopped.")

    def send_everyone(self, msg: Union[str, bytes], encode: bool = True):
        """Sends a message to every clients of the server."""
        for conn in self.connections:
            conn.send_msg(msg, encode=encode)

    def send_pm(self, connection: Connection, target_name: str, content: str):
        """Sends a private message from the connection 'connection' to the connection whose name is 'target_name'.
        Notifies the user about the success or not of the operation"""

        t = get_time()
        date = get_full_time()

        msg = f"{t} - {connection.name} sent you: {content}"
        log_msg = f"{date} - {connection.name} sent {target_name}: {content}"

        found = False
        for conn in self.connections:
            if conn.name == target_name:  # found the targeted user
                found = True
                conn.send_msg(msg)

        if found:  # operation was a success
            self.log(log_msg)
            ui.print_to_admin(msg)

        response_msg = "Message sent." if found else "Invalid user."  # notifies the user
        connection.send_msg(response_msg)

    def kick(self, target_name: str, reason: str):
        """Kicks a client from the server, but does not prevent him from connecting again.
        The connection from wich the command comes from need to be an administrator for this command to work."""

        t = get_time()
        date = get_full_time()

        msg = f"{t} - You got kicked from the chat for the reason: {reason}."
        log_msg = f"{date} - {target_name} has been kicked from the chat for the reason: {reason}."

        found = True
        for conn in self.connections:
            if conn.name == target_name:
                conn.send_msg(msg)
                conn.close()

                if conn.streaming:
                    self.handle_stream_end(conn)
                break
        else:
            found = False

        if found:
            self.log(log_msg)

        response_msg = "User kicked." if found else "Invalid user."
        ui.print_to_admin(response_msg)

    def ban(self, target_name: str, reason: str):
        """Bans a client from the server, preventing him from connecting again.
        The connection from wich the command comes from need to be an administrator for this command to work."""

        t = get_time()
        date = get_full_time()

        msg = f"{t} - You got banned you from the chat for the reason: {reason}."
        log_msg = f"{date} - {target_name} has been banned from the chat for the reason: {reason}."

        found = True
        for conn in self.connections:
            if conn.name == target_name:
                self.blacklist.append(conn.address[0])
                conn.send_msg(msg)
                conn.close()

                if conn.streaming:
                    self.handle_stream_end(conn)
                break
        else:
            found = False

        if found:
            self.log(log_msg)

        response_msg = "User banned." if found else "Invalid user."
        ui.print_to_admin(response_msg)

    # def is_same(self, connection1: Connection, connection2: Connection) -> bool:
    #     return connection1.client.getpeername() == connection2.client.getsockname() and connection1.client.getsockname() == connection2.client.getpeername()

    def connection_handler(self, connection: Connection):
        """Thread handling the communication between a client and the server."""

        while connection.is_up():
            try:
                raw_data = connection.receive(10_000_000, decode=False)
                if raw_data is None:  # means the connection has been closed
                    break

                header, res = decapsulate(raw_data)
                header = header.decode(ENCODING).strip()

                data_type = header.split(" ")[0]

            except ConnectionError:  # connection has been closed
                break
            except Exception as e:
                if DEBUG:
                    print(e)
                continue

            if data_type == MSG_DATATYPE:
                self.handle_message(connection, res.decode(ENCODING))

            elif data_type == IMG_STREAM_DATATYPE:
                self.handle_stream(connection, raw_data)

            elif data_type == STREAM_END_DATATYPE:
                self.handle_stream_end(connection)

        # the connection has been lost or closed
        # removes the client from the connections list and logs it

        connection.close()
        self.connections.remove(connection)

        msg = f"<font color=red>Server message</font> : '{connection.name}' ({connection.address[0]}:{connection.address[1]}) disconnected from the server."
        ui.print_to_admin(msg)

        date = get_full_time()
        log_msg = f"{date} - '{connection.name}' ({connection.address[0]}:{connection.address[1]}) disconnected from the server."
        self.log(log_msg)

        self.send_everyone(f"<font color=blue>{connection.name}</font> left the chat !")

        del connection

    def handle_message(self, connection: Connection, res: str):
        if res in {"!list names", "!list users"}:  # command to list the name of all connected users
            connection.send_msg(msg := f"Online users : <font color=blue>{'</font>, <font color=blue>'.join([conn.name for conn in self.connections])}</font>")
            date = get_full_time()
            ui.print_to_admin(f"{date} - {msg}")
            return

        if res.startswith("!send ") and len(parts := res.split(" ")[1:]) >= 2:  # command to send private message to other users
            target_name = parts[0]
            content = " ".join(parts[1:])
            self.send_pm(connection, target_name, content)
            return

        t = get_time()
        date = get_full_time()

        msg = f"""{t} - <font color=blue>{connection.name}</font>: {res}"""
        log_msg = f"{date} - {connection.name}: {res}"

        self.log(log_msg)
        ui.print_to_admin(msg)

        for conn in self.connections:
            if conn is not connection and conn.is_up():
                conn.send_msg(msg)

    def handle_stream(self, connection: Connection, encapsulated_frame: bytes):
        if connection.streaming == False:
            connection.streaming = True
            connection.stream_count += 1

            out = self._create_video_writer(f"{connection.name}{connection.stream_count}")
            self.video_logers[connection.name] = out

            log_msg = f"{get_full_time()}: {connection.name} started streaming."
            self.log(log_msg)

            log_msg_html = f"{get_full_time()}: <font color=blue>{connection.name}</font> started streaming."
            ui.print_to_admin(log_msg_html)

        for conn in self.connections:
            if conn is not connection and conn.is_up():
                conn.send(encapsulated_frame)
                # for logs
                _, frame = decapsulate(encapsulated_frame)
                self.video_log(frame, connection)

    def handle_stream_end(self, connection: Connection):
        connection.streaming = False
        self.video_logers[connection.name].release()
        del self.video_logers[connection.name]

        for conn in self.connections:
            if conn is not connection and conn.is_up():
                conn.send(encapsulate(bytes(connection.name, ENCODING, ENCODING_ERROR_TYPE), bytes(STREAM_END_DATATYPE, ENCODING, ENCODING_ERROR_TYPE)))
                conn.send_msg(f"{connection.name} stopped streaming.")

        log_msg = f"{get_full_time()}: {connection.name} stopped streaming."
        self.log(log_msg)

        log_msg_html = f"{get_full_time()}: <font color=blue>{connection.name}</font> stopped streaming."
        ui.print_to_admin(log_msg_html)

    def close_server(self):
        """Properly closes the server."""

        self.alive = False
        for conn in self.connections:
            try:
                conn.send_msg("Server is shutting down, you are going to be disconnected.")
                conn.close()
            except OSError:
                continue
        self.server.close()
        ui.print_to_admin("Server closed.")

    def log(self, log_msg: str):
        """Write a message to the log file."""

        with io.open(f"__log_{self.host_address}-{self.host_port}.log", "a", encoding=ENCODING, errors=ENCODING_ERROR_TYPE) as f:
            try:
                f.write(f"{log_msg}\n")
            except UnicodeEncodeError:
                ui.print_to_admin(f"Failed to log message : {log_msg}")

    def video_log(self, frame: bytes, connection: Connection):
        try:
            frame = bytes_to_array(frame)
        except ValueError:
            return
        self.video_logers[connection.name].write(frame)

    def _create_video_writer(self, name: str, resolution=(1920, 1080), fps=15.0):
        return cv2.VideoWriter(f"__log_{self.host_address}-{self.host_port}-{name}.avi", VIDEO_CODEC, fps, resolution)


# -----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------- CLIENT SIDE ------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


class Client:
    def __init__(self, host_address, host_port, name, password, chat):
        self.host_address = host_address
        self.host_port = host_port
        self.username = name
        self.chat = chat

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
                    ui.show_popup(
                        "Error !",
                        f"Your access to the following server : {self.host_address}:{self.host_port} has been denied due to an invalid password.",
                        icon=QMessageBox.Warning,
                    )

            elif response == BANNED_MESSAGE:
                self.close_chat()
                ui.show_popup(
                    "Error !",
                    f"Your access to the following server : {self.host_address}:{self.host_port} has been denied because you are banned from this server.",
                    icon=QMessageBox.Critical,
                )

            self.client.send(self.username.encode(ENCODING, ENCODING_ERROR_TYPE))
            self.username = self.client.recv(1024).decode(ENCODING)

            ui.show_popup("Success !", f"You successfully connected to the following server : {self.host_address}:{self.host_port}", icon=QMessageBox.Information)

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

                    if f"{streamer}{id}" not in self.closed_streams:
                        if cv2.getWindowProperty(streamer, cv2.WND_PROP_VISIBLE) == 0:
                            cv2.namedWindow(streamer, cv2.WINDOW_NORMAL)
                            cv2.resizeWindow(streamer, 1920 // 2, 1080 // 2)

                        cv2.imshow(streamer, frame)
                        if cv2.waitKey(1) & 0xFF == ord("q"):
                            self.closed_streams.append(f"{streamer}{id}")
                            cv2.destroyWindow(streamer)

                elif data_type == STREAM_END_DATATYPE:
                    cv2.destroyWindow(res.decode(ENCODING))

            except ConnectionError:
                self.close_chat()
                del app.clients[self.chat._name]
                break

            except Exception as e:
                if DEBUG:
                    self.chat.print_to_chat(e)
                continue

    def handle_input(self, inp: str):
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
        ui.tab_widget.setCurrentIndex(0)


# -----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------- MAIN PROGRAMM -----------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1000, 800)
        MainWindow.setWindowTitle("Message Network")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setToolTip("")
        self.main_frame.setStatusTip("")
        self.main_frame.setWhatsThis("")
        self.main_frame.setAccessibleName("")
        self.main_frame.setAccessibleDescription("")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        self.tab_widget = QtWidgets.QTabWidget(self.main_frame)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, 971, 751))
        self.tab_widget.setObjectName("tab_widget")

        self.join_tab = QtWidgets.QWidget()
        self.join_tab.setObjectName("join_tab")
        self.join_name_label = QtWidgets.QLabel(self.join_tab)
        self.join_name_label.setGeometry(QtCore.QRect(20, -10, 931, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.join_name_label.setFont(font)
        self.join_name_label.setText("Chose a name :")
        self.join_name_label.setObjectName("join_name_label")
        self.join_name_input = QtWidgets.QLineEdit(self.join_tab)
        self.join_name_input.setGeometry(QtCore.QRect(20, 50, 931, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.join_name_input.setFont(font)
        self.join_name_input.setText("")
        self.join_name_input.setAlignment(QtCore.Qt.AlignCenter)
        self.join_name_input.setPlaceholderText("Enter your name.")
        self.join_name_input.setClearButtonEnabled(False)
        self.join_name_input.setObjectName("join_name_input")
        self.line_4 = QtWidgets.QFrame(self.join_tab)
        self.line_4.setGeometry(QtCore.QRect(10, 130, 971, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.join_port_label = QtWidgets.QLabel(self.join_tab)
        self.join_port_label.setGeometry(QtCore.QRect(20, 140, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.join_port_label.setFont(font)
        self.join_port_label.setText("Chose a port :")
        self.join_port_label.setObjectName("join_port_label")
        self.join_port_input = QtWidgets.QLineEdit(self.join_tab)
        self.join_port_input.setGeometry(QtCore.QRect(20, 200, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.join_port_input.setFont(font)
        self.join_port_input.setText("8008")
        self.join_port_input.setAlignment(QtCore.Qt.AlignCenter)
        self.join_port_input.setPlaceholderText("Enter a port number.")
        self.join_port_input.setClearButtonEnabled(False)
        self.join_port_input.setObjectName("join_port_input")
        self.line_5 = QtWidgets.QFrame(self.join_tab)
        self.line_5.setGeometry(QtCore.QRect(0, 280, 971, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.join_server_label = QtWidgets.QLabel(self.join_tab)
        self.join_server_label.setGeometry(QtCore.QRect(20, 290, 481, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.join_server_label.setFont(font)
        self.join_server_label.setText("Chose a server :")
        self.join_server_label.setObjectName("join_server_label")
        self.join_serverlist_combo_box = QtWidgets.QComboBox(self.join_tab)
        self.join_serverlist_combo_box.setGeometry(QtCore.QRect(20, 350, 891, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.join_serverlist_combo_box.setFont(font)
        self.join_serverlist_combo_box.setObjectName("join_serverlist_combo_box")
        self.join_serverlist_combo_box.addItem("")
        self.join_serverlist_combo_box.setItemText(0, "No servers available. Try scanning for servers.")
        self.scan_server_button = QtWidgets.QPushButton(self.join_tab)
        self.scan_server_button.setGeometry(QtCore.QRect(640, 300, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.scan_server_button.setFont(font)
        self.scan_server_button.setText("Press to scan for available servers")
        self.scan_server_button.setObjectName("scan_server_button")
        self.line_6 = QtWidgets.QFrame(self.join_tab)
        self.line_6.setGeometry(QtCore.QRect(0, 400, 971, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.join_server_button = QtWidgets.QPushButton(self.join_tab)
        self.join_server_button.setGeometry(QtCore.QRect(60, 580, 851, 121))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.join_server_button.setFont(font)
        self.join_server_button.setText("Join Server !")
        self.join_server_button.setDefault(True)
        self.join_server_button.setFlat(False)
        self.join_server_button.setObjectName("join_server_button")
        self.line_7 = QtWidgets.QFrame(self.join_tab)
        self.line_7.setGeometry(QtCore.QRect(0, 550, 971, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.join_password_label = QtWidgets.QLabel(self.join_tab)
        self.join_password_label.setGeometry(QtCore.QRect(20, 410, 931, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.join_password_label.setFont(font)
        self.join_password_label.setText("Enter the server's password (if server has no password then leave blank) :")
        self.join_password_label.setObjectName("join_password_label")
        self.join_password_input = QtWidgets.QLineEdit(self.join_tab)
        self.join_password_input.setGeometry(QtCore.QRect(20, 470, 881, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.join_password_input.setFont(font)
        self.join_password_input.setText("")
        self.join_password_input.setAlignment(QtCore.Qt.AlignCenter)
        self.join_password_input.setPlaceholderText("Enter the password.")
        self.join_password_input.setClearButtonEnabled(False)
        self.join_password_input.setObjectName("join_password_input")
        self.tab_widget.addTab(self.join_tab, "Join Server")

        self.host_tab = QtWidgets.QWidget()
        self.host_tab.setObjectName("host_tab")
        self.host_ip_label = QtWidgets.QLabel(self.host_tab)
        self.host_ip_label.setEnabled(True)
        self.host_ip_label.setGeometry(QtCore.QRect(20, 10, 481, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.host_ip_label.setFont(font)
        self.host_ip_label.setText("Chose the IP address you want to use :")
        self.host_ip_label.setObjectName("host_ip_label")
        self.host_port_label = QtWidgets.QLabel(self.host_tab)
        self.host_port_label.setGeometry(QtCore.QRect(150, 180, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.host_port_label.setFont(font)
        self.host_port_label.setText("Chose a port :")
        self.host_port_label.setObjectName("host_port_label")
        self.host_password_label = QtWidgets.QLabel(self.host_tab)
        self.host_password_label.setGeometry(QtCore.QRect(20, 390, 931, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.host_password_label.setFont(font)
        self.host_password_label.setText("Chose a password (blank means the server is not password-protected) :")
        self.host_password_label.setObjectName("host_password_label")
        self.host_port_input = QtWidgets.QLineEdit(self.host_tab)
        self.host_port_input.setGeometry(QtCore.QRect(150, 250, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.host_port_input.setFont(font)
        self.host_port_input.setText("8008")
        self.host_port_input.setAlignment(QtCore.Qt.AlignCenter)
        self.host_port_input.setPlaceholderText("Enter a port number.")
        self.host_port_input.setClearButtonEnabled(False)
        self.host_port_input.setObjectName("host_port_input")
        self.host_ip_combo_box = QtWidgets.QComboBox(self.host_tab)
        self.host_ip_combo_box.setGeometry(QtCore.QRect(20, 80, 891, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.host_ip_combo_box.setFont(font)
        self.host_ip_combo_box.setObjectName("host_ip_combo_box")
        self.host_ip_combo_box.addItem("")
        self.host_ip_combo_box.setItemText(0, "Localhost (127.0.0.1)")
        self.host_ip_combo_box.addItem("")
        self.host_ip_combo_box.setItemText(1, "Local IP address")
        self.host_ip_combo_box.addItem("")
        self.host_ip_combo_box.setItemText(2, "Public IP address")
        self.host_ip_combo_box.addItem("")
        self.host_ip_combo_box.setItemText(3, "All interfaces (both private and public)")
        self.line = QtWidgets.QFrame(self.host_tab)
        self.line.setGeometry(QtCore.QRect(0, 160, 971, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.host_tab)
        self.line_2.setGeometry(QtCore.QRect(0, 370, 971, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.host_password_input = QtWidgets.QLineEdit(self.host_tab)
        self.host_password_input.setGeometry(QtCore.QRect(20, 460, 851, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.host_password_input.setFont(font)
        self.host_password_input.setText("")
        self.host_password_input.setAlignment(QtCore.Qt.AlignCenter)
        self.host_password_input.setPlaceholderText("Enter a password.")
        self.host_password_input.setClearButtonEnabled(False)
        self.host_password_input.setObjectName("host_password_input")
        self.host_server_button = QtWidgets.QPushButton(self.host_tab)
        self.host_server_button.setGeometry(QtCore.QRect(20, 580, 461, 121))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.host_server_button.setFont(font)
        self.host_server_button.setText("Host Server")
        self.host_server_button.setShortcut("")
        self.host_server_button.setAutoDefault(False)
        self.host_server_button.setDefault(True)
        self.host_server_button.setObjectName("host_server_button")
        self.line_3 = QtWidgets.QFrame(self.host_tab)
        self.line_3.setGeometry(QtCore.QRect(0, 550, 971, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.stop_hosting_button = QtWidgets.QPushButton(self.host_tab)
        self.stop_hosting_button.setGeometry(QtCore.QRect(490, 580, 461, 121))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.stop_hosting_button.setFont(font)
        self.stop_hosting_button.setText("Stop Hosting")
        self.stop_hosting_button.setShortcut("")
        self.stop_hosting_button.setObjectName("stop_hosting_button")
        self.line_8 = QtWidgets.QFrame(self.host_tab)
        self.line_8.setGeometry(QtCore.QRect(460, 180, 20, 191))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.debug_checkbox = QtWidgets.QCheckBox(self.host_tab)
        self.debug_checkbox.setGeometry(QtCore.QRect(670, 240, 151, 61))
        self.debug_checkbox.setMinimumSize(QtCore.QSize(50, 50))
        self.debug_checkbox.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.debug_checkbox.setFont(font)
        self.debug_checkbox.setText("Debug")
        self.debug_checkbox.setIconSize(QtCore.QSize(20, 20))
        self.debug_checkbox.setChecked(False)
        self.debug_checkbox.setObjectName("debug_checkbox")
        self.tab_widget.addTab(self.host_tab, "Host Server")

        self.gridLayout.addWidget(self.tab_widget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

    def init_ui(self):
        """Initialize the UI before being shown"""
        self.host_ip_combo_box.setCurrentIndex(1)

        self.join_server_button.clicked.connect(app.join_server)
        self.scan_server_button.clicked.connect(app.scan_servers)
        self.host_server_button.clicked.connect(app.host_server)
        self.stop_hosting_button.clicked.connect(app.stop_hosting)

        app.scan_servers()

        self.chats = {}

    def show_popup(self, title, message, details="", icon=QMessageBox.Information):
        msg = QMessageBox()

        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setDetailedText(details)

        msg.setIcon(icon)

        msg.setStandardButtons(QMessageBox.Ok)

        msg.exec_()

    def print_to_admin(self, msg=""):
        self.admin_browser.append(str(msg))

    def create_admin_tab(self):
        self.admin_tab = QtWidgets.QWidget()
        self.admin_tab.setObjectName("admin_tab")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.admin_tab)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 951, 711))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.admin_layout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.admin_layout.setContentsMargins(0, 0, 0, 0)
        self.admin_layout.setObjectName("admin_layout")
        self.admin_send_button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.admin_send_button.setFont(font)
        self.admin_send_button.setText("Send To Everyone")
        self.admin_send_button.setShortcut("")
        self.admin_send_button.setObjectName("admin_send_button")
        self.admin_layout.addWidget(self.admin_send_button, 2, 1, 1, 1)
        self.admin_input = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.admin_input.setFont(font)
        self.admin_input.setText("")
        self.admin_input.setPlaceholderText("Type here and hit enter to send a message.")
        self.admin_input.setObjectName("admin_input")
        self.admin_layout.addWidget(self.admin_input, 2, 0, 1, 1)
        self.admin_browser = QtWidgets.QTextBrowser(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Source Code Pro")
        font.setPointSize(10)
        self.admin_browser.setFont(font)
        self.admin_browser.setHtml(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'Source Code Pro'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
            '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>'
        )
        self.admin_browser.setObjectName("admin_browser")
        self.admin_layout.addWidget(self.admin_browser, 1, 0, 1, 2)
        self.tab_widget.addTab(self.admin_tab, "Server Administration")

        self.admin_send_button.clicked.connect(app.admin_send_msg)
        self.admin_input.returnPressed.connect(app.admin_send_msg)

        return self.admin_tab


class ChatTab(QtWidgets.QWidget):
    def __init__(self, name):
        self._name = name

        QtWidgets.QWidget.__init__(self)
        self.setObjectName(name)

        self.gridLayoutWidget_2 = QtWidgets.QWidget(self)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 9, 951, 711))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.chat_layout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_layout.setObjectName("chat_layout")
        self.chat_send_button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chat_send_button.setFont(font)
        self.chat_send_button.setText("Send")
        self.chat_send_button.setShortcut("")
        self.chat_send_button.setObjectName("chat_send_button")
        self.chat_layout.addWidget(self.chat_send_button, 2, 1, 1, 1)
        self.chat_input = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chat_input.setFont(font)
        self.chat_input.setText("")
        self.chat_input.setPlaceholderText("Type here and hit enter to send message.")
        self.chat_input.setObjectName("chat_input")
        self.chat_layout.addWidget(self.chat_input, 2, 0, 1, 1)
        self.chat_browser = QtWidgets.QTextBrowser(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Source Code Pro")
        font.setPointSize(10)
        self.chat_browser.setFont(font)
        self.chat_browser.setHtml(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'Source Code Pro'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
            '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>'
        )
        self.chat_browser.setObjectName("chat_browser")
        self.chat_layout.addWidget(self.chat_browser, 1, 0, 1, 2)

        ui.tab_widget.addTab(self, self._name)

        self.chat_input.returnPressed.connect(lambda: app.send_msg(self._name))
        self.chat_send_button.clicked.connect(lambda: app.send_msg(self._name))

    def clear_chat(self):
        self.chat_browser.clear()

    def print_to_chat(self, msg=""):
        self.chat_browser.append(str(msg))


class App:
    def __init__(self):
        self.clients = {}
        self.hosted_server = None

        self.joined_server = []

    def join_server(self):

        name = ui.join_name_input.text()
        name = name.replace(" ", "_") or "user"

        host = ui.join_serverlist_combo_box.currentText()
        if host == DEFAULT_SERVER_MSG:
            ui.show_popup("Invalid server", "This server is invalid, try scanning for servers again.", icon=QMessageBox.Warning)
            return

        ip = host.split(":")[0]
        port = host.split(":")[1].split(" - ")[0]
        chat_name = f"Chat {ip}:{port}"

        if chat_name in self.clients:
            ui.show_popup("Error", "You are already connected to that server. Only one connection is allowed.", icon=QMessageBox.Warning)
            return

        password = ui.join_password_input.text()

        ui.chats[chat_name] = ChatTab(chat_name)

        client = Client(ip, port, name, password, ui.chats[chat_name])
        self.clients[chat_name] = client
        if not client.accepted:
            del self.clients[chat_name]

        index = ui.tab_widget.indexOf(ui.chats[chat_name])
        ui.tab_widget.setCurrentIndex(index)

    def scan_servers(self):
        port = ui.join_port_input.text()
        if port and port.isdigit():
            port = int(port)
        else:
            ui.show_popup("Invalid port", "You need to enter a valid port before scanning for servers.", icon=QMessageBox.Warning)

        if servers := get_servers(port):
            if ui.join_serverlist_combo_box.currentText() == DEFAULT_SERVER_MSG:
                ui.join_serverlist_combo_box.clear()

            for ip in servers:
                ui.join_serverlist_combo_box.addItem(f"{ip}:{port} - {socket.gethostbyaddr(ip)[0]}")

    def host_server(self):
        global debug

        if self.hosted_server:
            ui.show_popup(
                "Can't host multiple servers",
                "You are already hosting a server.",
                details=f"You host a server at the following address : {self.host_ip}:{self.host_port}",
                icon=QMessageBox.Warning,
            )
            return

        combo_box_index = ui.host_ip_combo_box.currentIndex()
        if combo_box_index == 0:
            ip = "127.0.0.1"
        elif combo_box_index == 1:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        elif combo_box_index == 2:
            ip = get("https://api.ipify.org").text
        elif combo_box_index == 3:
            ip = ""

        port = int(ui.host_port_input.text())
        password = ui.host_password_input.text()

        debug = ui.debug_checkbox.isChecked()

        self.hosted_server = Server(ip, port, password)

        admin_tab = ui.create_admin_tab()

        self.host_ip = ip
        self.host_port = port
        ui.show_popup("Success !", f"You are currently hosting a server at the following address : {self.host_ip}:{self.host_port}", icon=QMessageBox.Information)

        index = ui.tab_widget.indexOf(admin_tab)
        ui.tab_widget.setCurrentIndex(index)

    def stop_hosting(self):

        if not self.hosted_server:
            ui.show_popup("Error", "You aren't hosting a server yet.", icon=QMessageBox.Warning)
            return

        self.hosted_server.close_server()
        self.hosted_server = None

        ui.show_popup("Success !", "You stopped hosting the server.", icon=QMessageBox.Information)
        ui.admin_tab.setParent(None)

    def send_msg(self, chat_name):
        chat = ui.chats[chat_name]
        client = self.clients[chat_name]

        if txt := chat.chat_input.text():
            chat.chat_input.setText("")

            if txt == "!clear":
                chat.clear_chat()
                return

            if txt == "!leave":
                client.handle_input(txt)
                # del self.clients[chat_name]
                return

            chat.print_to_chat(txt)
            client.handle_input(txt)

    def admin_send_msg(self):
        if txt := ui.admin_input.text():
            ui.admin_input.setText("")

            if txt.startswith("!kick ") and len(parts := txt.split(" ")[1:]) >= 1:  # command to kick other users
                ui.print_to_admin(txt)
                target_name = parts[0]
                content = " ".join(parts[1:])
                self.hosted_server.kick(target_name, content)
                return

            if txt.startswith("!ban ") and len(parts := txt.split(" ")[1:]) >= 1:  # command to ban other users
                ui.print_to_admin(txt)
                target_name = parts[0]
                content = " ".join(parts[1:])
                self.hosted_server.ban(target_name, content)
                return

            txt = f"[<font color=red>ADMIN</font>] {txt}"

            ui.print_to_admin(txt)
            self.hosted_server.send_everyone(txt)


if __name__ == "__main__":
    import sys

    global ui, app

    app = App()

    main_app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.init_ui()

    MainWindow.show()

    main_app.exec_()

    if app.clients:
        clients = app.clients.values()
        for client in clients:
            client.handle_input("!leave")

    if app.hosted_server:
        app.hosted_server.close_server()
        exit()

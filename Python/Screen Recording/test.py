# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ IMPORTS --------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

import socket
import threading

import os
import re
import io

import time
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
# -------------------------------------------------- HELPER FUNCTIONS ---------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


def encapsulate(data: bytes, head: bytes, fill_car=" ") -> bytes:
    while len(head) != CAPSULE_SIZE:
        head += bytes(fill_car, ENCODING)
    return head + data


def decapsulate(data: bytes) -> bytes:
    return data[:CAPSULE_SIZE], data[CAPSULE_SIZE:]


def get_ip_addresses():
    """Returns a list of all the ip adresses of the local network"""
    addresses = []
    for device in os.popen("arp -a"):
        device = re.search("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", device, re.M | re.I)
        if device is not None:
            addresses.append(device.group(0))
    return addresses


def get_time():
    return datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")


def array_to_bytes(x: np.ndarray) -> bytes:
    np_bytes = io.BytesIO()
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()


def bytes_to_array(b: bytes) -> np.ndarray:
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
# ----------------------------------------------------- CONSTANTS -------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

INVALID_PASSWORD = "Invalid password."
BANNED_MESSAGE = "Connection to the server impossible, you are banned from the chat."

DEFAULT_PORT = 8008

ENCODING = "utf-16le"
ENCODING_ERROR_TYPE = "backslashreplace"

MSG_DATATYPE = "1"
IMG_STREAM_DATATYPE = "2"
STREAM_END_DATATYPE = "3"

CAPSULE_SIZE = 500

# -----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------- SERVER SIDE ------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


class Connection:
    """Class representing a connection from the server side, wich is a couple client-address-name"""

    def __init__(self, client: socket.SocketType, address: str, name: Optional[str] = None):
        self.name = name
        self.client = client
        self.address = address

    def send(self, data: Union[str, bytes], encode: bool = False):
        """Send a message to the client side of the connection.
        There is option to encode or not the message."""

        data = data.encode(ENCODING, ENCODING_ERROR_TYPE) if encode else data
        self.client.sendall(data)

    def send_msg(self, msg: Union[str, bytes], encode: bool = True):
        """Send a message to the client side of the connection.
        There is option to encode or not the message."""

        msg = msg.encode(ENCODING, ENCODING_ERROR_TYPE) if encode else msg
        msg = encapsulate(msg, bytes(MSG_DATATYPE, ENCODING))
        self.client.sendall(msg)

    def receive(self, packet_size: int = 2048, decode: bool = True) -> Union[str, bytes]:
        """Receives a message to the client side of the connection.
        There is option to decode or not the message."""

        return self.client.recv(packet_size).decode(ENCODING) if decode else self.client.recv(packet_size)

    def is_up(self) -> bool:
        """Returns whether or not the client is still running."""
        return self.client.fileno() != -1

    def close(self):
        """Force closes the connection with the client side."""
        try:
            self.client.close()
        except Exception as e:
            print(f"Error while closing client {self.name} :\n{e}")


class ServerThread(threading.Thread):
    def __init__(self, host_address: str, host_port: str, password: str, max_connections: int = 50):
        self.host_address = host_address
        self.host_port = host_port
        self.password = password
        self.password_protected = password != ""

        self.max_connections = max_connections
        self.connections = []
        self.blacklist = []

        self.host_client = None

        self.establish_server_connection()

        super().__init__(name="Server Thread")
        self.daemon = False
        self.start()

    def establish_server_connection(self):
        """Creates the server with the provided ip and port number."""
        try:
            self.server: socket.SocketType = socket.create_server((self.host_address, self.host_port))
        except socket.error as e:
            print(e)

        self.server.listen(self.max_connections)
        print(f"Socket successfully bound to {self.host_address}:{self.host_port} and listening.\n")

    def send_everyone(self, msg: Union[str, bytes], encode: bool = True):
        """Sends a message to every clients of the server."""
        for conn in self.connections:
            conn.send_msg(msg, encode=encode)

    def run(self):
        """Thread that takes care of handling any new incoming connections to the server."""

        while True:
            client, address = self.server.accept()
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

                self.connections.append(connection)
                # starts a thread to handle the communication between the server and the client.
                thread = threading.Thread(target=self.connection_handler, args=(connection,), daemon=False)
                thread.start()

                time.sleep(0.1)
                thread.name = connection.name

                print(msg := f"Server message : '{connection.name}' ({connection.address[0]}:{connection.address[1]}) connected to the server.")
                date = get_time()
                self.log(f"{date} - {msg}")

                self.send_everyone(f"{connection.name} joined the chat !")

    def send_pm(self, connection: Connection, target_name: str, content: str):
        """Sends a private message from the connection 'connection' to the connection whose name is 'target_name'.
        Notifies the user about the success or not of the operation"""

        date = get_time()
        msg = f"{date} - {connection.name} sent you: {content}"
        log_msg = f"{date} - {connection.name} sent {target_name}: {content}"

        found = False
        for conn in self.connections:
            if conn.name == target_name:  # found the targeted user
                found = True
                conn.send_msg(msg)

        if found:  # operation was a success
            self.log(log_msg)

        response_msg = "Message sent." if found else "Invalid user."  # notifies the user
        connection.send_msg(response_msg)

    def kick(self, connection: Connection, target_name: str, reason: str):
        """Kicks a client from the server, but does not prevent him from connecting again.
        The connection from wich the command comes from need to be an administrator for this command to work."""

        if self.is_administator(connection):  # checks whether or not the client that executed the command is an administator
            date = get_time()
            msg = f"{date} - {connection.name} kicked you from the chat for the reason: {reason}."
            log_msg = f"{date} - {connection.name} kicked {target_name} from the chat for the reason: {reason}."

            found = False
            for conn in self.connections:
                if conn.name == target_name:
                    found = True
                    conn.send_msg(msg)
                    conn.close()

            if found:
                self.log(log_msg)
            response_msg = "User kicked." if found else "Invalid user."

        else:  # client is not an administator
            response_msg = "You are not an administrator."
        connection.send_msg(response_msg)

    def ban(self, connection: Connection, target_name: str, reason: str):
        """Bans a client from the server, preventing him from connecting again.
        The connection from wich the command comes from need to be an administrator for this command to work."""

        if self.is_administator(connection):  # checks whether or not the client that executed the command is an administator
            date = get_time()
            msg = f"{date} - {connection.name} banned you from the chat for the reason: {reason}."
            log_msg = f"{date} - {connection.name} banned {target_name} from the chat for the reason: {reason}."

            found = False
            for conn in self.connections:
                if conn.name == target_name:
                    found = True
                    self.blacklist.append(conn.address[0])
                    conn.send_msg(msg)
                    conn.close()

            if found:
                self.log(log_msg)
            response_msg = "User banned." if found else "Invalid user."

        else:  # client is not an administator
            response_msg = "You are not an administrator."
        connection.send_msg(response_msg)

    def spy(self, connection: Connection, target_name: str):
        """Bans a client from the server, preventing him from connecting again.
        The connection from wich the command comes from need to be an administrator for this command to work."""

        if self.is_administator(connection):  # checks whether or not the client that executed the command is an administator

            msg = ""

            found = False
            for conn in self.connections:
                if conn.name == target_name:
                    found = True
                    conn.send_msg(msg)
                    conn.close()

            response_msg = "User spyed." if found else "Invalid user."
        else:  # client is not an administator
            response_msg = "You are not an administrator."
        connection.send_msg(response_msg)

    def is_administator(self, connection: Connection) -> bool:
        """Returns whether or not the connection is an administator of the server."""
        return self.host_client and self.host_client.getpeername() == connection.client.getsockname() and self.host_client.getsockname() == connection.client.getpeername()

    def connection_handler(self, connection: Connection):
        """Thread handling the communication between a client and the server."""

        name = connection.receive()

        while name in [conn.name for conn in self.connections if conn != connection]:
            name = f"{name}_"

        connection.name = name

        time.sleep(0.5)

        while connection.is_up():
            try:
                raw_data = connection.receive(10_000_000, decode=False)
                header, res = decapsulate(raw_data)
                header = header.decode(ENCODING).strip()

                data_type = header.split(" ")[0]

            except ConnectionError:  # connection has been closed
                break
            except Exception as e:
                print(e)
                continue

            if data_type == MSG_DATATYPE:
                self.handle_message(connection, res.decode(ENCODING))

            elif data_type == IMG_STREAM_DATATYPE:
                self.handle_stream(connection, raw_data)

            elif data_type == STREAM_END_DATATYPE:
                self.handle_stream_end(connection, res.decode(ENCODING))

        # the connection has been lost or closed
        # removes the client from the connections list and logs it

        connection.close()
        self.connections.remove(connection)

        print(msg := f"Server message : '{connection.name}' ({connection.address[0]}:{connection.address[1]}) disconnected from the server.")
        date = get_time()
        self.log(f"{date} - {msg}")

        self.send_everyone(f"{connection.name} left the chat !")

        del connection

    def handle_message(self, connection: Connection, res: str):
        if res in {"!list names", "!list users"}:  # command to list the name of all connected users
            connection.send_msg(msg := f"Online users : {', '.join([conn.name for conn in self.connections])}")
            date = get_time()
            self.log(f"{date} - {msg}")
            return

        if res.startswith("!send ") and len(parts := res.split(" ")[1:]) >= 2:  # command to send private message to other users
            target_name = parts[0]
            content = " ".join(parts[1:])
            self.send_pm(connection, target_name, content)
            return

        if res.startswith("!kick ") and len(parts := res.split(" ")[1:]) >= 1:  # command to kick other users
            target_name = parts[0]
            content = " ".join(parts[1:])
            self.kick(connection, target_name, content)
            return

        if res.startswith("!ban ") and len(parts := res.split(" ")[1:]) >= 1:  # command to ban other users
            target_name = parts[0]
            content = " ".join(parts[1:])
            self.ban(connection, target_name, content)
            return

        if res.startswith("!spy ") and len(parts := res.split(" ")[1:]) >= 1:  # command to spy other users (very ethical)
            target_name = parts[0]
            self.spy(connection, target_name)
            return

        date = get_time()
        msg = f"{date} - {connection.name}: {res}"

        self.log(msg)

        for conn in self.connections:
            if conn is not connection and conn.is_up():
                conn.send_msg(msg)

    def handle_stream(self, connection: Connection, frame: bytes):
        for conn in self.connections:
            if conn is not connection and conn.is_up():
                conn.send(frame)

    def handle_stream_end(self, connection: Connection, msg: str):
        for conn in self.connections:
            if conn is not connection and conn.is_up():
                conn.send(encapsulate(bytes(connection.name, ENCODING, ENCODING_ERROR_TYPE), bytes(STREAM_END_DATATYPE, ENCODING, ENCODING_ERROR_TYPE)))
                conn.send_msg(msg)

    def log(self, log_msg: str):
        """Write a message to the log file."""

        with io.open(f"__log_{self.host_address}-{self.host_port}.log", "a", encoding=ENCODING, errors=ENCODING_ERROR_TYPE) as f:
            try:
                f.write(f"{log_msg}\n")
            except UnicodeEncodeError:
                print(f"Failed to log message : {log_msg}")


def host_server():
    while True:
        try:
            choice = int(input("Hosting IP address ?\n1) localhost (127.0.0.1)\n2) machine's local ip address\n3) machine's public ip address\n4) all interfaces\n"))
        except ValueError:
            print("Invalide input, try again.")
            continue

        if choice == 1:
            ip = "127.0.0.1"
            break
        elif choice == 2:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            break
        elif choice == 3:
            ip = get("https://api.ipify.org").text
        elif choice == 4:
            ip = ""
        else:
            print("Invalide choice, try again.")

    port = input(f"Port (leave blank for {DEFAULT_PORT}): ")
    port = int(port) if port else DEFAULT_PORT

    password = str(input("Enter a password (leave blank for no password) : "))

    return ServerThread(ip, port, password)


# -----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------- CLIENT SIDE ------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


class KeyboardThread(threading.Thread):
    def __init__(self, input_cbk=None, *, name="keyboard-input-thread"):
        self.input_cbk = input_cbk
        self.stopped = False
        super().__init__(name=name)
        self.daemon = True
        self.start()

    def run(self):
        while not self.stopped:
            self.input_cbk(input())

    def stop(self):
        self.stopped = True


class ClientThread(threading.Thread):
    def __init__(self, host_address, host_port, name):
        self.host_address = host_address
        self.host_port = host_port
        self.username = name

        self.closed_streams = []
        self.streaming = False
        self.streamcount = 0

        super().__init__(name=name)
        self.daemon = True

        self.establish_client_connection()
        self.kthread = KeyboardThread(self.handle_input)

    def run(self):
        if self.denied:
            return
        print("Connection established with the server.")

        if hosted_server and (hosted_server.host_address == self.host_address or self.host_address == "") and hosted_server.host_port == self.host_port:
            hosted_server.host_client = self.client

        while self.client.fileno() != -1:
            try:
                header, res = decapsulate(self.client.recv(10_000_000))
                header = header.decode(ENCODING).strip()

                data_type = header.split(" ")[0]

                if data_type == MSG_DATATYPE:
                    print(res.decode(ENCODING))

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
                print("Connection closed, press ENTER to continue.")
                break
            except EOFError:
                continue
            except Exception as e:
                print(e)

    def establish_client_connection(self):
        print("Waiting for connection response")
        try:
            self.denied = False
            self.client = socket.create_connection((self.host_address, self.host_port))

            if (response := self.client.recv(1024).decode(ENCODING)) == "1":  # server has a password
                self.client.send(str(input("Enter server password : ")).encode(ENCODING, ENCODING_ERROR_TYPE))
                print(response := self.client.recv(1024).decode(ENCODING))
                if response == INVALID_PASSWORD:
                    print("Connection denied, press ENTER to continue.")
                    self.denied = True
            elif response == BANNED_MESSAGE:
                print(response)
                self.denied = True

            self.client.send(self.username.encode(ENCODING, ENCODING_ERROR_TYPE))
            self.start()
        except socket.error as e:
            print(e)
        print()

    def stream(self):
        self.streaming = True
        self.streamcount += 1

        for frame in ScreenRecorder(to_bytes=True):
            if self.streaming:
                header = f"{IMG_STREAM_DATATYPE} {self.username} {self.streamcount}"
                header = bytes(header, ENCODING, ENCODING_ERROR_TYPE)
                frame = encapsulate(frame, header)

                self.client.send(frame)
            else:
                header = bytes(STREAM_END_DATATYPE, ENCODING, ENCODING_ERROR_TYPE)
                msg = str.encode(f"{self.username} stopped streaming.", ENCODING, ENCODING_ERROR_TYPE)
                self.client.send(encapsulate(msg, header))

                print("Stream ended.")
                break

    def stopstream(self):
        if self.streaming:
            self.streaming = False
        else:
            print("You aren't streaming at the moment.")

    def handle_input(self, inp: str):
        # evaluate the keyboard input
        if inp == "!leave":
            self.client.close()
            return

        elif inp == "!stream":
            if self.streaming:
                print("You are already streaming, close old stream with !stopstream to start a new one.")
            else:
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


def get_ip_from_host():
    while True:
        choice = str(input("Enter host's PC name : "))
        try:
            return socket.gethostbyname(choice)
        except socket.gaierror:
            print("Invalid choice, try again.")


def get_ip() -> str:
    choice = ""
    while not re.search("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", choice, re.M | re.I):
        choice = str(input("Enter host's IP address : "))
    return choice


def join_server():
    name = str(input("Enter your online name (defaults to 'user'): "))

    while True:
        try:
            choice = int(
                input(
                    "Host IP address ?\n1) localhost (127.0.0.1)\n2) automatic connection\n3) manual connection from host's PC name\n4) manual connection from host's IP address\n"
                )
            )
        except ValueError:
            print("Invalide input, try again.")
            continue

        if choice == 1:
            host = "127.0.0.1"
            break
        elif choice == 2:
            host = ""
            break
        elif choice == 3:
            host = get_ip_from_host()
            break
        elif choice == 4:
            host = get_ip()
            break
        else:
            print("Invalide choice, try again.")

    port = input(f"Port (leave blank for {DEFAULT_PORT}): ")
    port = int(port) if port else DEFAULT_PORT
    name = name.replace(" ", "_") or "user"

    client_thread = ClientThread(host, port, name)

    client_thread.join()
    client_thread.kthread.stop()

    main()


# -----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------- MAIN PROGRAMM -----------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


hosted_server = None


def main():
    global hosted_server

    while True:
        choice = int(input("1) Host a server\n2) Join a chat server\n3) Quit\n"))
        if choice == 1:
            if hosted_server:
                print("Can only host 1 server.")
            else:
                hosted_server = host_server()
        elif choice == 2:
            join_server()
            break
        elif choice == 3:
            return
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ IMPORTS --------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

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

DEFAULT_PORT = 8008

ENCODING = "utf-16le"
ENCODING_ERROR_TYPE = "backslashreplace"
VIDEO_CODEC = cv2.VideoWriter_fourcc(*"XVID")

MSG_DATATYPE = "1"
IMG_STREAM_DATATYPE = "2"
STREAM_END_DATATYPE = "3"

CAPSULE_SIZE = 500
NAME_MAX_LENGTH = 100

DEBUG = True

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

        self.host_client = None

        self.establish_server_connection()

        self.auth_thread = threading.Thread(target=self.authentification_thread, daemon=False)
        self.auth_thread.start()

    def establish_server_connection(self):
        """Creates the server with the provided ip and port number."""
        try:
            self.server: socket.SocketType = socket.create_server((self.host_address, self.host_port))
        except socket.error as e:
            print(e)

        self.server.listen(self.max_connections)
        print(f"Socket successfully bound to {self.host_address}:{self.host_port} and listening.\n")

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

                print(msg := f"Server message : '{connection.name}' ({connection.address[0]}:{connection.address[1]}) connected to the server.")
                date = get_time()
                self.log(f"{date} - {msg}")

                self.send_everyone(f"{connection.name} joined the chat !")

        print("Authentification thread stopped.")

    def send_everyone(self, msg: Union[str, bytes], encode: bool = True):
        """Sends a message to every clients of the server."""
        for conn in self.connections:
            conn.send_msg(msg, encode=encode)

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

        else:  # client is not an administator
            response_msg = "You are not an administrator."
        connection.send_msg(response_msg)

    def is_administator(self, connection: Connection) -> bool:
        """Returns whether or not the connection is an administator of the server."""
        return self.host_client and self.host_client.getpeername() == connection.client.getsockname() and self.host_client.getsockname() == connection.client.getpeername()

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

        date = get_time()
        msg = f"{date} - {connection.name}: {res}"

        self.log(msg)

        for conn in self.connections:
            if conn is not connection and conn.is_up():
                conn.send_msg(msg)

    def handle_stream(self, connection: Connection, encapsulated_frame: bytes):
        if connection.streaming == False:
            connection.streaming = True
            connection.stream_count += 1

            out = self._create_video_writer(f"{connection.name}{connection.stream_count}")
            self.video_logers[connection.name] = out

            self.log(f"{get_time()}: {connection.name} started streaming.")

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

        self.log(f"{get_time()}: {connection.name} stopped streaming.")

    def close_server(self):
        """Properly closes the server."""

        self.alive = False
        for conn in self.connections:
            conn.send_msg("Server is shutting down, you are going to be disconnected.")
            conn.close()
        self.server.close()
        print("Server closed.")

    def log(self, log_msg: str):
        """Write a message to the log file."""

        with io.open(f"__log_{self.host_address}-{self.host_port}.log", "a", encoding=ENCODING, errors=ENCODING_ERROR_TYPE) as f:
            try:
                f.write(f"{log_msg}\n")
            except UnicodeEncodeError:
                print(f"Failed to log message : {log_msg}")

    def video_log(self, frame: bytes, connection: Connection):
        try:
            frame = bytes_to_array(frame)
        except ValueError:
            return
        self.video_logers[connection.name].write(frame)

    def _create_video_writer(self, name: str, resolution=(1920, 1080), fps=15.0):
        return cv2.VideoWriter(f"__log_{self.host_address}-{self.host_port}-{name}.avi", VIDEO_CODEC, fps, resolution)


def host_server() -> socket.SocketType:
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

    return Server(ip, port, password)


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


class Client:
    def __init__(self, host_address, host_port, name):
        self.host_address = host_address
        self.host_port = host_port
        self.username = name

        self.closed_streams = []
        self.streaming = False
        self.streamcount = 0

        self.message_thread = threading.Thread(target=self.message_reception_thread, daemon=True)

        self.establish_client_connection()
        self.kthread = KeyboardThread(self.handle_input)

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
            self.username = self.client.recv(1024).decode(ENCODING)
            self.message_thread.start()

        except socket.error as e:
            print(e)
        print()

    def message_reception_thread(self):
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
            except Exception as e:
                if DEBUG:
                    print(e)
                continue

    def handle_input(self, inp: str):
        """Callback called every time an keyboard input is sent that evaluates that input
        and does actions accordingly."""

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

            print("Stream ended.")
        else:
            print("You aren't streaming at the moment.")


def get_ip_from_host():
    while True:
        choice = str(input("Enter host's PC name : "))
        try:
            return socket.gethostbyname(choice)
        except socket.gaierror:
            print("Invalid host, try again.")


def chose_ip() -> str:
    choice = ""
    while not re.search("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", choice, re.M | re.I):
        choice = str(input("Enter host's IP address : "))
    return choice


def chose_server(servers: list) -> str:
    for i, server in enumerate(servers):
        print(f"{i+1} : {server} - {socket.gethostbyaddr(server)[0]}")

    while True:
        try:
            choice = int(input("Chose an ip from the list above : "))
        except ValueError:
            print("Invalide input, try again.")
            continue

        if 1 <= choice <= len(servers):
            return servers[choice - 1]

        print("Invalide choice, try again.")
        continue


def join_server():
    name = str(input("Enter your online name (defaults to 'user'): "))[:NAME_MAX_LENGTH]

    port = input(f"Port (leave blank for {DEFAULT_PORT}): ")
    port = int(port) if port else DEFAULT_PORT

    while True:
        try:
            choice = int(
                input(
                    "Host IP address ?\n1) localhost (127.0.0.1)\n2) automatic connection\n3) manual connection from host's PC name\n4) manual connection from host's IP address\n5) scan available servers\n"
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
            host = chose_ip()
            break
        elif choice == 5:
            if servers := get_servers(port):
                host = chose_server(servers)
                break
            else:
                print("No servers are currently available.")
                return
        else:
            print("Invalide choice, try again.")

    name = name.replace(" ", "_") or "user"

    client = Client(host, port, name)
    client.message_thread.join()

    client.kthread.stop()

    main()


# -----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------- MAIN PROGRAMM -----------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


hosted_server = None


def main():
    global hosted_server

    while True:
        try:
            choice = int(input("1) Host a server\n2) Join a chat server\n3) Quit\n"))
        except ValueError:
            print("Invalide input, try again.")
            continue

        if choice == 1:
            if hosted_server:
                print("You can only host 1 server.")
            else:
                hosted_server = host_server()
        elif choice == 2:
            join_server()
            break
        elif choice == 3:
            if hosted_server:
                hosted_server.close_server()
            quit()
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()

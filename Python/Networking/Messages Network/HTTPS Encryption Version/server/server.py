from helpers import *

import socket
from typing import Optional, Union
import io
import threading
import cv2


class Connection:
    """Class representing a connection from the server side, wich is a couple client-address-name"""

    def __init__(self, client: socket.SocketType, address: str, name: Optional[str] = None):
        self.name = name
        self.client = client
        self.address = address

        self.streaming = False
        self.stream_count = 0

    def send(self, data: Union[str, bytes], encode: bool = False, encrypt: bool = True):
        """Send a message to the client side of the connection.
        There is option to encode or not the message."""

        data = data.encode(ENCODING, ENCODING_ERROR_TYPE) if encode else data
        data = byte_xor(data, self.encryption_key) if encrypt else data
        try:
            self.client.sendall(data)
        except ConnectionError:
            return

    def send_msg(self, msg: Union[str, bytes], encode: bool = True, encrypt: bool = True):
        """Send a message to the client side of the connection.
        There is option to encode or not the message."""

        msg = msg.encode(ENCODING, ENCODING_ERROR_TYPE) if encode else msg
        msg = encapsulate(msg, bytes(MSG_DATATYPE, ENCODING))
        msg = byte_xor(msg, self.encryption_key) if encrypt else msg

        self.client.sendall(msg)

    def receive(self, packet_size: int = 2048, decode: bool = True, decrypt: bool = True) -> Union[str, bytes]:
        """Receives a message to the client side of the connection.
        There is option to decode or not the message."""
        try:
            raw = self.client.recv(packet_size)
            data = raw.decode(ENCODING) if decode else raw
            return byte_xor(data, self.encryption_key) if decrypt else data
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
    def __init__(
        self, ui, host_address: str, host_port: str, password: str, rsa_public_exp: int, rsa_private_exp: int, rsa_modulo: int, debug: bool = False, max_connections: int = 50
    ):
        self.alive = True
        self.debug = debug

        self.ui = ui

        self.host_address = host_address
        self.host_port = host_port
        self.password = password
        self.password_protected = password != ""

        self.rsa_public_exp = rsa_public_exp
        self.rsa_private_exp = rsa_private_exp
        self.rsa_modulo = rsa_modulo

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
            self.ui.print_to_admin(e)

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
                    connection.send(BANNED_MESSAGE, encode=True, encrypt=False)
                    connection.close()
                    del connection
                    continue

                if self.password_protected:  # server has a password
                    connection.send("1", encode=True, encrypt=False)
                    password = connection.receive(decrypt=False)
                    if password != self.password:  # client did not provide the right password
                        connection.send(INVALID_PASSWORD, encode=True, encrypt=False)
                        connection.close()
                        del connection
                        continue
                    connection.send("Password correct.", encode=True, encrypt=False)
                else:  # server is password free
                    connection.send("0", encode=True, encrypt=False)

                name = connection.receive(decrypt=False)
                if name is None or name == "":
                    continue

                while name in [conn.name for conn in self.connections if conn != connection]:
                    name = f"{name}_"

                connection.send(name, encode=True, encrypt=False)
                connection.name = name

                public_key = bytes(f"{self.rsa_public_exp},{self.rsa_modulo}", ENCODING, ENCODING_ERROR_TYPE)
                connection.send(public_key, encrypt=False)

                xor_key = connection.receive(decrypt=False)
                xor_key = decode_xor_key(xor_key, self.rsa_private_exp, self.rsa_modulo).encode(ENCODING, ENCODING_ERROR_TYPE)
                connection.encryption_key = xor_key

                self.connections.append(connection)

                # starts a thread to handle the communication between the server and the client.
                thread = threading.Thread(target=self.connection_handler, args=(connection,), daemon=True)
                thread.start()

                thread.name = connection.name

                self.ui.print_to_admin(
                    msg := f"<font color=red>Server message</font> : '{connection.name}' ({connection.address[0]}:{connection.address[1]}) connected to the server."
                )
                date = get_full_time()
                self.log(f"{date} - {msg}")

                self.send_everyone(f"<font color=blue>{connection.name}</font> joined the chat !")

        self.ui.print_to_admin("Authentification thread stopped.")

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
            self.ui.print_to_admin(msg)

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
        self.ui.print_to_admin(response_msg)

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
        self.ui.print_to_admin(response_msg)

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
                if self.debug:
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
        self.ui.print_to_admin(msg)

        date = get_full_time()
        log_msg = f"{date} - '{connection.name}' ({connection.address[0]}:{connection.address[1]}) disconnected from the server."
        self.log(log_msg)

        self.send_everyone(f"<font color=blue>{connection.name}</font> left the chat !")

        del connection

    def handle_message(self, connection: Connection, res: str):
        if res in {"!list names", "!list users"}:  # command to list the name of all connected users
            connection.send_msg(msg := f"Online users : <font color=blue>{'</font>, <font color=blue>'.join([conn.name for conn in self.connections])}</font>")
            date = get_full_time()
            self.ui.print_to_admin(f"{date} - {msg}")
            return

        if res.startswith("!send ") and len(parts := res.split(" ")[1:]) >= 2:  # command to send private message to other users
            target_name = parts[0]
            content = " ".join(parts[1:])
            self.send_pm(connection, target_name, content)
            return

        msg = f"""<strong>{get_time()} - <font color=blue>{connection.name}</font> ~</strong> {res}"""
        log_msg = f"{get_full_time()} - {connection.name}: {res}"

        self.log(log_msg)
        self.ui.print_to_admin(msg)

        for conn in self.connections:
            if conn is not connection and conn.is_up():
                conn.send_msg(msg)

    def handle_stream(self, connection: Connection, encapsulated_frame: bytes):
        if connection.streaming == False:
            connection.streaming = True
            connection.stream_count += 1

            out = self._create_video_writer(f"{connection.name}{connection.stream_count}")
            self.video_logers[connection.name] = out

            for conn in self.connections:
                if conn is not connection and conn.is_up():
                    conn.send_msg(f"{get_time()} - <font color=green>{connection.name}</font> started streaming.")

            log_msg = f"{get_full_time()}: {connection.name} started streaming."
            self.log(log_msg)

            log_msg_html = f"{get_full_time()}: <font color=blue>{connection.name}</font> started streaming."
            self.ui.print_to_admin(log_msg_html)

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
                conn.send_msg(f"{get_time()} - <font color=green>{connection.name}</font> stopped streaming.")

        log_msg = f"{get_full_time()}: {connection.name} stopped streaming."
        self.log(log_msg)

        log_msg_html = f"{get_full_time()}: <font color=blue>{connection.name}</font> stopped streaming."
        self.ui.print_to_admin(log_msg_html)

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
        self.ui.print_to_admin("Server closed.")

    def log(self, log_msg: str):
        """Write a message to the log file."""

        with io.open(f"__log_{self.host_address}-{self.host_port}.log", "a", encoding=ENCODING, errors=ENCODING_ERROR_TYPE) as f:
            try:
                f.write(f"{log_msg}\n")
            except UnicodeEncodeError:
                self.ui.print_to_admin(f"Failed to log message : {log_msg}")

    def video_log(self, frame: bytes, connection: Connection):
        try:
            frame = bytes_to_array(frame)
        except ValueError:
            return
        self.video_logers[connection.name].write(frame)

    def _create_video_writer(self, name: str, resolution=(1920, 1080), fps=15.0):
        return cv2.VideoWriter(f"__log_{self.host_address}-{self.host_port}-{name}.avi", VIDEO_CODEC, fps, resolution)

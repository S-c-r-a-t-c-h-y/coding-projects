import socket
import threading

import os
import re
import time
import datetime

try:
    from requests import get
except ImportError:
    os.system("pip install requests")
    print("Package installing...")
    time.sleep(5)
    print("Package installed !")
    from requests import get


def get_time():
    return datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")


INVALID_PASSWORD = "Invalid password."

# -----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------- SERVER SIDE ------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


def get_ip_adresses():
    """Returns a list of all the ip adresses of the local network"""
    devices = []
    for device in os.popen("arp -a"):
        device = re.search("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", device, re.M | re.I)
        if device is not None:
            devices.append(device.group(0))
    return devices


class Connection:
    def __init__(self, client, address, name=None):
        self.name = name
        self.client = client
        self.address = address

    def send(self, msg, encode=True):
        msg = msg.encode("utf-8") if encode else msg
        self.client.sendall(msg)

    def receive(self, packet_size=2048, decode=True):
        return self.client.recv(packet_size).decode("utf-8") if decode else self.client.recv(packet_size)

    def is_up(self):
        return self.client.fileno() != -1

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            print(f"Error while closing client {self.name} :\n{e}")


class ServerThread(threading.Thread):
    def __init__(self, host_address, host_port, password, max_connections=50):
        self.host_address = host_address
        self.host_port = host_port
        self.password = password
        self.password_protected = password != ""

        self.max_connections = max_connections
        self.connections = []

        self.establish_server_connection()

        super().__init__(name="Server Thread")
        self.daemon = False
        self.start()

    def establish_server_connection(self):
        try:
            self.server = socket.create_server((self.host_address, self.host_port))
        except socket.error as e:
            print(e)

        self.server.listen(self.max_connections)
        print(f"Socket successfully bound to {self.host_address}:{self.host_port} and listening.\n")

    def send_everyone(self, msg, encode=True):
        for conn in self.connections:
            conn.send(msg, encode=encode)

    def run(self):
        while True:
            client, address = self.server.accept()
            connection = Connection(client, address)
            if connection not in self.connections:

                if self.password_protected:
                    connection.send("1")
                    password = connection.receive()
                    if password != self.password:
                        connection.send(INVALID_PASSWORD)
                        connection.close()
                        del connection
                        continue
                    connection.send("Password correct.")
                else:
                    connection.send("0")

                self.connections.append(connection)
                threading.Thread(target=self.connection_handler, args=(connection,), daemon=False).start()

                time.sleep(0.1)
                print(msg := f"Server message : '{connection.name}' ({connection.address[0]}:{connection.address[1]}) connected to the server.")
                date = get_time()
                self.log(f"{date} - {msg}")

                self.send_everyone(f"{connection.name} joined the chat !")

    def connection_handler(self, connection):
        """Thread handling the communication with a client of the server"""
        name = connection.receive()
        connection.name = name

        time.sleep(0.5)

        while connection.is_up():
            try:
                data = connection.receive(decode=False)
                decoded = data.decode("utf-8")
            except Exception as e:  # connection has been closed
                break

            if decoded in ["!list names", "!list users"]:
                connection.send(msg := f"Online users : {', '.join([conn.name for conn in self.connections])}")
                date = get_time()
                self.log(f"{date} - {msg}")
                continue

            date = get_time()
            msg = f"{date} - {name}: {decoded}"

            self.log(msg)

            for conn in self.connections:
                if conn is not connection:
                    conn.send(msg)

        # the connection has been lost or closed
        # removes the client from the connections list and logs it

        connection.close()
        self.connections.remove(connection)

        print(msg := f"Server message : '{connection.name}' ({connection.address[0]}:{connection.address[1]}) disconnected from the server.")
        date = get_time()
        self.log(f"{date} - {msg}")

        self.send_everyone(f"{connection.name} left the chat !")

        del connection

    def log(self, log_msg):
        with open(f"__log_{self.host_address}-{self.host_port}.txt", "a") as f:
            f.write(f"{log_msg}\n")


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

    port = input("Port (leave blank for 8008): ")
    port = int(port) if port else 8008

    password = str(input("Enter a password (leave blank for no password) : "))

    server_thread = ServerThread(ip, port, password)


# -----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------- CLIENT SIDE ------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


class KeyboardThread(threading.Thread):
    def __init__(self, input_cbk=None, *, name="keyboard-input-thread"):
        self.input_cbk = input_cbk
        self.running = True
        super().__init__(name=name)
        self.daemon = True
        self.start()

    def run(self):
        while self.running:
            self.input_cbk(str(input()))  # waits to get input + Return


class ClientThread(threading.Thread):
    def __init__(self, host_address="127.0.0.1", host_port="8008", name="user"):
        self.host_address = host_address
        self.host_port = host_port
        self.username = name

        super().__init__(name=name)
        self.daemon = True

        self.establish_client_connection()
        self.kthread = KeyboardThread(self.handle_input)

    def run(self):
        if self.denied:
            return
        print("Connection established with the server.")

        while self.client.fileno() != -1:
            try:
                res = self.client.recv(1024)
                print(res.decode("utf-8"))
            except:
                print("Connection closed.")
                break

    def establish_client_connection(self):
        print("Waiting for connection response")
        try:
            self.denied = False
            self.client = socket.create_connection((self.host_address, self.host_port))

            if (response := self.client.recv(1024).decode("utf-8")) == "1":  # server has a password
                self.client.send(str(input("Enter server password : ")).encode("utf-8"))
                print(response := self.client.recv(1024).decode("utf-8"))
                if response == INVALID_PASSWORD:
                    print("Connection denied.")
                    self.denied = True
            self.client.send(self.username.encode("utf-8"))
            self.start()
        except socket.error as e:
            print(e)
        print()

    def handle_input(self, inp):
        # evaluate the keyboard input
        if inp == "!leave":
            self.client.close()
            return

        self.client.send(str.encode(inp))


def get_ip_from_host():
    while True:
        choice = str(input("Enter host's PC name : "))
        try:
            return socket.gethostbyname(choice)
        except socket.gaierror:
            print("Invalid choice, try again.")


def get_ip():
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

    port = input("Port (leave blank for 8008): ")
    port = int(port) if port else 8008
    name = name or "user"

    client_thread = ClientThread(host, port, name)

    client_thread.join()
    client_thread.kthread.running = False
    main()


# -----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------- MAIN PROGRAMM -----------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


hosting = False


def main():
    global hosting

    while True:
        choice = int(input("1) Host a server\n2) Join a chat server\n3) Quit\n"))
        if choice == 1:
            if hosting:
                print("Can only host 1 server.")
            else:
                hosting = True
                host_server()
        elif choice == 2:
            join_server()
            break
        elif choice == 3:
            return
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()

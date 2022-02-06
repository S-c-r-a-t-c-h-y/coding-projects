import socket
import threading
from requests import get
import os
import re


def get_ip_adresses():
    """Returns a list of all the ip adresses of the local network"""
    devices = []
    for device in os.popen("arp -a"):
        device = re.search("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", device, re.M | re.I)
        if device is not None:
            devices.append(device.group(0))
    return devices


class ServerThread(threading.Thread):
    def __init__(self, host_address, host_port, max_connections=50):
        self.host_address = host_address
        self.host_port = host_port
        self.max_connections = max_connections
        self.connections = []

        self.server = socket.socket()
        self.establish_server_connection()

        super().__init__(name="Server Thread")
        self.daemon = False
        self.start()

    def establish_server_connection(self):
        try:
            self.server.bind((self.host_address, self.host_port))
        except socket.error as e:
            print(e)

        self.server.listen(self.max_connections)
        print(f"Socket successfully bound to {self.host_address}:{self.host_port} and listening.\n")

    def run(self):
        while True:
            client, address = self.server.accept()
            if (client, address) not in self.connections:
                self.connections.append((client, address))

                print(f"Server message : {address[0]}:{address[1]} connected to the server.")

                threading.Thread(target=self.connection_handler, args=(client,), daemon=False).start()

    def connection_handler(self, connection):
        """Thread handling the communication with a client of the server"""
        name = connection.recv(2048).decode("utf-8")
        while connection.fileno() != -1:
            try:
                data = connection.recv(2048)
                decoded = data.decode("utf-8")
            except:  # connection has been closed
                break

            for client, _ in self.connections:
                if client is not connection:
                    client.sendall(f"{name} sent : {decoded}".encode("utf-8"))


def host_server():
    while True:
        choice = int(input("Hosting ip address ?\n1) localhost (127.0.0.1)\n2) machine ip address\n"))
        if choice == 1:
            ip = "127.0.0.1"
            break
        elif choice == 2:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            break
        else:
            print("Invalide choice, try again.")

    # ip = get("https://api.ipify.org").text

    port = input("Port (leave blank for 8008): ")
    port = port or 8008

    server_thread = ServerThread(ip, port)
    main()


# -----------------------------------------------------------------------------------------------------------------------


class KeyboardThread(threading.Thread):
    def __init__(self, input_cbk=None, *, name="keyboard-input-thread"):
        self.input_cbk = input_cbk
        super().__init__(name=name)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            self.input_cbk(input())  # waits to get input + Return


class ClientThread(threading.Thread):
    def __init__(self, host_address="127.0.0.1", host_port="8008", name="user"):
        self.host_address = host_address
        self.host_port = host_port
        self.username = name

        self.client = socket.socket()
        self.establish_client_connection()

        super().__init__(name=name)
        self.daemon = True
        self.start()

    def run(self):
        while self.client.fileno() != -1:
            try:
                res = self.client.recv(1024)
                print(res.decode("utf-8"))
            except:
                print("Connection closed.")

    def establish_client_connection(self):
        print("Waiting for connection response")
        try:
            self.client.connect((self.host_address, self.host_port))
            self.client.send(self.username.encode("utf-8"))
            print("Connection established with the server.")
        except socket.error as e:
            print(e)
        print()

    def handle_input(self, inp):
        # evaluate the keyboard input
        if inp == "leave":
            self.client.close()
            return

        self.client.send(str.encode(inp))


def join_server():
    name = str(input("Enter your online name (defaults to 'user'): "))
    host = input("Host IP adress (leave blank for localhost): ")
    port = input("Port (leave blank for 8008): ")

    host = host or "127.0.0.1"
    port = port or 8008
    name = name or "user"

    client_thread = ClientThread(host, port, name)
    kthread = KeyboardThread(client_thread.handle_input)

    client_thread.join()


hosting = False


def main():
    global hosting

    while True:
        choice = int(input("1) Host a server\n2) Join a chat server\n"))
        if choice == 1:
            if hosting:
                print("Can only host 1 server.")
            else:
                hosting = True
                host_server()
                break
        elif choice == 2:
            join_server()
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()

import socket
import os
import threading
from requests import get

server = socket.socket()


def establish_connection(ip_adress, port):
    try:
        server.bind((ip_adress, port))
    except socket.error as e:
        print(e)

    server.listen(5)
    print(f"Socket successfully bound to {ip_adress}:{port} and listening.")


def connection_handler(connection):
    name = connection.recv(2048).decode("utf-8")
    while connection.fileno() != -1:
        try:
            data = connection.recv(2048)
            decoded = data.decode("utf-8")
        except:  # connection has been closed
            break

        for client, _ in connections:
            if client is not connection:
                client.sendall(f"{name} sent : {decoded}".encode("utf-8"))


connections = []


def receive_connection():
    while True:
        client, address = server.accept()
        if (client, address) not in connections:
            connections.append((client, address))

            print(f"{address[0]}:{address[1]} connected to the server.")

            threading.Thread(target=connection_handler, args=(client,), daemon=False).start()


def main():
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

    pt = input("Port (leave blank for 8008): ")
    port = pt or 8008

    establish_connection(ip, port)

    t1 = threading.Thread(target=receive_connection, daemon=False)
    t1.start()
    t1.join()
    server.close()


if __name__ == "__main__":
    main()

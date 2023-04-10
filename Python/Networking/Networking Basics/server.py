import socket
import os
from _thread import *

server_side_socket = socket.socket()
host = "127.0.0.1"
port = 2004
thread_count = 0
try:
    server_side_socket.bind((host, port))
except socket.error as e:
    print(e)

print("Socket is listening..")
server_side_socket.listen(5)


def multi_threaded_client(connection, connection_nb):
    # connection.send(str.encode('Server is working:'))
    connection.sendall(str.encode(f"Server is working: connection n°{connection_nb}."))
    while True:
        data = connection.recv(2048)
        decoded = data.decode("utf-8")
        parts = decoded.split(" ")

        if len(parts) >= 3 and "send" in parts and parts[1].isdigit() and (index := int(parts[1])) <= thread_count:

            msg = " ".join(parts[2:])
            msg = f"Message from client n°{connection_nb} : {msg}"
            msg = msg.encode("utf-8")

            clients[index - 1].sendall(msg)

        response = f"Server message: {decoded}"

        # response = f"Server message: {data.decode('utf-8')}"
        if not data:
            break
        # connection.sendall(str.encode(response))
    connection.close()


clients = []

while True:
    client, address = server_side_socket.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    thread_count += 1
    start_new_thread(
        multi_threaded_client,
        (
            client,
            thread_count,
        ),
    )
    print("Thread Number: " + str(thread_count))
    if client not in clients:
        clients.append(client)
        print(client.raddr[0])

server_side_socket.close()

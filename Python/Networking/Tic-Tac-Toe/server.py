import socket
import os
from _thread import *
import time

DEBUG = False

server_side_socket = socket.socket()
inp = str(input("Enter IP adress to host the server (leave blank for localhost) : "))
host = inp or "127.0.0.1"
port = 2004
thread_count = 0
try:
    server_side_socket.bind((host, port))
except socket.error as e:
    print(e)

print("Socket is listening..")
server_side_socket.listen(5)


def multi_threaded_client(connection, connection_nb):
    connection.sendall(str.encode(f"{connection_nb}"))
    while True:
        data = connection.recv(2048)

        if DEBUG:
            print(f"{data.decode('utf-8')} received from {connection_nb}")

        if connection_nb == 1:
            clients[1].sendall(data)
            if DEBUG:
                print(f"{data.decode('utf-8')} sent to 2")
        else:
            clients[0].sendall(data)
            if DEBUG:
                print(f"{data.decode('utf-8')} sent to 1")

        if not data:
            break
    connection.close()


clients = []

while True:
    if len(clients) < 2:
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

    if clients and all(client.fileno() == -1 for client in clients):
        break

    time.sleep(0.5)


server_side_socket.close()

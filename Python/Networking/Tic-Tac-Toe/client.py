import socket

client_multi_socket = socket.socket()

inp = input("Host IP adress (leave blank for localhost): ")

host = inp or "127.0.0.1"
port = 2004

print("Waiting for connection response")
try:
    client_multi_socket.connect((host, port))
    print("Connection established with the server.")
except socket.error as e:
    print(e)

res = client_multi_socket.recv(1024)
print(res.decode("utf-8"), "\n")

while True:
    res = client_multi_socket.recv(1024)
    print(res.decode("utf-8"))

client_multi_socket.close()

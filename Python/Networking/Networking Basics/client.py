import socket
import threading


class KeyboardThread(threading.Thread):
    def __init__(self, input_cbk=None, name="keyboard-input-thread"):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input())  # waits to get input + Return


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


def callback(inp):
    # evaluate the keyboard input
    client_multi_socket.send(str.encode(inp))


# start the Keyboard thread
kthread = KeyboardThread(callback)

while True:
    res = client_multi_socket.recv(1024)
    print(res.decode("utf-8"))

client_multi_socket.close()

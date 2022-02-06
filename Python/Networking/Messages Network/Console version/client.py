import socket
import threading


class KeyboardThread(threading.Thread):
    def __init__(self, input_cbk=None, input_msg="", *, name="keyboard-input-thread"):
        self.input_cbk = input_cbk
        self.input_msg = input_msg
        super(KeyboardThread, self).__init__(name=name)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            self.input_cbk(input(self.input_msg))  # waits to get input + Return


def establish_connection(ip_adress, port, name):
    print("Waiting for connection response")
    try:
        client.connect((ip_adress, port))
        client.send(name.encode("utf-8"))
        print("Connection established with the server.")
    except socket.error as e:
        print(e)
    print()


def handle_input(inp):
    # evaluate the keyboard input
    if inp == "leave":
        client.close()
        return

    client.send(str.encode(inp))


client = socket.socket()


def main():
    name = str(input("Enter your online name (defaults to 'user'): "))
    inp = input("Host IP adress (leave blank for localhost): ")
    pt = input("Port (leave blank for 8008): ")

    host = inp or "127.0.0.1"
    port = pt or 8008
    name = name or "user"

    establish_connection(host, port, name)

    # start the Keyboard thread
    kthread = KeyboardThread(handle_input)

    while client.fileno() != -1:
        try:
            res = client.recv(1024)
            print(res.decode("utf-8"))
        except:
            print("Connection closed.")

    exit()


if __name__ == "__main__":
    main()

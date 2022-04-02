# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ IMPORTS --------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


import socket
import threading

import time

import requests

from helpers import *
from UI import ChatTab, Ui_MainWindow
from server import Server
from client import Client

# -----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------- MAIN PROGRAMM -----------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


class App:
    def __init__(self, ui):
        self.ui = ui

        self.clients = {}
        self.hosted_server = None

        self.joined_server = []

        self._client_deleting_thread = threading.Thread(target=self.remove_dead_clients_thread, daemon=True)
        self._client_deleting_thread.start()

    def join_server(self):

        name = self.ui.join_name_input.text()
        name = name.replace(" ", "_") or "user"

        host = self.ui.join_serverlist_combo_box.currentText()
        if host == DEFAULT_SERVER_MSG:
            self.ui.show_popup("Invalid server", "This server is invalid, try scanning for servers again.", icon=QMessageBox.Warning)
            return

        ip = host.split(":")[0]
        port = host.split(":")[1].split(" - ")[0]
        chat_name = f"Chat {ip}:{port}"

        if chat_name in self.clients:
            self.ui.show_popup("Error", "You are already connected to that server. Only one connection is allowed.", icon=QMessageBox.Warning)
            return

        password = self.ui.join_password_input.text()

        self.ui.chats[chat_name] = ChatTab(chat_name, self, self.ui)

        client = Client(self.ui, ip, port, name, password, self.ui.chats[chat_name])
        self.clients[chat_name] = client
        if not client.accepted:
            del self.clients[chat_name]

        index = self.ui.tab_widget.indexOf(self.ui.chats[chat_name])
        self.ui.tab_widget.setCurrentIndex(index)

    def scan_servers(self):
        port = self.ui.join_port_input.text()
        if port and port.isdigit():
            port = int(port)
        else:
            self.ui.show_popup("Invalid port", "You need to enter a valid port before scanning for servers.", icon=QMessageBox.Warning)

        if servers := get_servers(port):
            if self.ui.join_serverlist_combo_box.currentText() == DEFAULT_SERVER_MSG:
                self.ui.join_serverlist_combo_box.clear()

            for ip in servers:
                name = f"{ip}:{port} - {socket.gethostbyaddr(ip)[0]}"
                if self.ui.join_serverlist_combo_box.findText(name) == -1:
                    self.ui.join_serverlist_combo_box.addItem(name)

    def host_server(self):
        global debug

        if self.hosted_server:
            self.ui.show_popup(
                "Can't host multiple servers",
                "You are already hosting a server.",
                details=f"You host a server at the following address : {self.host_ip}:{self.host_port}",
                icon=QMessageBox.Critical,
            )
            return

        combo_box_index = self.ui.host_ip_combo_box.currentIndex()
        if combo_box_index == 0:
            ip = "127.0.0.1"
        elif combo_box_index == 1:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        elif combo_box_index == 2:
            try:
                ip = requests.get("https://api.ipify.org").text
            except requests.exceptions.ConnectionError:
                self.ui.show_popup("Failed to host server", "You do not currently have a public IP address (e.g you're not connected to internet).", icon=QMessageBox.Critical)
                return

        elif combo_box_index == 3:
            ip = ""

        port = int(self.ui.host_port_input.text())
        password = self.ui.host_password_input.text()

        debug = self.ui.debug_checkbox.isChecked()

        self.hosted_server = Server(self.ui, ip, port, password, debug)

        admin_tab = self.ui.create_admin_tab(self)

        self.host_ip = ip
        self.host_port = port
        self.ui.show_popup("Success !", f"You are currently hosting a server at the following address : {self.host_ip}:{self.host_port}", icon=QMessageBox.Information)

        index = self.ui.tab_widget.indexOf(admin_tab)
        self.ui.tab_widget.setCurrentIndex(index)

    def stop_hosting(self):

        if not self.hosted_server:
            self.ui.show_popup("Error", "You aren't hosting a server yet.", icon=QMessageBox.Warning)
            return

        self.hosted_server.close_server()
        self.hosted_server = None

        self.ui.show_popup("Success !", "You stopped hosting the server.", icon=QMessageBox.Information)
        self.ui.admin_tab.setParent(None)

    def send_msg(self, chat_name):
        chat = self.ui.chats[chat_name]
        client = self.clients[chat_name]

        if txt := chat.chat_input.text():
            chat.chat_input.setText("")

            if txt == "!clear":
                chat.clear_chat()
                return

            if txt == "!leave":
                client.handle_input(txt)
                return

            ui_txt = f"<strong>{get_time()} - <font color=purple>you</font> ~ </strong>{txt}"

            chat.print_to_chat(ui_txt, Qt.AlignRight)

            client.handle_input(txt)

    def admin_send_msg(self):
        if txt := self.ui.admin_input.text():
            self.ui.admin_input.setText("")

            if txt.startswith("!kick ") and len(parts := txt.split(" ")[1:]) >= 1:  # command to kick other users
                self.ui.print_to_admin(txt)
                target_name = parts[0]
                content = " ".join(parts[1:])
                self.hosted_server.kick(target_name, content)
                return

            if txt.startswith("!ban ") and len(parts := txt.split(" ")[1:]) >= 1:  # command to ban other users
                self.ui.print_to_admin(txt)
                target_name = parts[0]
                content = " ".join(parts[1:])
                self.hosted_server.ban(target_name, content)
                return

            txt = f"{get_time()} - [<font color=red>ADMIN</font>] {txt}"

            self.ui.print_to_admin(txt)
            self.hosted_server.send_everyone(txt)

    def stream(self, chat_name):
        chat = self.ui.chats[chat_name]
        client = self.clients[chat_name]

        button = chat.chat_start_stop_stream_button
        if button.text() == START_STREAM_UI_MSG:
            client.start_stream()
            button.setText(STOP_STREAM_UI_MSG)
        else:
            client.stop_stream()
            button.setText(START_STREAM_UI_MSG)

    def remove_dead_clients_thread(self):
        while True:
            time.sleep(2)
            dead_clients = [key for key, client in self.clients.items() if not client.is_alive()]
            for key in dead_clients:
                del self.clients[key]


def main():
    import sys

    main_app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    app = App(ui)
    ui.init_ui(app)

    MainWindow.show()

    main_app.exec_()

    # runs after the window is closed

    if app.clients:
        clients = app.clients.values()
        for client in clients:
            client.handle_input("!leave")

    if app.hosted_server:
        app.hosted_server.close_server()
        exit()


if __name__ == "__main__":
    main()

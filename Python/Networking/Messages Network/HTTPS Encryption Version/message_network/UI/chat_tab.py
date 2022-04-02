from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from helpers.constants import START_STREAM_UI_MSG


class ChatTab(QtWidgets.QWidget):
    def __init__(self, name, app, ui):
        self._name = name
        self._app = app

        QtWidgets.QWidget.__init__(self)
        self.setObjectName(name)

        self.gridLayoutWidget_2 = QtWidgets.QWidget(self)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 9, 951, 711))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.chat_layout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_layout.setObjectName("chat_layout")
        self.chat_send_button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chat_send_button.setFont(font)
        self.chat_send_button.setText("Send")
        self.chat_send_button.setShortcut("")
        self.chat_send_button.setObjectName("chat_send_button")
        self.chat_layout.addWidget(self.chat_send_button, 2, 2, 1, 1)
        self.chat_input = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chat_input.setFont(font)
        self.chat_input.setText("")
        self.chat_input.setPlaceholderText("Type here and hit enter to send message.")
        self.chat_input.setObjectName("chat_input")
        self.chat_layout.addWidget(self.chat_input, 2, 0, 1, 1)
        self.chat_start_stop_stream_button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chat_start_stop_stream_button.setFont(font)
        self.chat_start_stop_stream_button.setText(START_STREAM_UI_MSG)
        self.chat_start_stop_stream_button.setObjectName("chat_start_stop_stream_button")
        self.chat_layout.addWidget(self.chat_start_stop_stream_button, 2, 3, 1, 1)
        self.chat_browser = QtWidgets.QTextBrowser(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Source Code Pro")
        font.setPointSize(10)
        self.chat_browser.setFont(font)
        self.chat_browser.setHtml(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'Source Code Pro'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
            '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>'
        )
        self.chat_browser.setOpenExternalLinks(True)
        self.chat_browser.setSearchPaths(["../data/"])
        self.chat_browser.setObjectName("chat_browser")
        self.chat_layout.addWidget(self.chat_browser, 1, 0, 1, 4)

        ui.tab_widget.addTab(self, self._name)

        self.chat_input.returnPressed.connect(lambda: self._app.send_msg(self._name))
        self.chat_send_button.clicked.connect(lambda: self._app.send_msg(self._name))
        self.chat_start_stop_stream_button.clicked.connect(lambda: self._app.stream(self._name))

    def clear_chat(self):
        self.chat_browser.clear()

    def print_to_chat(self, msg="", align=Qt.AlignLeft):
        self.chat_browser.append(str(msg))
        # self.chat_browser.setAlignment(align)

    def align_left(self):
        self.chat_browser.setAlignment(Qt.AlignLeft)

    def align_right(self):
        self.chat_browser.setAlignment(Qt.AlignRight)

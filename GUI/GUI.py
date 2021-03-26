import sys
import API

from PyQt5 import QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QFileDialog
)


class ServiceListener(QObject):
    def __init__(self):
        super().__init__()
        self.state = 0

    def run(self):
        listener_thread = QThread.currentThread()
        while getattr(listener_thread, "listening", True):
            message = API.Listen()
            print(message)
            API.Send({"state": self.state})


class Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 450, 300)
        self.setStyleSheet("background-color: lightblue")
        self.setWindowTitle("MyAntivirus")

        self.button_start_scan = QPushButton("Start scan", self)
        self.button_start_scan.setFixedSize(100, 50)
        self.button_start_scan.move(10, 240)
        self.button_start_scan.setStyleSheet("QPushButton{"
                                             "background-color: white;"
                                             "border-style: outset;"
                                             "border-width: 1px;"
                                             "border-radius: 10px;"
                                             "font: arial 10px;"
                                             "padding: 6px;"
                                             "border-radius: 10px}"
                                             "QPushButton:pressed {border-style: inset}")

        self.button_stop_scan = QPushButton("Stop scan", self)
        self.button_stop_scan.setFixedSize(100, 50)
        self.button_stop_scan.move(120, 240)
        self.button_stop_scan.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "border-style: outset;"
                                            "border-width: 1px;"
                                            "border-radius: 10px;"
                                            "font: arial 10px;"
                                            "padding: 6px;"
                                            "border-radius: 10px}"
                                            "QPushButton:pressed {border-style: inset}")

        self.button_quarantine = QPushButton("Move to \nquarantine", self)
        self.button_quarantine.setFixedSize(100, 50)
        self.button_quarantine.move(230, 240)
        self.button_quarantine.setStyleSheet("QPushButton{"
                                             "background-color: white;"
                                             "border-style: outset;"
                                             "border-width: 1px;"
                                             "border-radius: 10px;"
                                             "font: arial 10px;"
                                             "padding: 6px;"
                                             "border-radius: 10px}"
                                             "QPushButton:pressed {border-style: inset}")

        self.button_delete = QPushButton("Delete", self)
        self.button_delete.setFixedSize(100, 50)
        self.button_delete.move(340, 240)
        self.button_delete.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "border-style: outset;"
                                         "border-width: 1px;"
                                         "border-radius: 10px;"
                                         "font: arial 10px;"
                                         "padding: 6px;"
                                         "border-radius: 10px}"
                                         "QPushButton:pressed {border-style: inset}")

        self.button_start_scan.clicked.connect(self.buttonStartClicked)
        self.button_stop_scan.clicked.connect(self.buttonStopClicked)

        self.label_path = QLabel("Scan path: ", self)
        self.label_path.setFixedSize(440, 20)
        self.label_path.move(5, 5)
        self.label_path.setStyleSheet("background-color: white")
        self.label_path.setFont(QtGui.QFont('Arial', 10))

        self.show()

        self.listener_thread = QThread()
        self.service_listener = ServiceListener()
        self.service_listener.moveToThread(self.listener_thread)
        self.listener_thread.started.connect(self.service_listener.run)

    def buttonStartClicked(self):
        scan_path = QFileDialog.getExistingDirectory(self, "Choose directory", ".")
        self.label_path.setText("Scan path: " + scan_path)
        API.Send({"state": 1,
                  "path": scan_path})
        self.service_listener.state = 1
        self.listener_thread.start()


    def buttonStopClicked(self):
        self.service_listener.state = 0
        #self.listener_thread.listening = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

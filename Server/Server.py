import API
import time
import queue

from PyQt5.QtCore import QThread, QObject
from threading import Thread, currentThread
from multiprocessing import Process


class Scanner(QObject):

    def __init__(self):
        super().__init__()

    def run(self, file_queue):
        scanner_thread = QThread.currentThread()
        while getattr(scanner_thread, "scanning", True):
            itter = 1


# def listen(message_queue):
#     while True:
#         request = API.Listen()
#         print(request)
#         message_queue.put_nowait(request)
#         if request["action"] == "Start scan":
#             scanner_thread.start()
#         elif request["state"] == 0:
#             scanner_thread.scanning = False


if __name__ == '__main__':
    global scanner_thread
    file_queue = queue.Queue()

    request = None
    while not request:
        request = API.Listen()
        print(request)
    if request["state"] == 1:
        print("ololol")
        scanner_thread = QThread()
        scanner_thread.start()

    while True:
        if request["state"] == 1:
            request = API.SendAndWaitForResponse({file_queue.get(): 0})
            print(request)
        if request["state"] == 0:
            print('olololol')
            scanner_thread.join()
            break


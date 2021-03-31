import API
import time

from threading import Thread, currentThread


def Scan():
    global result

    scan_thread = currentThread()
    while getattr(scan_thread, "scanning", True):
        for i in range(100):
            result = i


if __name__ == '__main__':
    scanner_thread = Thread(target=Scan())
    scanner_thread.start()
    scanner_thread.scanning = True

    while True:
        request = API.Listen()
        print(request)
        if request['state'] == 1:
            API.Send({"state": "ready"})
            result = 1
        if request['state'] == 0:
            scanner_thread.scanning = False
        if request['state'] == 2:
            API.Send({"state": "scanning"})

from multiprocessing.connection import Client
from multiprocessing.connection import Listener

server = ('localhost', 6000)
client = ('localhost', 6001)


def SendAndWaitForResponse(request: dict) -> bool or dict:
    with Client(server) as connection:
        connection.send(request)
    with Listener(client) as listener:
        with listener.accept() as connection:
            try:
                return connection.recv()
            except EOFError:
                return False


def Send(request: dict):
    with Client(server) as connection:
        connection.send(request)


def Listen() -> bool or dict:
    with Listener(client) as listener:
        with listener.accept() as connection:
            try:
                return connection.recv()
            except EOFError:
                return False

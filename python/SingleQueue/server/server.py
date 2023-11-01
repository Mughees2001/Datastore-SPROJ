from typing import List, Dict, Tuple
from lib.RapidQueue import RapidQueue
from socket import socket, AF_INET, SOCK_STREAM


class Server:
    def __init__(self, host : str, port : str):
        self.store: RapidQueue = RapidQueue()
        self.clients: Dict[Tuple, socket] = dict()
        self.host = host
        self.port = int(port)

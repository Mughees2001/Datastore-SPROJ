from UpdatedCode.lib.hashedQueue import MultipleHashQueue
from UpdatedCode.lib.log import logger

from typing import List
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class Master:
    def __init__(
        self, initial_size: int = 2, host: str = "localhost", port: int = 8080
    ):
        """__summary__
            Initializes a master that interacts with one client only.

        Args:
            initial_size (int, optional): _description_. Defaults to 2.
            host (str, optional): _description_. Defaults to "localhost".
            port (int, optional): _description_. Defaults to 8080.
        """
        self.store = MultipleHashQueue(initial_size)
        self.host = host
        self.port = port

        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.bind((self.host, self.port))
        except OSError:
            logger.error("Port already in use")
            exit(1)

        logger.info(f"Server started on {self.host}:{self.port}")

        self.threads: List[Thread] = list()
        
        

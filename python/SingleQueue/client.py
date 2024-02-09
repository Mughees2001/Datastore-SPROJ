from typing import List, Optional
from lib.log import logger  # Changed to relative import
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from time import time, sleep
from sys import argv


class Client:
    def __init__(self, host: str = "localhost", port: str = "8009"):
        self.host: str = host
        self.port: int = int(port)
        self.running: bool = True
        self.id: Optional[str] = None
        self.connect()

        id_mess = self.socket.recv(4096).decode()
        print(id_mess)
        # logger.debug(f"Recieved ID request from server. ID is {self.id}")

        if self.id:
            msg = self.id
            self.socket.send(msg.encode())
        else:
            msg = "-1"
            self.socket.send(msg.encode())
            id = self.socket.recv(4096).decode()
            self.id = id.split(":")[-1]
            # logger.debug(f"ID recieved. Client ID is now {self.id}")

    def connect(self):
        self.socket: socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        self.socket.connect((self.host, self.port))
        logger.debug(f"Connected to {self.host}:{self.port}")

    def close(self):
        self.socket.close()
        logger.debug(f"Closed connection to {self.host}:{self.port}")

    def get(self, key: str) -> str:
        """
        Summary:
            Gets the value of a key from the server
        Args:
            key (string): contains the key to be searched

        Returns:
            string: returns the value of the key if found, else returns "MISS". If no key is provided, returns "Please enter a key"
        """
        if key:
            message = "GET " + key + "\n"
            self.socket.send(message.encode())
            res: str = self.socket.recv(4096).decode()
            return res
        else:
            return ""

    def put(self, key: str, value: bytes) -> None:
        """
        Sends a PUT request to the server with the specified key and value.

        Args:
            key (str): The key to store the value under.
            value (bytes): The value to store.

        Returns:
            None
        """
        # logger.debug(f"Request timestamp {time()}")
        self.socket.send(f"PUT {key} {value.decode()}\n".encode())

    def delete(self, key: str) -> None:
        """
        Deletes a key from the server.

        Args:
            key (str): The key to delete.

        Returns:
            None
        """
        self.socket.send(f"DELETE {key}\n".encode())
        return

    def genMobilityHint(self, host: str, port: int) -> None:
        """
        Sends a mobility hint message to the server with the specified host and port.

        Args:
            host (str): The host to include in the mobility hint message.
            port (int): The port to include in the mobility hint message.

        Returns:
            None
        """
        msg: str = f"MB_HINT {host} {port}\n"
        self.socket.send(msg.encode())

    def handleDisconnect(self, host: str, port: int):
        self.socket.send("DISCONNECT\n".encode())
        sleep(0.100) # to simulate a handover event on the client
        self.host = host
        self.port = port

        self.connect()
        id_mess = self.socket.recv(4096).decode()
        print(id_mess)
        # logger.debug(f"Recieved ID request from server. ID is {self.id}")

        if self.id:
            msg = self.id
            self.socket.send(msg.encode())
        else:
            msg = "-1"
            self.socket.send(msg.encode())
            id = self.socket.recv(4096).decode()
            self.id = id.split(":")[-1]
            # logger.debug(f"ID recieved. Client ID is now {self.id}")

    def run(self):
        while self.running:
            msg: List[str] = input("LLDS: ").split(" ")
            msg.append("\n")
            if msg[0] == "GET":
                key: str = msg[1]
                res: str = self.get(key)
                if res:
                    print(res)
                else:
                    print("MISS")

            elif msg[0] == "PUT":
                key: str = msg[1]
                value: bytes = " ".join(msg[2:]).encode()
                self.put(key, value)

            elif msg[0] == "DELETE":
                key: str = msg[1]
                self.delete(key)

            elif msg[0] == "MB_HINT":
                host: str = msg[1]
                port: int = int(msg[2])
                self.genMobilityHint(host, port)

            elif msg[0] == "DISCONNECT":
                host: str = msg[1]
                port: int = int(msg[2])
                self.handleDisconnect(host, port)

            elif msg[0] == "exit" or msg[0] == "quit":
                self.socket.send("DISCONNECT\n".encode())
                self.running = False
                self.close()
                break


def main():
    if len(argv) == 3:
        client = Client(argv[1], argv[2])
    else:
        client = Client()
    # print(f"Starting at time {time()}")
    # for i in range(100):
    #     client.put(f"key{i}", f"value{i}".encode())
    # print(f"Ending at time {time()}")
    client.run()


if __name__ == "__main__":
    main()

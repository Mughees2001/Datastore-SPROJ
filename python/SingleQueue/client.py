from socket import socket, AF_INET, SOCK_STREAM
from .lib.log import logger  # Changed to relative import
from threading import Thread



class Client:
    def __init__(self, host: str = "localhost", port: str = "8007"):
        self.host: str = host
        self.port: int = int(port)
        self.socket: socket = socket(AF_INET, SOCK_STREAM)
        self.running: bool = True
        self.id: str = None
        self.connect()

    def connect(self):
        self.socket.connect((self.host, self.port))
        logger.debug(f"Connected to {self.host}:{self.port}")

    def close(self):
        self.socket.close()
        logger.debug(f"Closed connection to {self.host}:{self.port}")

    def get(self, key: str) -> bytes:
        """
        Summary:
            Gets the value of a key from the server
        Args:
            key (string): contains the key to be searched

        Returns:
            string: returns the value of the key if found, else returns "MISS". If no key is provided, returns "Please enter a key"
        """
        if key:
            message = "GET " + key
            self.socket.send(message.encode())
            res = self.socket.recv(4096).decode()
            return res

    def put(self, key: str, value: bytes) -> None:
        """
        Sends a PUT request to the server with the specified key and value.

        Args:
            key (str): The key to store the value under.
            value (bytes): The value to store.

        Returns:
            None
        """
        self.socket.send(f"PUT {key} {value.decode()}".encode())

    def delete(self, key: str) -> None:
        """
        Deletes a key from the server.

        Args:
            key (str): The key to delete.

        Returns:
            None
        """
        self.socket.send(f"DELETE {key}".encode())
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
        msg: str = f"MB_HINT {host} {port}"
        self.socket.send(msg.encode())

    def run(self):
        id_mess = self.socket.recv(4096).decode()
        print(id_mess)
        logger.debug(f"Recieved ID request from server. ID is {self.id}")

        if self.id:
            msg = self.id
            self.socket.send(msg.encode())
        else:
            msg = "-1"
            self.socket.send(msg.encode())
            id = self.socket.recv(4096).decode()
            self.id = id.split(":")[-1]
            logger.debug(f"ID recieved. Client ID is now {self.id}")

        while self.running:
            msg: str = input("LLDS: ").split(" ")
            if msg[0] == "GET":
                key: str = msg[1]
                res: bytes = self.get(key)
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

            elif msg == "exit" or msg == "quit":
                self.running = False
                self.close()
                break


def main():
    client = Client()
    client.run()


if __name__ == "__main__":
    main()

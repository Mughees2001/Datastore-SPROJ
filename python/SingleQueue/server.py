from lib.log import logger
from typing import List, Dict, Tuple, Optional
from lib.RapidQueue import RapidQueue
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from uuid import uuid4


class Server:
    def __init__(self, host: str = "localhost", port: str = "8000"):
        """_summary_

        Initializes a server that communicates to multiple clients

        Args:
            host (str, optional): _description_. Defaults to "localhost".
            port (str, optional): _description_. Defaults to "8000".
        """
        self.store: Dict[Tuple, RapidQueue] = dict()
        self.clients_id: Dict[socket, int] = dict()
        self.host = host
        self.port = int(port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.running = True

        try:
            self.socket.bind((self.host, self.port))
            logger.debug("Server connected successfully")
        except OSError:
            logger.error(f"Port already in use")
            exit(1)

        self.client_threads: Dict[
            socket, Thread
        ] = dict()  # a dictionary to keep track of client threads
        self.migrating_bses: Dict[
            socket, socket
        ] = (
            dict()
        )  # a dictionary to keep track of the next base station for a thread if any

    def generate_client_ID(self, client: socket):
        """_summary_

        This function generates a unique client ID using UUID and sends it to the Client.
        The Client uses this ID when it wants to migrate to a new base station and sends it
        while connecting.

        Args:
            client (socket): _description_
        """
        self.clients_id[client] = uuid4()

    def put(self, client: socket, key: str, value: bytes):
        pass

    def get(self, client: socket, key: str) -> Optional[bytes]:
        pass

    def delete(self, client: socket, key: str) -> bool:
        pass

    def mobility_hint(self, client: socket, dest_host: str, dest_port: str):
        pass

    def recieve_update(self, client_id: int):
        pass

    def client_handler(self, client: socket, id=None):
        if id is None:
            self.generate_client_ID(client)
            id = self.clients_id[client]

            # inform the client of it's ID before starting any other communication
            client.send(
                f"Recv_ID:{id}".encode()
            )  # no need to ack since we are using TCP

        # add code here
        while self.running:
            cmd = client.recv(4096).decode().split(" ")

            if cmd[0] == "GET":
                pass
            if cmd[0] == "PUT":
                pass
            if cmd[0] == "DELETE":
                pass
            if cmd[0] == "MB_HINT":
                pass
            if cmd[0] == "SYNC_PUT":
                pass
            if cmd[0] == "DISCONNECT":
                pass
                
            

    def run(self):
        """
        This function listens for connections. It connects to a client and asks it for an ID
        If it has no ID, it calls the client handler that informs the client of it's ID
        """
        logger.log(f"Server is up and listening on {self.host}:{self.port}")
        self.socket.listen(25)
        try:
            while self.running == True:
                try:
                    client, address = self.socket.accept()
                except:
                    break

                logger.log(f"Connected to client at {address}")

                client.send("Have_ID")
                id = client.recv(2048).decode()

                if id == "":
                    id = None
                else:
                    id = int(id)

                t = Thread(
                    self.client_handler,
                    args=(
                        client,
                        id,
                    ),
                )
                t.daemon = False
                self.client_threads[client] = t
                t.start()

        except KeyboardInterrupt:
            self.exit()
            logger.debug("Keyboard Interrupt recieved")

    def exit(self):
        logger.debug(f"Shutting down server")
        self.socket.close()
        self.running = False
        exit(0)

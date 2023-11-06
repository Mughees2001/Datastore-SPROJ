from .lib.log import logger
from typing import List, Dict, Tuple, Optional
from .lib.RapidQueue import RapidQueue
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from uuid import uuid4



class Server:
    def __init__(self, host: str = "localhost", port: str = "8007"):
        """_summary_

        Initializes a server that communicates to multiple clients

        Args:
            host (str, optional): _description_. Defaults to "localhost".
            port (str, optional): _description_. Defaults to "8000".
        """
        self.store: Dict[str, RapidQueue] = dict()
        self.clients_id: Dict[socket, str] = dict()
        self.other_masters: Dict[str, socket] = dict()  # {client_id: socket of master}
        self.host: str = host
        self.port: int = int(port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.running: bool = True

        try:
            self.socket.bind((self.host, self.port))
            # logger.debug("Server connected successfully")
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
        self.clients_id[client] = str(uuid4())

    def put(self, client_id: str, key: str, value: bytes):
        try:
            self.store[client_id].put(key, value)
        except KeyError:
            self.store[client_id] = RapidQueue()
            self.store[client_id].put(key, value)

    def get(self, client_id: str, key: str) -> Optional[bytes]:
        try:
            return self.store[client_id].get(key)
        except KeyError:
            self.store[client_id] = RapidQueue()
            return self.store[client_id].get(key)

    def delete(self, client_id: str, key: str) -> bool:
        try:
            self.store[client_id].remove(key)
            return True
        except KeyError:
            return False

    def mobility_hint(self, client_id: str, dest_host: str, dest_port: int):
        self.other_masters[client_id] = socket(AF_INET, SOCK_STREAM)
        self.other_masters[client_id].connect((dest_host, dest_port))

        # now we want to initialize the migration using our queue
        dump: str = self.store[client_id].startMigration()
        logger.debug(f"Prepared dump {dump} for client {client_id}")

        # now we want to send the dump to the other master
        dump_msg: str = f"SYNC_PUT {client_id} {dump}"
        self.other_masters[client_id].send(dump_msg.encode())

    def recieve_update(self, client_id: int):
        pass

    def client_handler(self, client: socket, id: str = None):
        if id is None:
            self.generate_client_ID(client)
            id: str = self.clients_id[client]

            # inform the client of it's ID before starting any other communication
            client.send(
                f"Recv_ID:{id}".encode()
            )  # no need to ack since we are using TCP

        while self.running:
            cmd = client.recv(4096).decode().split(" ")
            logger.debug(f"Recieved command {cmd} from client {id}")

            if cmd[0] == "GET":
                key: str = cmd[1]
                res: bytes = self.get(id, key)
                logger.debug(
                    f"Getting key {cmd[1]} from client {id}. Key contains {res}"
                )
                if res:
                    client.send(res)
                else:
                    client.send(" ".encode())

            if cmd[0] == "PUT":
                key: str = cmd[1]
                value: bytes = " ".join(cmd[2:]).encode()
                logger.debug(f"Putting key {key} with value {value} in client {id}")
                self.put(id, key, value)

            if cmd[0] == "DELETE":
                key: str = cmd[1]
                self.delete(id, key)

            if cmd[0] == "MB_HINT":
                host: str = cmd[1]
                port: int = int(cmd[2])
                self.mobility_hint(id, host, port)

            if cmd[0] == "SYNC_PUT":
                client_id: str = cmd[1]
                key: str = cmd[2]
                value: bytes = " ".join(cmd[3:]).encode()

                found: bool = False
                for k, v in self.clients_id.items():
                    if v == client_id:
                        found = True
                        self.put(v, key, value)

                if not found:
                    logger.error(f"Client with ID {client_id} not found")

            if cmd[0] == "DISCONNECT" or cmd[0] == "":
                break

    def run(self):
        """
        This function listens for connections. It connects to a client and asks it for an ID
        If it has no ID, it calls the client handler that informs the client of it's ID
        """
        # logger.debug(f"Server is up and listening on {self.host}:{self.port}")  # type: ignore
        self.socket.listen(25)
        try:
            while self.running == True:
                try:
                    client, address = self.socket.accept()
                except:
                    break

                logger.debug(f"Connected to client at {address}")

                client.send("Have_ID".encode())
                id = client.recv(2048).decode()
                print(f"ID recieved is {id}")

                if id == "-1":
                    id = None
                else:
                    id = str(id)

                t = Thread(
                    target=self.client_handler,
                    args=(
                        client,
                        id,
                    ),
                )
                t.daemon = False
                self.client_threads[client] = t
                t.start()
                logger.debug(f"Started thread for client at {address}")

        except KeyboardInterrupt:
            self.exit()
            logger.debug("Keyboard Interrupt recieved")

    def exit(self):
        logger.debug(f"Shutting down server")
        self.socket.close()
        self.running = False
        #exit(0)


def main():
    server = Server()
    server.run()


if __name__ == "__main__":
    main()

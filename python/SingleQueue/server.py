from lib.log import logger
from typing import List, Dict, Tuple, Optional
from lib.RapidQueue import RapidQueue
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from threading import Thread
from uuid import uuid4
from time import time, sleep
from sys import argv, exit


class Server:
    def __init__(self, host: str = "localhost", port: str = "8009"):
        """

        Initializes a server that communicates to multiple clients

        Args:
            host (str, optional): Defaults to "localhost".
            port (str, optional): Defaults to "8000".
        """
        self.store: Dict[str, RapidQueue] = dict()
        self.clients_id: Dict[socket, str] = dict()
        self.other_masters: Dict[str, socket] = dict()  # {client_id: socket of master}
        self.host: str = host
        self.port: int = int(port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        self.running: bool = True
        self.client_running: Dict[str, bool] = dict()

        try:
            self.socket.bind((self.host, self.port))
            # logger.debug("Server connected successfully")
        except OSError:
            logger.error(f"Port already in use")
            exit()

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
        logger.critical(f"Putting {key} {value} in client {client_id}")
        try:
            self.store[client_id].put(key, value)
        except KeyError:
            # logger.debug(f"Created a new store for client {client_id}")
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
        self.other_masters[client_id].setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        self.other_masters[client_id].connect((dest_host, dest_port))

        sock: socket = self.other_masters[client_id]

        id_message: str = sock.recv(2048).decode()
        logger.debug(f"Recieved ID message from new master")
        id: str = "server"
        sock.send(id.encode())

        # now we want to initialize the migration using our queue
        dump: str = self.store[client_id].startMigration()
        logger.debug(f"Prepared dump {dump} for client {client_id}")

        # now we want to send the dump to the other master
        dump_msg: str = f"SYNC_PUT {client_id} {dump}\n"
        sock.send(dump_msg.encode())

        t = Thread(target=self.syncHandler, args=(client_id,))
        t.daemon = False
        t.start()

    def handle_command(self, client: socket, id: str, cmd: List[str]):
        # logger.debug(f"Recieved command {cmd} from client {id} at time {time()}")
        if cmd[0] == "GET":
            key: str = cmd[1]
            res: Optional[bytes] = self.get(id, key)
            logger.debug(f"Getting key {cmd[1]} from client {id}. Key contains {res}")
            if res is not None:
                if len(res) == 0:
                    client.send(" ".encode())
                client.send(res)
            else:
                client.send(" ".encode())

        if cmd[0] == "PUT":
            key: str = cmd[1]
            value: bytes = " ".join(cmd[2:]).encode()
            if value[-1] == " ":
                value = value[:-1]  # remove the last space
            # logger.debug(f"Putting key {key} with value {value} in client {id}")
            self.put(id, key, value)

        if cmd[0] == "DELETE":
            key: str = cmd[1]
            self.delete(id, key)

        if cmd[0] == "MB_HINT":
            host: str = cmd[1]
            port: int = int(cmd[2])
            self.mobility_hint(id, host, port)

        if cmd[0] == "SYNC_PUT":
            # logger.debug(f"Recieved SYNC PUT with {cmd}")
            client_id: str = cmd[1]
            # kv_pairs: List[str] = " ".join(cmd[2:]).split(";")
            kv_pairs: List[str] = " ".join(cmd[2:]).split(";")
            logger.debug(f"Recieved {kv_pairs} from client {client_id}")
            for pair in kv_pairs:
                try:
                    key_p: str
                    value_p: str
                    logger.debug(f"Pair {pair}")
                    # remove space from the end of the string
                    if pair[-1] == " ":
                        pair = pair[:-1]
                    tokenized = pair.split(" ")
                    logger.critical(f"Tokenized {tokenized}")
                    if len(tokenized) != 1:
                        key_p = tokenized[0]
                        value_p = " ".join(tokenized[1:])

                    logger.debug(
                        f"Put {key_p} {value_p.encode()} in client {client_id}"  # type: ignore
                    )
                    self.put(client_id, key_p, value_p.encode())  # type: ignore

                except:
                    # logger.debug(f"Error occured while parsing {pair}")
                    pass
            logger.debug(f"State after processing {self.store[client_id]}")

        if cmd[0] == "DISCONNECT":
            self.client_running[id] = False  # to stop all other threads

            dump = self.store[id].getFirstN(self.store[id].length)
            logger.debug(f"Dumping {dump} for client {id}")
            dump_msg: str = f"SYNC_PUT {id} {dump}\n"
            try:
                client_migration_server: socket = self.other_masters[id]
                client_migration_server.send(dump_msg.encode())
            except KeyError:
                pass
            # client.send(dump_msg.encode())

            return

    def client_handler(self, client: socket, id: Optional[str] = None):
        if id is None:
            self.generate_client_ID(client)
            id = self.clients_id[client]

            # inform the client of it's ID before starting any other communication
            client.send(
                f"Recv_ID:{id}".encode()
            )  # no need to ack since we are using TCP

        self.client_running[id] = True

        delimiter = b"\n"
        data = b""
        while self.client_running[id]:
            chunk = client.recv(4096)
            if not chunk:
                break
            data += chunk
            commands = data.split(delimiter)
            data = commands.pop()  # Keep the incomplete command for the next iteration

            for command in commands:
                # Process the command (e.g., handle "PUT" or "GET" commands)
                if command == b"exit":
                    self.client_running[id] = False
                    break
                self.handle_command(client, id, command.decode().split(" "))

            # cmd: str = "".join(parts)

    def syncHandler(self, id: str):
        while self.client_running[id]:
            if self.store[id].head:
                logger.debug(f"Syncing client {id}")
                key: str
                val: str
                dump = self.store[id].getFirstN(1).split(" ")
                key = dump[0]
                val = " ".join(dump[1:])
                sync_msg: str = f"SYNC_PUT {id} {key} {val}\n"
                self.other_masters[id].send(sync_msg.encode())
            sleep(2)  # sleep for 1 millisecond

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
                # logger.debug(f"Started thread for client at {address}")

        except KeyboardInterrupt:
            self.exit()
            logger.debug("Keyboard Interrupt recieved")

    def exit(self):
        logger.debug(f"Shutting down server")
        self.socket.close()
        self.running = False
        # exit(0)


def main():
    if len(argv) == 3:
        host = argv[1]
        port = argv[2]
        server = Server(host, port)
    else:
        server = Server()
    server.run()


if __name__ == "__main__":
    main()

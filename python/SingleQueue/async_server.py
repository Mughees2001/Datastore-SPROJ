from typing import List, Optional, Dict, Tuple
from asyncio import AbstractServer, StreamReader, StreamWriter
import asyncio
from lib.log import logger
from lib.RapidQueue import RapidQueue
from uuid import uuid4
from sys import argv


class Server:
    def __init__(self, host: str = "localhost", port: str = "8009"):
        """
        Initializes an instance of the AsyncServer class.

        Args:
            host (str): The host address to bind the server to. Defaults to "localhost".
            port (str): The port number to bind the server to. Defaults to "8009".
        """
        self.store: Dict[str, RapidQueue] = dict()
        self.clients_id: Dict[asyncio.transports.Transport, str] = dict()
        self.other_masters: Dict[str, Tuple[StreamReader, StreamWriter]] = dict()
        self.host: str = host
        self.port: int = int(port)
        self.server: Optional[AbstractServer] = None
        self.running: bool = True
        # self.client_running: Dict[str, bool] = dict()


    async def start(self):
        """
        Starts the server and listens for incoming connections.

        This method starts the server by creating a new asyncio server using the
        provided host and port. It then logs the server's start information and
        waits for incoming connections indefinitely.

        """
        try:
            self.server = await asyncio.start_server(
                self.handle_connection, self.host, self.port
            )
            logger.info(f"Server started at {self.host}:{self.port}")
            await self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server stopped")

    def generate_client_id(self, transport: asyncio.transports.Transport):
        """
        Generates a unique client ID for the given transport and stores it in the clients_id dictionary.

        Parameters:
        transport (asyncio.transports.Transport): The transport object associated with the client.

        Returns:
        None
        """
        client_id = str(uuid4())
        self.clients_id[transport] = client_id

    def put(self, client_id: str, key: str, value: bytes):
        """
        Adds a key-value pair to the store for the specified client.

        Args:
            client_id (str): The ID of the client.
            key (str): The key of the data to be stored.
            value (bytes): The value of the data to be stored.
        """
        try:
            self.store[client_id].put(key, value)
        except KeyError:
            self.store[client_id] = RapidQueue()
            self.store[client_id].put(key, value)

    def get(self, client_id: str, key: str) -> Optional[bytes]:
        """
        Retrieves the value associated with the given key for the specified client.

        Args:
            client_id (str): The ID of the client.
            key (str): The key to retrieve the value for.

        Returns:
            Optional[bytes]: The value associated with the key, or None if the key does not exist.
        """
        try:
            return self.store[client_id].get(key)
        except KeyError:
            self.store[client_id] = RapidQueue()
            return self.store[client_id].get(key)

    def delete(self, client_id: str, key: str) -> bool:
        """
        Deletes a key from the store for a specific client.

        Args:
            client_id (str): The ID of the client.
            key (str): The key to be deleted.

        Returns:
            bool: True if the key was successfully deleted, False otherwise.
        """
        try:
            self.store[client_id].remove(key)
            return True
        except KeyError:
            return False

    async def mobility_hint(self, client_id: str, dest_host: str, dest_port: int):
        try:
            reader, writer = await asyncio.open_connection(dest_host, dest_port)
            self.other_masters[client_id] = (reader, writer)
            # Perform operations with the connected server

            id_message = await reader.readline()
            id_message = id_message.decode().strip()
            logger.debug(f"Received ID message from new master: {id_message}")

            # Send server ID
            server_id = "server"
            writer.write(server_id.encode())
            await writer.drain()

            # # Initialize the migration using the queue
            # if client_id in self.store:
            #     dump = self.store[client_id].startMigration()
            #     logger.debug(f"Prepared dump {dump} for client {client_id}")

            #     # Send the dump to the other master
            #     dump_msg = f"SYNC_PUT {client_id} {dump}\n"
            #     writer.write(dump_msg.encode())
            #     await writer.drain()

            #     # Handle synchronization (assuming you have an async version of syncHandler)
            #     await self.async_syncHandler(client_id, reader, writer)

            writer.close()
            await writer.wait_closed()

        except ConnectionRefusedError:
            logger.error(f"Failed to connect to {dest_host}:{dest_port}")

    async def async_syncHandler(self, client_id, reader, writer):
        # Implement the asynchronous version of syncHandler
        pass
    
    # async def mobility_hint(self, client_id: str, dest_host: str, dest_port: int):
    #     try:
    #         reader, writer = await asyncio.open_connection(dest_host, dest_port)
    #         self.other_masters[client_id] = (reader, writer)
    #         # Perform operations with the connected server
    #         # ...

    #         id_message: str = await reader.readline().decode()

    #         writer.close()
    #         await writer.wait_closed()
    #     except ConnectionRefusedError:
    #         logger.error(f"Failed to connect to {dest_host}:{dest_port}")

    def handle_command(self, client: asyncio.transports.Transport, cmd: List[str]):
        cmd[0] = cmd[0].upper()
        print(cmd)
        if cmd[0] == "PUT":
            if len(cmd) == 3:
                self.put(self.clients_id[client], cmd[1], cmd[2][:-1].encode())
                client.write("OK\n".encode())
            else:
                client.write("ERR\n".encode())

        elif cmd[0] == "GET":
            if len(cmd) == 2:
                value = self.get(self.clients_id[client], cmd[1][:-1])
                if value:
                    client.write(f"{value.decode()}\n".encode())
                else:
                    client.write("ERR\n".encode())
            else:
                client.write("ERR\n".encode())

        elif cmd[0] == "DELETE":
            if len(cmd) == 2:
                if self.delete(self.clients_id[client], cmd[1]):
                    client.write("OK\n".encode())
                else:
                    client.write("ERR\n".encode())
            else:
                client.write("ERR\n".encode())

        elif cmd[0] == "MB_HINT":
            if len(cmd) == 3:
                asyncio.create_task(
                    self.mobility_hint(self.clients_id[client], cmd[1], int(cmd[2]))
                )
                client.write("OK\n".encode())
            else:
                client.write("ERR\n".encode())

        elif cmd[0] == "DISCONNECT":
            client_id = self.clients_id.get(client)
            if client_id is None:
                logger.error("Client ID not found for the given transport.")
                return

            #self.client_running[client_id] = False  # Mark the client as not running
            # # Prepare and send the dump
            # dump = self.store[client_id].getFirstN(self.store[client_id].length)
            # logger.debug(f"Dumping {dump} for client {client_id}")
            # dump_msg = f"SYNC_PUT {client_id} {dump}\n"
            # try:
            #     client_migration_writer = self.other_masters[client_id][1]
            #     asyncio.create_task(self.send_async_message(client_migration_writer, dump_msg))
            # except KeyError:
            #     logger.error(f"No migration server found for client {client_id}")

            # Close the client connection
            client.close()

            # Clean up client references
            del self.clients_id[client]

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        """
        Handles a client connection.

        Args:
            reader (StreamReader): The reader object for reading data from the client.
            writer (StreamWriter): The writer object for writing data to the client.
        """
        print(f"New connection from {writer.get_extra_info('peername')}")
        client_id = self.generate_client_id(writer.transport)
        self.store[client_id] = RapidQueue()

        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                # Process the received data
                # ...
                if data == b"exit":
                    break

                # # Example: Echo back the received data
                # writer.write(data)
                # await writer.drain()

                self.handle_command(writer.transport, data.decode().split(" "))

        except asyncio.CancelledError:
            pass

        finally:
            # Clean up resources
            writer.close()
            await writer.wait_closed()
            del self.store[client_id]


def main():
    if len(argv) == 3:
        server = Server(argv[1], argv[2])
    else:
        server = Server()

    try:
        asyncio.run(server.start())
    except:
        print("Server stopped")


if __name__ == "__main__":
    main()

from json import dumps, loads
from time import time
import socket
from sys import argv
from threading import Thread
from typing import Dict, Tuple
from hashqueue import MultipleHashQueue
import pprint


class KV:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        # self.time = time() # removing time for now, since this would be part of a protocol later


class Master:
    def __init__(self, host, port):
        self.store = MultipleHashQueue(2)
        self.host = host
        self.port = int(port)
        self.threads = list()
        self.otherMasterSockets: Dict[Tuple(str, str), socket.socket] = dict()
        self.masterSocketByClient: Dict[socket.socket, socket.socket] = dict()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def put(self, kv: KV):
        if kv:
            self.store.put(kv.key, kv.value)

    def get(self, key):
        return self.store.get(key)

    def delete(self, key):
        return self.store.delete(key)

    def inOrderTraversal(self):
        return self.store.inOrderTraversal()

    def mbHint(self, client: socket.socket, host, port):
        """
        Summary:
            Connects to a master node and sends all current values to it

        Args:
            host (string): Contains the new master's host address
            port (string): Contains the new master's host port
        """
        try:
            self.otherMasterSockets[(host, port)] = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            self.otherMasterSockets[(host, port)].connect((host, int(port)))

            self.masterSocketByClient[client] = self.otherMasterSockets[
                (host, port)
            ]  # saving the socket by reference so we can use it for other requests

            data_to_send = dumps(self.store)
            message = "MIGRATING_DATA " + data_to_send
            self.otherMasterSockets[(host, port)].send(message.encode())

        except Exception as e:
            print(e)
            return

    def disconnect(self, client: socket.socket, message=None):
        """
        Summary:
            Disconnects a client from the server
        Args:
            client (socket.socket): contains the client socket to be disconnected
        """
        if message:
            client.send(message.encode())
        client.close()
        print(f"Disconnected from client.")

        # disconnect from master server for old client
        try:
            conn = self.masterSocketByClient[client]
            conn.send("DISCONNECT".encode())
            del self.masterSocketByClient[client]
            print("Disconnected from master server for old client")
        except KeyError:
            pass

    def handleMigrationData(self, data: str):
        """
        Summary:
            Handles incoming data from another master server, after the MB_HINT command is sent to the first server

        Args:
            data (str): Data sent by the old master server
        """
        # print(data)
        data_in_dict = loads(data)
        self.store.update(
            data_in_dict
        )  # adds the data from the old master server to the current master server

    def clientHandler(self, client: socket.socket):
        while True:
            cmd = client.recv(1024).decode()
            cmd = cmd.split(" ")
            if cmd[0] == "PUT":
                key, value = cmd[1].split(":")
                self.put(KV(key, value))
                # print(f"PUT {key}:{value}")
                # we will also send a put request to the other master servers, if a client has any
                try:
                    conn = self.masterSocketByClient[client]
                    message = "PUT " + key + ":" + value
                    conn.send(message.encode())
                except KeyError:
                    pass
            elif cmd[0] == "GET":
                val = self.get(cmd[1])
                # print(f"GET {cmd[1]}:{val}")
                client.send(val.encode())
            elif cmd[0] == "DELETE":
                val = self.delete(cmd[1])
                if val:
                    client.send("DELETED".encode())
                else:
                    client.send("MISS".encode())
            elif cmd[0] == "MB_HINT":
                host, port = cmd[1].split(":")
                self.mbHint(client, host, port)
            elif cmd[0] == "MIGRATING_DATA":
                data = " ".join(cmd[1:])
                self.handleMigrationData(data)
            elif cmd[0] == "DISCONNECT":
                self.disconnect(client)
                break
            else:
                self.disconnect(client, "Invalid command")
                break
            state = self.store.currentState()
            # pprint.pprint(state)

    def run(self):
        print(f"Server listening on {self.host}:{self.port}")
        self.socket.listen(25)  # arbitrary number
        try:
            while True:
                try:
                    client, address = self.socket.accept()
                except:
                    break
                print(f"Connected to {address}")
                t = Thread(target=self.clientHandler, args=(client,))
                self.threads.append(t)
                t.start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            for t in self.threads:
                t.join()
            self.socket.close()
            print("Server shut down successfully.")

    def currentState(self):
        return self.store.currentState()

    def exit(self):
        self.socket.close()
        print("Server shut down successfully.")
        exit()


def main():
    if len(argv) < 3:
        exit(Exception("Usage: python[3] master.py <host> <port>"))

    host, port = argv[1], argv[2]
    master = Master(host, port)
    master.run()


if __name__ == "__main__":
    main()

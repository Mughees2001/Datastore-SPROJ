from time import time
import socket
from sys import argv
from threading import Thread

if len(argv) < 3:
    exit(Exception("Usage: python[3] master.py <host> <port>"))

host, port = argv[1], argv[2]


class KV:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        # self.time = time() # removing time for now, since this would be part of a protocol later


class Master:
    def __init__(self, host, port):
        self.store = dict()  # key: key, value:
        self.host = host
        self.port = int(port)
        self.threads = list()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def put(self, kv: KV):
        if kv:
            self.store[kv.key] = kv.value

    def get(self, key):
        return self.store.get(key, "MISS")

    def delete(self, key):
        if key in self.store:
            del self.store[key]
            return True
        else:
            return False

    def clientHandler(self, client: socket.socket):
        while True:
            cmd = client.recv(1024).decode()
            cmd = cmd.split(" ")
            if cmd[0] == "PUT":
                key, value = cmd[1].split(":")
                self.put(KV(key, value))
                print(f"PUT {key}:{value}")
                self.currentState()
            elif cmd[0] == "GET":
                val = self.get(cmd[1])
                client.send(val.encode())
            elif cmd[0] == "DELETE":
                val = self.delete(cmd[1])
                if val:
                    client.send("DELETED".encode())
                else:
                    client.send("MISS".encode())
            else:
                client.send("Invalid command. Disconnecting.".encode())
                client.close()
                break

    def run(self):
        print(f"Server listening on {self.host}:{self.port}")
        self.socket.listen(25)  # arbitrary number
        try:
            while True:
                client, address = self.socket.accept()
                print(f"Connected to {address}")
                t = Thread(target=self.clientHandler, args=(client,))
                self.threads.append(t)
                t.start()
        except KeyboardInterrupt:
            print("Shutting down server...")
            for t in self.threads:
                t.join()
            self.socket.close()
            print("Server shut down successfully.")

    def currentState(self):
        print(self.store)


def main():
    master = Master(host, port)
    master.run()


if __name__ == "__main__":
    main()

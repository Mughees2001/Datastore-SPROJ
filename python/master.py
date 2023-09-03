import os
from time import time
import socket


class KV:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.time = time()


class Master:
    def __init__(self, host, port):
        self.storePath = os.getcwd() + "/store/temp.txt"
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def store(self, KV):
        if KV:
            with open(self.storePath, "a") as f:
                f.write(KV.key + ":" + KV.value + "\n")
                f.close()
                return True


def main():
    master = Master("localhost", 8081)

    while True:
        master.socket.listen(5)
        conn, addr = master.socket.accept()
        data = conn.recv(1024)
        if data:
            data = data.decode()
            kv = KV(data.split(":")[0], data.split(":")[1])
            master.store(kv)


if __name__ == "__main__":
    main()

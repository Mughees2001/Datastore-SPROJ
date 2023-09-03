import socket
from master import KV
from sys import argv

if len(argv) < 3:
    exit(Exception("Usage: python[3] client.py <host> <port>"))

host, port = argv[1], int(argv[2])


class Client:
    def __init__(self, host, port):
        """
        Summary:
            Intializes a client by connecting to the server at the given host and port
        Args:
            host (string): contains the host address
            port (int): contains the port number of the server
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
        except Exception as e:
            print(e)
            exit(1)

        print(f"Connected to server at {self.host}:{self.port}")

    def put(self, KV):
        if KV:
            val = KV.key + ":" + KV.value
            self.socket.send(val.encode())
            return True
        else:
            return False

    async def get(self, key):
        if key:
            self.socket.send(key.encode())
            return await self.socket.recv(1024)

    def delete(self, key):
        pass

    def main(self):
        """
        Summary:
            Main function for the client. It takes user input for commands and communicates with the server, carrying out appropriate actions

        Legal Inputs:
            1. PUT : <key> <value>
            2. GET : <key>
            3. DELETE : <key>
            4. EXIT
        """

        try:
            while True:
                prompt = input("datastore: ")
                prompt = prompt.split(" ")
                if prompt[0] == "PUT":
                    key = prompt[1]
                    value = prompt[2]
                    kv = KV(key, value)
                    key = prompt[1]
                    self.put(kv)
                elif prompt[0] == "GET":
                    print(self.get(key))

                elif prompt[0] == "DELETE":
                    key = prompt[1]
                    self.delete(key)
                elif prompt[0] == "EXIT":
                    break
                else:
                    print("Invalid command")
        except KeyboardInterrupt:
            print("\nExiting...")
            self.socket.close()  # close the socket


def main():
    client = Client(host, port)

    # client.main()


if __name__ == "__main__":
    # main()
    print(Client(host, port).__init__.__doc__)

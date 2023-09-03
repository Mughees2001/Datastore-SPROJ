import socket
from master import KV
from sys import argv

if len(argv) < 3:
    exit(Exception("Usage: python[3] client.py <host> <port>"))

host, port = argv[1], argv[2]


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
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
        except Exception as e:
            print(e)
            exit(1)

        print(f"Connected to server at {self.host}:{self.port}")

    def put(self, KV):
        """
        Summary:
            Sends a key-value pair to the server
        Args:
            KV (tuple<key, value>): contains the key-value pair to be sent to the server

        Returns:
            Bool: returns True if the key-value pair was sent successfully, else returns False
        """
        if KV:
            val = "PUT " + KV.key + ":" + KV.value
            self.socket.send(val.encode())
            return True
        else:
            return False

    def get(self, key):
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
            res = self.socket.recv(1024).decode()
            return res
        else:
            return "Please enter a key"

    def delete(self, key):
        """
        Summary:
            Deletes a key-value pair from the server
        Args:
            key (string): contains the key to be deleted
        """
        if key:
            message = "DELETE " + key
            self.socket.send(message.encode())
            response = self.socket.recv(1024).decode()
            if response == "DELETED":
                return f"Key {key} deleted successfully"
            else:
                return f"Key {key} not found at server"
        else:
            return "Please enter a key"

    def run(self):
        """
        Summary:
            Main function for the client. It takes user input for commands and communicates with the server, carrying out appropriate actions

        Legal Inputs:
            - PUT : <key> <value>
            - GET : <key>
            - DELETE : <key>
            - EXIT
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
                    key = prompt[1]
                    print(self.get(key))
                elif prompt[0] == "DELETE":
                    key = prompt[1]
                    print(self.delete(key))
                elif prompt[0] == "EXIT":
                    break
                else:
                    print("Invalid command")
        except KeyboardInterrupt:
            print("\nExiting...")
            self.socket.close()  # close the socket connection on keyboard interrupt


def main():
    client = Client(host, port)

    client.run()


if __name__ == "__main__":
    main()

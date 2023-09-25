import socket
from master import KV
from sys import argv


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

    def generateMobilityHint(self, new_master_host, new_master_port):
        """
        Summary:
            This function is called when a mobility hint is generated by the client. It sends the mobility hint to the server, along with the new master's host and port. This function is for simulation purposes.

        Args:
            new_master_host (string): Contains the new master's host address
            new_master_port (string): Contains the new master's port number
        """

        # send a message to the master server, indicating that a mobility hint was generated, indicating the new master's host and port
        self.socket.send(f"MB_HINT {new_master_host}:{new_master_port}".encode())

    def disconnect(self, new_master_host, new_master_port):
        """
        Summary:
            This function is called when the client is disconnecting from the old master server. It sends a disconnect message to the server, and connects to the new master server. This is meant to simulate a client under mobility, moving from one server to another.
        Args:
            new_master_host (string): Contains the new master's host address
            new_master_port (string): Contains the new master's port number
        """

        # send the disconnect message
        self.socket.send("DISCONNECT".encode())

        # close the socket connection
        self.socket.close()

        # connect to the new master server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((new_master_host, int(new_master_port)))
        except Exception as e:
            print(
                f"Failed to connect to new server at {new_master_host}:{new_master_port} with exception: \n\n {e}"
            )
            exit(1)

    def run(self):
        """
        Summary:
            Main function for the client. It takes user input for commands and communicates with the server, carrying out appropriate actions

        Legal Inputs:
            - PUT : <key> <value>
            - GET : <key>
            - DELETE : <key>
            - MB_HINT : <new_master_host> <new_master_port>
            - DISCONNECT : <new_master_host> <new_master_port> (this function disconnects from the old master server, and connects to the new one.)
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
                elif prompt[0] == "MB_HINT":  # FOR MOBILITY HINTS
                    host, port = prompt[1], prompt[2]
                    self.generateMobilityHint(host, port)
                elif prompt[0] == "DISCONNECT":  # FOR DISCONNECTING FROM OLD MASTER
                    host, port = prompt[1], prompt[2]
                    self.disconnect(host, port)
                elif prompt[0] == "EXIT":
                    break
                else:
                    print("Invalid command")
        except KeyboardInterrupt:
            print("\nExiting...")
            self.socket.close()  # close the socket connection on keyboard interrupt


def main():
    if len(argv) < 3:
        exit(Exception("Usage: python[3] client.py <host> <port>"))

    host, port = argv[1], argv[2]

    client = Client(host, port)
    summary = """
    Legal Inputs:
        - PUT : <key> <value>
        - GET : <key>
        - DELETE : <key>
        - MB_HINT : <new_master_host> <new_master_port>
        - DISCONNECT : <new_master_host> <new_master_port> (this function disconnects from the old master server, and connects to the new one.)
        - EXIT
        """
    print(summary)
    client.run()


if __name__ == "__main__":
    main()

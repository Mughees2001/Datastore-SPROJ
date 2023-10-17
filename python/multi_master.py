from hashqueue import MultipleHashQueue
from socket import socket, AF_INET, SOCK_STREAM
from typing import Dict
from UpdatedCode.lib.log import logger


class KV:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Datastore:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.nestedDatastore: Dict[socket, MultipleHashQueue] = dict()
        self.new_masters: Dict[socket, socket] = dict()
        self.threads = list() # a list of all active threads
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.bind((self.host, self.port))
        except Exception as e:
            logger.error(e)

    def put(self, client : socket, kv : KV):
        if kv:
            self.nestedDatastore[client].put(kv.key, kv.value)
        
    def get(self, client : socket, key : str):
        return self.nestedDatastore[client].get(key)
    
    def delete(self, client : socket, key : str):
        return self.nestedDatastore[client].delete(key)
    
    def MobilityHint(self, client : socket, host, port):
        
        # connect to new master
        try:
            self.new_masters[client] = socket(AF_INET, SOCK_STREAM)
            self.new_masters[client].connect((host, int(port)))
            
            
            
        except Exception as e:
            pass
        
        
    def client_handler(self, client: socket):
        while True:
            cmd = client.recv(4096).decode("utf-8")
            cmd = cmd.split(" ")
            print(cmd)

    def run(self):
        pass


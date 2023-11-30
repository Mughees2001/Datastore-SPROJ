from uuid import uuid4
from server import Server
from lib.RapidQueue import RapidQueue


server = Server()

vals = [f"{str(i)}" for i in range(1000)]

random_id = str(uuid4())
server.store[random_id] = RapidQueue()

for val in vals:
    server.store[random_id].put(val, val.encode())

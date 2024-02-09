from typing import List, Optional
import asyncio
from sys import argv


class Client:
    def __init__(self, host: str = "localhost", port: str = "8009"):
        self.host: str = host
        self.port: int = int(port)
        self.running: bool = True
        self.id: Optional[str] = None
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print(f"Connected to {self.host}:{self.port}")

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
        print(f"Closed connection to {self.host}:{self.port}")

    async def get(self, key: str) -> str:
        if key:
            message: str = "GET " + key + "\n"
            self.writer.write(message.encode())
            res: str = await self.reader.readline()
            return res.decode()
        else:
            return ""

    async def put(self, key: str, value: bytes) -> None:
        if key:
            message: str = "PUT " + key + " " + value.decode() + "\n"
            self.writer.write(message.encode())
            await self.writer.drain()
            res: str = await self.reader.readline()
            print(res.decode())
        else:
            return None

    async def delete(self, key: str) -> None:
        if key:
            message: str = "DELETE " + key + "\n"
            self.writer.write(message.encode())
            await self.writer.drain()
        else:
            return None

    async def genMobilityHint(self, dest_host: str, dest_port: int) -> None:
        message: str = "MB_HINT " + dest_host + " " + str(dest_port) + "\n"
        self.writer.write(message.encode())
        await self.writer.drain()

    async def handleDisconnect(self, new_host: str, new_port: int):
        # Send the disconnect message
        disconnect_message = "DISCONNECT\n"
        self.writer.write(disconnect_message.encode())
        await self.writer.drain()

        # Sleep to simulate a handover event (replacing the blocking sleep with asyncio.sleep)
        await asyncio.sleep(0.100)

        # Update host and port
        self.host = new_host
        self.port = new_port

        # Reconnect with the new host and port
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        # Receive the ID message
        # id_message = await self.reader.read(4096)
        # id_message = id_message.decode()
        # print("Id_message",id_message)

        # # Send the client ID or -1 if not set
        # if self.id:
        #     msg = self.id
        # else:
        #     msg = "-1"

        # self.writer.write(msg.encode())
        # await self.writer.drain()
        # print("HERERER")

        # # If the client ID was not set, receive the new ID from the server
        # if not self.id:
        #     id_response = await self.reader.read(4096)
        #     id_response = id_response.decode()
        #     self.id = id_response.split(":")[-1]


    async def run(self):
        await self.connect()

        while self.running:
            msg: List[str] = input("Enter a command: ").split(" ")
            msg[0] = msg[0].upper()

            if msg[0] == "GET":
                key: str = msg[1]
                res: str = await self.get(key)
                if res:
                    print(res)
                else:
                    print("MISS")

            elif msg[0] == "PUT":
                key: str = msg[1]
                value: bytes = " ".join(msg[2:]).encode()
                await self.put(key, value)

            elif msg[0] == "DELETE":
                key: str = msg[1]
                await self.delete(key)

            elif msg[0] == "MB_HINT":
                host: str = msg[1]
                port: int = int(msg[2])
                await self.genMobilityHint(host, port)

            elif msg[0] == "DISCONNECT":
                host: str = msg[1]
                port: int = int(msg[2])
                await self.handleDisconnect(host, port)

            elif msg[0] == "EXIT" or msg[0] == "QUIT":
                await self.close()
                self.running = False
                break


def main():
    if len(argv) > 2:
        host = argv[1]
        port = argv[2]
        client = Client(host, port)
    else:
        client = Client()

    asyncio.run(client.run())


if __name__ == "__main__":
    main()

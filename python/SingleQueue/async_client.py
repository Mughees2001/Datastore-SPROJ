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
        message: str = "MOBILITY " + dest_host + " " + str(dest_port) + "\n"
        self.writer.write(message.encode())
        await self.writer.drain()

    async def handleDisconnect(self, host: str, port: int):
        message: str = "DISCONNECT " + host + " " + str(port) + "\n"
        self.writer.write(message.encode())
        await self.writer.drain()

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

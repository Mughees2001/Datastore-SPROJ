import asyncio


class Communication:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def read(self):
        data = await self.reader.readline()
        return data.decode().strip()

    async def write(self, message):
        self.writer.write(message.encode())
        await self.writer.drain()

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

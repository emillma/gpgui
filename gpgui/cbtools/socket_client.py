import aiohttp
import websockets
import asyncio
import websockets.client


async def hello():
    async with websockets.client.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()


asyncio.run(hello())


class Client:
    def __init__(self, url: str):
        self.url = url
        self.session = aiohttp.ClientSession()
        self.ws: websockets.client.ClientConnection | None = None

    async def __aenter__(self):
        self.ws = await websockets.client.connect(
            self.url, extra_headers={}
        ).__aenter__()

    async def __aexit__(self, exc_type, exc, tb):
        await self.ws.__aexit__(exc_type, exc, tb)

    async def send(self, topic: str, data: dict):
        async with self.session.post(
            self.url, json=data, headers={"topic": topic}
        ) as resp:
            return await resp.json()

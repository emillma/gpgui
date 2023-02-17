import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError
from websockets.legacy import server, client


async def hello():
    for i in range(100):
        try:
            async with websockets.connect("ws://10.53.58.89:8083") as websocket:
                while True:
                    await websocket.send("Hello world!")
                    print(await websocket.recv())

        except ConnectionRefusedError as e:
            print(e)
        except ConnectionClosedError as e:
            print(e)
        except Exception as e:
            raise e


asyncio.run(hello())

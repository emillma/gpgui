import asyncio
import json
import random
from quart import websocket, Quart
import time
import logging

quart_app = Quart(__name__)


@quart_app.websocket("/random_data")
async def random_data():
    while True:
        output = json.dumps([random.random() for _ in range(10)])
        await websocket.send(output)
        await asyncio.sleep(0.2)


@quart_app.websocket("/midi")
async def midi():
    await websocket.accept()
    while True:
        msg = await websocket.receive()
        print(msg)
        await websocket.send(msg)


@quart_app.websocket("/time")
async def markdown():
    while True:
        msg = f"time is {time.time()}"
        await websocket.send(msg)
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.INFO("Starting Quart server")
    quart_app.run(port=5000)

from gpgui.sockets import SocketClient
from asyncio import sleep, run, gather
import time
import json


async def send_forever(client: SocketClient):
    while True:
        await client.send({"i": time.time()})
        await sleep(1)


async def recv_forever(client: SocketClient):
    while True:
        data = await client.recv()
        print(data)


async def main():
    async with SocketClient(pub="topic1", sub="topic1") as client:
        await gather(send_forever(client), recv_forever(client))


if __name__ == "__main__":
    run(main())

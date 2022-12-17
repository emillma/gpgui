from gpgui.sockets import SocketClient
from asyncio import sleep, run
import json


async def main():
    client = SocketClient(
        "testclient", "ws://localhost:8050/hallows", publish_to="testtopic"
    )
    async with client:
        for i in range(10):
            await client.publish(
                json.dumps({a: {b: c} for a, b, c in zip(range(i), range(i), range(i))})
            )
            await sleep(0.1)


run(main())

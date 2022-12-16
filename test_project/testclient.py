from gpgui.sockets import SocketClient
from asyncio import sleep, run


async def main():
    client = SocketClient(
        "testclient", "ws://localhost:8050/hallows", publish_to="testtopic"
    )
    async with client:
        for i in range(10):
            await client.publish(f"testmessage {i}")
            await sleep(0.1)


run(main())

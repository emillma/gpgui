import asyncio
from websockets.legacy import server


async def serve_img():
    async def serve(websocket):
        print("hello" * 100)

    async with server.serve(serve, "127.0.0.1", 8050):
        for i in range(100000):
            print("running", i)
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(serve_img())

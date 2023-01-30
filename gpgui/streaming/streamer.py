import asyncio
import itertools

import ffmpeg
from . import VideoSource, RotatingBytearray


class Streamer:
    def __init__(
        self,
        source: VideoSource,
        chunk_size,
        buffer_size=2**30,
    ):
        self.source = source
        self.chunk_size = chunk_size
        self.buffer = RotatingBytearray(buffer_size)

        self.proc = None

        self.running = False

        self.input_event = asyncio.Event()
        self.output_condition = asyncio.Condition()

        self.ffmpeg_args = ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s=f"{self.source.width}x{self.source.height}",
            framerate=30,
        ).output(
            "pipe:",
            f="ismv",
            codec="libx265",
            preset="fast",
            frag_duration=200_000
            # movflags="frag_keyframe+empty_moov",
            # crf=5
            # **{"x265-params": "lossless=1"},
        )

    async def start(self):
        assert self.running is False
        self.proc = await asyncio.create_subprocess_exec(
            *self.ffmpeg_args.compile(),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            # stderr=asyncio.subprocess.PIPE,
        )
        loop = asyncio.get_running_loop()
        self.running = True
        loop.create_task(self.pipe_input())
        loop.create_task(self.store_output())

    async def stop(self):
        self.proc.kill()
        await self.proc.wait()
        self.running = False
        self.proc = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()

    async def pipe_input(self):
        it = aiter(self.source)

        while self.running:
            data = (await anext(it)).tobytes()
            self.proc.stdin.write(data)
            await self.proc.stdin.drain()
            self.input_event.set()

        self.proc.stdin.close()

    async def store_output(self):
        while self.running:
            await self.input_event.wait()
            self.input_event.clear()
            data = await self.proc.stdout.read(1000_000_000)
            await self.buffer.append_async(data)

    async def get_generator(self, start, stop):
        try:
            for start in range(start, stop, self.chunk_size):
                data = await self.buffer.read_async(start, self.chunk_size)
                yield data
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            pass

    # async def foo(self):
    #     assert self.proc is not None
    #     loop = asyncio.get_running_loop()
    #     loop.create_task(self.pipe_input())

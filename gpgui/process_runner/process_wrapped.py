import asyncio
from pathlib import Path
from asyncio.subprocess import Process
from gpgui.sockets import PubSubServer


class ProcessWrapped:
    proc: Process

    def __init__(self, file: Path):
        self.file = file
        self.topic_output = f"proc_{file.stem}_out"
        self.topic_status = f"proc_{file.stem}_status"
        self.lines = []
        self.event = asyncio.Event()
        self.tasks: list[asyncio.Task] = []
        self.started = False
        
    async def start(self):
        if self.started:
            return
        cmd = f"python3 {self.file}"
        self.proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        self.tasks = [
            asyncio.create_task(self._stream_reader_task(self.proc.stdout)),
            asyncio.create_task(self._stream_reader_task(self.proc.stderr)),
            asyncio.create_task(self._publish()),
            asyncio.create_task(self._wait()),
        ]
        
        self.started = True
        await PubSubServer.publish(self.topic_status, "running")

    async def stop(self):
        self.proc.terminate()
        try:
            await asyncio.wait_for(self.proc.wait(), timeout=5)
        except asyncio.TimeoutError:
            self.proc.kill()
        for task in self.tasks:
            task.cancel()
        await PubSubServer.publish(self.topic_status, "stopped")
            
    async def _wait(self):
        await self.proc.wait()
        await PubSubServer.publish(self.topic_status, "stopped")
        
    async def _stream_reader_task(self, stream: asyncio.StreamReader):
        async for line in stream:
            self.lines = (self.lines + line.decode().splitlines())[-30:]
            self.event.set()
            # self.event.clear()

    async def _publish(self, extra: float = 0.1):
        while True:
            await self.event.wait()
            self.event.clear()
            await PubSubServer.publish(self.topic_output, "\n".join(self.lines))
            await asyncio.sleep(extra)

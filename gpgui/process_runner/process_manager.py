from pathlib import Path
from .process_wrapped import ProcessWrapped


class ProcessManager:
    procs: dict[Path, ProcessWrapped] = dict()

    @classmethod
    async def start_process(cls, file: Path):
        if not file in cls.procs:
            cls.procs[file] = ProcessWrapped(file)
            await cls.procs[file].start()

    @classmethod
    async def stop_process(cls, file: Path):
        if proc := cls.procs.pop(file, None):
            await proc.stop()

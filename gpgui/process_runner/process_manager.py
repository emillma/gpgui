from pathlib import Path
from .process_wrapped import ProcessWrapped


class ProcessManager:
    procs: dict[Path, ProcessWrapped] = dict()

    @classmethod
    async def start_process(cls, file: Path):
        if not (proc := cls.procs.get(file, None)):
            cls.procs[file] = ProcessWrapped(file)
            await cls.procs[file].start()
        elif proc.done:
            cls.procs[file] = ProcessWrapped(file)
            await cls.procs[file].start()

    @classmethod
    async def stop_process(cls, file: Path):
        if proc := cls.procs.pop(file, None):
            await proc.stop()

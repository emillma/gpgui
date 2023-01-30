import itertools
import asyncio
import numpy as np
from . import VideoSource


class TestVideoSource(VideoSource):
    def __init__(self, height=512, width=512, fps=30):
        super().__init__(512, 512)
        self.fps = fps
        self.i = 0

    async def __anext__(self) -> np.ndarray:
        arr = np.zeros((512, 512, 3), dtype=np.uint8)
        arr[:, : self.i % 100, :] = 255
        self.i += 1
        await asyncio.sleep(1 / self.fps)
        return arr

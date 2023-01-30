from abc import abstractmethod

import numpy as np


class VideoSource:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    @abstractmethod
    async def __anext__(self) -> np.ndarray:
        ...

    def __aiter__(self):
        return self

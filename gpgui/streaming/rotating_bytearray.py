import asyncio


class RotatingBytearray:
    def __init__(self, size):
        self.size = size
        self.buffer = bytearray(size)

        self.start = 0

        self.filled = 0
        self.new_data_condition = asyncio.Condition()

    def append(self, data):
        stop_index = self.stop % self.size
        if self.filled < self.size:
            if self.filled + len(data) <= self.size:
                self.filled += len(data)
                self.buffer[stop_index : stop_index + len(data)] = data

            else:
                self.append(data[: self.size - self.filled])
                self.append(data[self.size - self.filled :])
        else:
            if stop_index + len(data) <= self.size:
                self.buffer[stop_index : stop_index + len(data)] = data

            else:
                remaining = self.size - stop_index
                self.buffer[stop_index:] = data[:remaining]
                self.buffer[: len(data) - remaining] = data[remaining:]
            self.start += len(data)

    def read(self, start, length):
        if start < 0:
            start = self.stop + start

        if start < self.start or start > self.stop:
            raise ValueError("Out of bounds")

        start_index = start % self.size

        if start_index + length <= self.size:
            data = self.buffer[start_index : start_index + length]

        else:
            remaining = self.size - start_index
            data = self.buffer[start_index:] + self.buffer[: length - remaining]

        return data

    async def append_async(self, data):
        async with self.new_data_condition:
            self.append(data)
            self.new_data_condition.notify_all()

    async def read_async(self, start, length):
        while self.stop < start + length:
            async with self.new_data_condition:
                await self.new_data_condition.wait()

        return self.read(start, length)

    def data(self):
        return self.read(self.start, self.filled)

    def __len__(self):
        return self.filled

    @property
    def stop(self):
        return self.start + self.filled

    def __repr__(self):
        return f"RotatingBytearray({self.start}, {self.stop})"

    def __str__(self):
        return str(self.data())

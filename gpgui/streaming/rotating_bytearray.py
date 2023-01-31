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

        if start < self.start or self.stop < start:
            raise ValueError("Start of bounds")

        if start + length > self.stop:
            raise ValueError("End of bounds")

        start_index = start % self.size

        if start_index + length <= self.size:
            data = self.buffer[start_index : start_index + length]

        else:
            remaining = self.size - start_index
            data = self.buffer[start_index:] + self.buffer[: length - remaining]

        return data

    def read_from(self, start):
        return self.read(start, self.filled - start)

    async def append_async(self, data):
        self.append(data)
        async with self.new_data_condition:
            self.new_data_condition.notify_all()

    async def read_async(self, start, lentght):
        while start + lentght > self.stop:
            async with self.new_data_condition:
                await self.new_data_condition.wait()
        return self.read(start, lentght)

    async def read_from_async(self, start):
        while True:
            if start < self.stop:
                return self.read_from(start)

            async with self.new_data_condition:
                await self.new_data_condition.wait()

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

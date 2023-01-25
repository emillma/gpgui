import asyncio
from pathlib import Path
import os
import re

import ffmpeg
import quart

app = quart.Quart("apekatt")

video_name = Path(__file__).parent / "lions.mp4"
metadata = ffmpeg.probe(video_name)


async def chunk_generator(start, chunk_size):
    try:
        with open(video_name, "rb") as f:
            f.seek(start)
            while data := f.read(chunk_size):
                yield data
                await asyncio.sleep(0)
    except asyncio.CancelledError:
        pass


@app.route("/livestream")
async def serve_file():
    file_size = os.stat(video_name).st_size
    range_header = quart.request.headers.get("Range", None)
    chunk_size = 32 * 1024

    match = re.search(r"(\d+)-(\d*)", range_header or "") or [None, None, None]
    start, end = int(match[1] or 0), int(match[2] or file_size - 1)

    return await quart.make_response(
        chunk_generator(start, chunk_size),
        206,
        {
            "content-type": "video/mp4",
            "Content-Range": f"bytes {start}-{end}/{file_size}",
        },
    )


app.run(port=5000)

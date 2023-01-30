from pathlib import Path
from PIL import Image
import asyncio

import ffmpeg
import numpy as np

out_filename = Path(__file__).parent / "outfile"


height, width = 512, 512


async def translate():
    args2 = (
        ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s=f"{width}x{height}",
            framerate=25,
        )
        .output(
            "pipe:",
            codec="libx265",
            preset="fast",
            f="ismv",
            # movflags="frag_keyframe+empty_moov",
            # crf=5,
            # **{"x265-params": "lossless=1"},
            # crf=0,
            # qp=0,
        )
        .overwrite_output()
    )

    proc2 = await asyncio.create_subprocess_exec(
        *args2.compile(),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        # stderr=asyncio.subprocess.PIPE,
    )
    for i in range(50):
        in_bytes = (
            np.random.randint(0, 255, [height, width, 3]).astype(np.uint8).tobytes()
        )
        proc2.stdin.write(in_bytes)
        await proc2.stdin.drain()
    proc2.stdin.close()

    ret2 = await proc2.communicate()
    with open(out_filename, "wb") as f:
        f.write(ret2[0])
    probed = ffmpeg.probe(out_filename)
    nframes = int(probed["streams"][0]["nb_frames"])
    total_size = int(probed["format"]["size"])
    compression = total_size / (nframes * width * height * 3)
    print("compression", compression)


asyncio.run(translate())

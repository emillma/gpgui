from pathlib import Path
from PIL import Image
import asyncio

import ffmpeg
import numpy as np

in_filename = Path(__file__).parent / "lions.mp4"
out_filename = Path(__file__).parent / "lions_out.mp4"


height, width = (
    ffmpeg.probe(in_filename)["streams"][0]["height"],
    ffmpeg.probe(in_filename)["streams"][0]["width"],
)


async def translate():
    args1 = ffmpeg.input(str(in_filename)).output(
        "pipe:", format="rawvideo", pix_fmt="rgb24", vframes=50
    )

    args2 = (
        ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s=f"{width}x{height}",
            framerate=25,
        )
        .output(
            str(out_filename),
            codec="libx265",
            preset="fast",
            **{"x265-params": "lossless=1"},
            # crf=0,
            # qp=0,
        )
        .overwrite_output()
    )

    proc1 = await asyncio.create_subprocess_exec(
        *args1.compile(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        limit=width * height * 3,
    )
    proc2 = await asyncio.create_subprocess_exec(
        *args2.compile(),
        stdin=asyncio.subprocess.PIPE,
        # stdout=asyncio.subprocess.PIPE,
        # stderr=asyncio.subprocess.PIPE,
    )
    while True:
        try:
            in_bytes = await proc1.stdout.readexactly(width * height * 3)
        except asyncio.IncompleteReadError as e:
            assert not e.partial
            break

        in_arr: np.ndarray = np.frombuffer(in_bytes, np.uint8)  # type: ignore
        in_frame = in_arr.reshape([height, width, 3])
        out_frame = in_frame
        proc2.stdin.write(out_frame.astype(np.uint8).tobytes())
        await proc2.stdin.drain()
    proc2.stdin.close()

    ret1 = await proc1.communicate()
    ret2 = await proc2.communicate()

    probed = ffmpeg.probe(out_filename)
    nframes = int(probed["streams"][0]["nb_frames"])
    total_size = int(probed["format"]["size"])
    compression = total_size / (nframes * width * height * 3)
    print("compression", compression)


async def verify_lossless():
    args1 = ffmpeg.input(str(in_filename)).output(
        "pipe:", format="rawvideo", pix_fmt="rgb24", vframes=200
    )

    args2 = ffmpeg.input(str(out_filename)).output(
        "pipe:", format="rawvideo", pix_fmt="rgb24"
    )

    proc1 = await asyncio.create_subprocess_exec(
        *args1.compile(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        limit=width * height * 3,
    )
    proc2 = await asyncio.create_subprocess_exec(
        *args2.compile(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        limit=width * height * 3,
    )

    while True:
        try:
            img1_bytes = await proc1.stdout.readexactly(width * height * 3)
            img2_bytes = await proc2.stdout.readexactly(width * height * 3)
        except asyncio.IncompleteReadError as e:
            assert not e.partial
            break

        img1_arr: np.ndarray = np.frombuffer(img1_bytes, np.uint8)  # type: ignore
        img1 = img1_arr.reshape([height, width, 3])

        img2_arr: np.ndarray = np.frombuffer(img2_bytes, np.uint8)  # type: ignore
        img2 = img2_arr.reshape([height, width, 3])
        print(np.bincount(np.abs(img1.astype(int) - img2).ravel()))
        # assert np.all(img1 == img2)

    ret1 = await proc1.communicate()
    ret2 = await proc2.communicate()


asyncio.run(translate())
asyncio.run(verify_lossless())

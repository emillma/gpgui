import asyncio
from PIL import Image
from io import BytesIO
import base64
import re
import requests
from pathlib import Path
import os
import time
from typing import Generator

import quart
import ffmpeg
import numpy as np

from gpgui import dcc, dash, dmc, idp, html, dash_player, html
from gpgui.cbtools import cbm, no_update
from gpgui.sockets import Message, SocketComponentPubSub, SocketClientPubSub
from gpgui.streaming import TestVideoSource

dash.register_page(__name__)


layout = dmc.Paper(
    [
        html.Video(
            src="/livestream",
            controls=True,
            # autoPlay=True,
            # preload="auto",
        ),
        # dash_player.DashPlayer(
        #     id=idp.player,
        #     url="/livestream",
        #     # controls=True,
        #     playing=True,
        #     # playbackRate=2,
        # ),
        dmc.Text(id=idp.text_current_time, p="xl"),
        dmc.Text(id=idp.text_time_loaded, p="xl"),
        dmc.Text(id=idp.text_time_total, p="xl"),
        dmc.Text(id=idp.testing, p="xl"),
    ],
    p="xl",
)


streamer = Streamer(
    TestVideoSource(),
    chunk_size=1024,
    buffer_size=2**30,
)


# async def foo():
#     await streamer.start()
#     frames = [frame async for frame in streamer.get_generator(0, 10000)]
#     await streamer.stop()
#     with open("assets/test.mp4", "wb") as f:
#         f.write(b"".join(frames))


# asyncio.run(foo())
# here = True


@cbm.route("/livestream")
async def serve_file():
    if not streamer.running:
        await streamer.start()
    file_size = 2**30

    range_header = quart.request.headers.get("Range", "bytes=0-")
    match = re.match(r"bytes=(\d+)-(\d*)", range_header)
    start, end = int(match[1]), int(match[2] or file_size - 1)

    # frames = [frame async for frame in streamer.get_generator(start, end)]
    # data = b"".join(frames)

    res = await quart.make_response(
        streamer.get_generator(start, end),
        200,
        {
            # "content-type": "application/dash+xml",
            "content-type": "application/dash+xml",
            # "Content-Range": f"bytes {start}-{end}/{file_size}",
        },
    )
    res.timeout = None
    return res


# @cbm.js_callback(idp.player.as_output("playing"))
# async def update_time_loaded(time=idp.player.as_input("secondsLoaded")):
#     """return true"""


# @cbm.js_callback(idp.text_current_time.as_output("children"))
# async def update_current_time(time=idp.player.as_input("currentTime")):
#     """return `Current time: ${time}`"""


# @cbm.js_callback(idp.text_time_loaded.as_output("children"))
# async def update_time_loaded(time=idp.player.as_input("secondsLoaded")):
#     """return `Time loaded: ${time}`"""


# @cbm.js_callback(idp.text_time_total.as_output("children"))
# async def update_time_total(time=idp.player.as_input("duration")):
#     """return `Time total: ${time}`"""


# @cbm.callback(idp.player.as_output("url"), prevent_initial_call=True)
# async def reset_video(
#     secondsLoaded=idp.player.as_input("secondsLoaded"),
#     url=idp.player.as_state("url"),
# ):
#     if float(secondsLoaded or 0) > 35:
#         return f"/live_video?a={time.time()}"
#     return no_update
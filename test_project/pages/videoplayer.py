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

from gpgui import dcc, dash, dmc, idp, html, dash_player
from gpgui.cbtools import cbm, no_update
from gpgui.sockets import Message, SocketComponent, SocketClient
from gpgui.streaming import TestVideoSource, Streamer

dash.register_page(__name__)


layout = dmc.Paper(
    [
        dash_player.DashPlayer(
            id=idp.player,
            url="/livestream",
            # controls=True,
            playing=True,
        ),
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


@cbm.route("/livestream")
async def serve_file():
    if not streamer.running:
        await streamer.start()
    file_size = 30 * 1024
    range_header = quart.request.headers.get("Range", None)

    match = re.search(r"(\d+)-(\d*)", range_header or "") or [None, None, None]
    start, end = int(match[1] or 0), int(match[2] or file_size - 1)

    frames = [frame async for frame in streamer.get_generator(start, end)]
    data = b"".join(frames)
    with open("test", "wb") as f:
        f.write(data)
    # data = sum(
    #     [frame async for frame in streamer.get_generator(0, 1024 * 4)], start=b""
    # )

    res = await quart.make_response(
        data[start:end],
        206,
        {
            "content-type": "video/mp4",
            "Content-Range": f"bytes {start}-{end}/{file_size}",
        },
    )
    res.timeout = None
    return res


@cbm.js_callback(idp.text_current_time.as_output("children"))
async def update_current_time(time=idp.player.as_input("currentTime")):
    """return `Current time: ${time}`"""


@cbm.js_callback(idp.text_time_loaded.as_output("children"))
async def update_time_loaded(time=idp.player.as_input("secondsLoaded")):
    """return `Time loaded: ${time}`"""


@cbm.js_callback(idp.text_time_total.as_output("children"))
async def update_time_total(time=idp.player.as_input("duration")):
    """return `Time total: ${time}`"""


# @cbm.callback(idp.player.as_output("url"), prevent_initial_call=True)
# async def reset_video(
#     secondsLoaded=idp.player.as_input("secondsLoaded"),
#     url=idp.player.as_state("url"),
# ):
#     if float(secondsLoaded or 0) > 35:
#         return f"/live_video?a={time.time()}"
#     return no_update

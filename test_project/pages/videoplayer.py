import asyncio
from PIL import Image
from io import BytesIO
import base64
import re
import requests
from pathlib import Path
import os

import quart
import numpy as np
import ffmpeg

from gpgui import dcc, dash, dmc, idp, html, dash_player
from gpgui.cbtools import cbm, no_update
from gpgui.sockets import Message, SocketComponent, SocketClient


dash.register_page(__name__)


layout = dmc.Paper(
    [
        dash_player.DashPlayer(
            id=idp.player,
            url="/live_video",
            controls=True,
            playing=True,
        ),
        dmc.Text(id=idp.text_current_time, p="xl"),
        dmc.Text(id=idp.text_time_loaded, p="xl"),
        dmc.Text(id=idp.text_time_total, p="xl"),
    ],
    p="xl",
)

datadir = Path.cwd() / "data"
video_name = str(datadir / "lions.mp4")
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


@cbm.route("/live_video")
async def serve_file():
    file_size = os.stat(video_name).st_size
    range_header = quart.request.headers.get("Range", None)
    chunk_size = 1024 * 1024

    match = re.search(r"(\d+)-(\d*)", range_header) or [None, None, None]
    start, end = int(match[1] or 0), int(match[2] or file_size - 1)

    return await quart.make_response(
        chunk_generator(start, chunk_size),
        206,
        {
            "content_type": "video/mp4",
            "Content-Range": f"bytes {start}-{end}/{file_size}",
        },
    )


@cbm.js_callback(idp.text_current_time.as_output("children"))
async def update_current_time(time=idp.player.as_input("currentTime")):
    """return `Current time: ${time}`"""


@cbm.js_callback(idp.text_time_loaded.as_output("children"))
async def update_time_loaded(time=idp.player.as_input("secondsLoaded")):
    """return `Time loaded: ${time}`"""


@cbm.js_callback(idp.text_time_total.as_output("children"))
async def update_time_total(time=idp.player.as_input("duration")):
    """return `Time total: ${time}`"""

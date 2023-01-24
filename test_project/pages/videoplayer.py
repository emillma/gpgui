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
            id=idp.player2,
            url="/assets/lions.mp4",
            # url="https://www.youtube.com/watch?v=zqLEO5tIuYs",
            controls=True,
            playing=True,
            loop=False,
        ),
        dash_player.DashPlayer(
            id=idp.player,
            url="/live_video",
            # url="/assets/lions.mp4",
            # url="https://www.youtube.com/watch?v=zqLEO5tIuYs",
            controls=True,
            playing=True,
            loop=False,
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


@cbm.route("/live_video")
async def serve_file():
    range_header = quart.request.headers.get("Range", "")
    file_size = os.stat(video_name).st_size

    chunk_size = 1024**2
    match = re.match("bytes=(\d+)-(\d*)", range_header) or [None] * 3
    start = int(match[1] or 0)
    end = int(match[2] or file_size - 1)

    async def generator():
        with open(video_name, "rb") as f:
            f.seek(start)
            while (data := f.read(chunk_size)) and f.tell() < end:
                a = yield data
                print(a)
                print(len(data))

    resp = await quart.make_response(generator())
    # resp.status_code = 206
    # resp.mimetype = "video/mp4"
    resp.content_type = "video/mp4"
    # resp.timeout = None
    # resp.direct_passthrough = True
    # resp.headers["Content-Range"] = f"bytes {start}-{file_size}/{file_size}"
    return resp


@cbm.js_callback(idp.text_current_time.as_output("children"))
async def update_current_time(time=idp.player.as_input("currentTime")):
    """return `Current time: ${time}`"""
    return f"Current time: {time}"


@cbm.js_callback(idp.text_time_loaded.as_output("children"))
async def update_time_loaded(time=idp.player.as_input("secondsLoaded")):
    """return `Time loaded: ${time}`"""
    return f"Time loaded: {time}"


@cbm.js_callback(idp.text_time_total.as_output("children"))
async def update_time_total(time=idp.player.as_input("duration")):
    """return `Time total: ${time}`"""
    return f"Time total: {time}"

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


def get_chunk(byte1=None, byte2=None):
    file_size = os.stat(video_name).st_size
    start = 0

    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(video_name, "rb") as f:
        f.seek(start)
        chunk = f.read(length)
    return chunk, start, length, file_size


@cbm.route("/live_video")
async def serve_file():
    range_header = quart.request.headers.get("Range", None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r"(\d+)-(\d*)", range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])

    chunk, start, length, file_size = get_chunk(byte1, byte2)
    resp = quart.Response(
        chunk,
        206,
        mimetype="video/mp4",
        content_type="video/mp4",
    )
    resp.headers.add(
        "Content-Range",
        "bytes {0}-{1}/{2}".format(start, start + length - 1, file_size),
    )
    return resp


@cbm.callback(idp.text_current_time.as_output("children"))
async def update_current_time(time=idp.player.as_input("currentTime")):
    return f"Current time: {time}"


@cbm.callback(idp.text_time_loaded.as_output("children"))
async def update_time_loaded(time=idp.player.as_input("secondsLoaded")):
    return f"Time loaded: {time}"


@cbm.callback(idp.text_time_total.as_output("children"))
async def update_time_total(time=idp.player.as_input("duration")):
    return f"Time total: {time}"

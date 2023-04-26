import asyncio
import re
from pathlib import Path
import os

import quart
import ffmpeg

from gpgui import dash, dmc, idp, dash_player
from gpgui.cbtools import cbm


dash.register_page(__name__)
idp = idp.video_file_streamer

layout = dmc.Paper(
    [
        dash_player.DashPlayer(
            id=idp.player,
            url="/livestream3",
            controls=True,
            currentTime=20,
            playing=True,
        ),
        dmc.Text(id=idp.text_current_time, p="xl"),
        dmc.Text(id=idp.text_time_loaded, p="xl"),
        dmc.Text(id=idp.text_time_total, p="xl"),
        dmc.Text(id=idp.testing, p="xl"),
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


@cbm.route("/livestream3")
async def serve_lionthing():
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

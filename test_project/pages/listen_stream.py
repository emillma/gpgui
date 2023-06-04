import asyncio
import re
from pathlib import Path
import os

import quart
from quart import redirect

from gpgui import dash, dmc, idp, dash_player, html
from gpgui.cbtools import cbm
import shlex

dash.register_page(__name__)
idp = idp.listen_stream

layout = dmc.Paper(
    [
        dash_player.DashPlayer(
            id=idp.player,
            url="/mystream",
            controls=True,
            # currentTime=20,
            playing=True,
        ),
        dmc.Text(id=idp.text_current_time, p="xl"),
        dmc.Text(id=idp.text_time_loaded, p="xl"),
        dmc.Text(id=idp.text_time_total, p="xl"),
        dmc.Text(id=idp.testing, p="xl"),
    ],
    p="xl",
)


async def gen():
    move = (
        "gst-launch-1.0 videotestsrc is-live=true"
        " ! x264enc"
        " ! video/x-h264,width=640,height=480,framerate=30/1"
        " ! h264parse "
        " ! mp4mux streamable=true fragment-duration=1 presentation-time=true "
        " ! filesink location=/dev/stdout"
    )
    proc = await asyncio.create_subprocess_exec(
        *shlex.split(move),
        stdout=asyncio.subprocess.PIPE,
        # stderr=asyncio.subprocess.PIPE,
    )
    while True:
        try:
            data = await proc.stdout.read(1024 * 8)
            if not data:
                break
            yield data
        except asyncio.CancelledError as e:
            print(e)
            break


async def tmptest():
    async for data in gen():
        print(data)


# asyncio.run(tmptest())


@cbm.route("/mystream")
async def foo():
    resp = await quart.make_response(
        gen(),
        200,
        {
            "content-type": "video/mp4",
        },
    )
    resp.timeout = None
    return resp


@cbm.js_callback(idp.text_current_time.as_output("children"))
async def update_current_time(time=idp.player.as_input("currentTime")):
    """return `Current time: ${time}`"""


@cbm.js_callback(idp.text_time_loaded.as_output("children"))
async def update_time_loaded(time=idp.player.as_input("secondsLoaded")):
    """return `Time loaded: ${time}`"""


@cbm.js_callback(idp.text_time_total.as_output("children"))
async def update_time_total(time=idp.player.as_input("duration")):
    """return `Time total: ${time}`"""

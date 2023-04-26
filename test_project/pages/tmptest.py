import asyncio
from gpgui import dash, dmc, idp, html, dash_player
from gpgui.cbtools import cbm
from quart import make_response

import time

dash.register_page(__name__)
idp = idp.hello


layout = dmc.Paper(
    [
        dmc.Text(id=idp.text_output, p="xl", children="abrakadabrs"),
        dash_player.DashPlayer(
            id=idp.player,
            url="/somevideo",
            controls=True,
            # currentTime=20,
            playing=True,
        ),
        # html.Video(id=idp.video, src="/somevideo"),
    ],
    p="xl",
)


@cbm.route("/somevideo")
async def somevideo():
    reader, _ = await asyncio.open_connection("10.53.58.89", 8876)

    async def generator():
        while True:
            data = await reader.read(1024**64)
            yield data

    response = await make_response(generator())
    response.timeout = None  # No timeout for this route

    return response

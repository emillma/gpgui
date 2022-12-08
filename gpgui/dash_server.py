"""Main app module."""
import os
import logging

import dash
import dash_labs as dl

from dash import html, dcc, Dash

from async_dash import Dash
from dash_extensions.enrich import html, dcc

from gpgui import idp
from gpgui.layout import stylesheets, navbar, configure_plotly
from quart import websocket, json
import asyncio
import random

configure_plotly()
app = Dash(
    __name__,
    external_stylesheets=stylesheets,
    use_pages=True,
    assets_ignore="myfuncs.js",
)

app.layout = html.Div(
    [
        navbar(),
        dash.page_container,
        dcc.Store(id=idp.intermediate_value),
    ],
)


@app.server.websocket("/ws")
async def ws():
    while True:
        output = json.dumps([random.randint(200, 1000) for _ in range(6)])
        await websocket.send(output)
        await asyncio.sleep(1)


def run():
    """Run the gui."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Dash server")
    idp.generate_code()

    try:
        app.run(debug=True, use_reloader=True, port=8050)
    except SystemExit as e:
        os._exit(3)  # pylint: disable=all


if __name__ == "__main__":
    idp.a
    idp.b
    idp.b.c
    idp.a.b.c
    idp.generate_code()
    # app.run(debug=True, use_reloader=True, port=8050)

    # run()

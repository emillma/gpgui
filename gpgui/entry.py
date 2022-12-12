from typing import Callable
import json
from pathlib import Path
import asyncio
import time
from quart import send_from_directory, websocket

import gpgui
from gpgui import MyDash, html, WebSocket, idp
from gpgui.cbtools import cbm, Input, Output

# from gpgui.layout import navbar, page_container


gpgui_dir = Path(gpgui.__path__[0])
extra_assets_dir = gpgui_dir / "extra_assets"

socket_cb = """function(msg){console.log(msg);return msg;}"""


def get_dash_app(layout: Callable[[], html.Div], name="__main__"):
    dash_app = MyDash(
        name,
        external_stylesheets=[
            "extra_assets/style.css",
            # "extra_assets/sandstone.css",
        ],
        external_scripts=[
            # "extra_assets/midi.js",
            "extra_assets/watchdog.js",
            # "extra_assets/requests.js",
        ],
        use_pages=True,
        pages_folder="pages",
    )

    dash_app.layout = html.Div(
        [
            layout(),
            # WebSocket(id=idp.watchdog, url="ws://127.0.0.1:8050/watchdog"),
        ]
    )

    cbm.register(dash_app)

    # @dash_app.callback(
    #     Output(idp.watchdog, "send"),
    #     Input(idp.watchdog, "message"),
    # )
    # async def watchdog(msg):
    #     # print(msg)
    #     return msg

    @dash_app.server.route("/extra_assets/<path:path>")
    async def extra_assets(path):
        return await send_from_directory(extra_assets_dir, path)

    @dash_app.server.route("/hartbeat")
    async def hartbeat():
        return "", 200

    # @dash_app.server.websocket("/watchdog")
    # async def watchdog_socket():
    #     while True:
    #         output = f"hello {time.time()}"
    #         await websocket.send(output)
    #         await asyncio.sleep(1)

    return dash_app

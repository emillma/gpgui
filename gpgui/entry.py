from typing import Callable
from pathlib import Path
import time
from quart import send_from_directory

import gpgui
from gpgui import MyDash, html
from gpgui.cbtools import cbm
from gpgui import exceptions
from quart import Quart
import sys


gpgui_dir = Path(gpgui.__path__[0])
extra_assets_dir = gpgui_dir / "extra_assets"


def get_dash_app(layout: Callable[[], html.Div], name="__main__"):
    quart = Quart(name)
    cbm.quart = quart

    dash_app = MyDash(
        name,
        external_stylesheets=[
            "extra_assets/style.css",
        ],
        external_scripts=[
            # "extra_assets/midi.js",
            "extra_assets/watchdog.js",
            # "extra_assets/requests.js",
        ],
        use_pages=True,
        pages_folder="pages",
    )

    dash_app.layout = layout()

    cbm.register(dash_app)

    hashval = time.time()

    @cbm.quart.route("/hartbeat")
    async def hartbeat():
        return str(hashval), 200

    @cbm.quart.route("/extra_assets/<path:path>")
    async def extra_assets(path):
        return await send_from_directory(extra_assets_dir, path)

    @cbm.quart.errorhandler(exceptions.CallbackException)
    async def callback_exception_handler(e):
        sys.exit(e)

    return dash_app

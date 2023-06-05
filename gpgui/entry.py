from typing import Callable
from pathlib import Path
import time
from quart import send_from_directory, redirect

import gpgui
from gpgui import MyDash, html, exceptions, dcc, idp
from gpgui.cbtools import cbm, PreventUpdate
from gpgui.layout import configure_plotly

from gpgui import sockets
from quart import Quart
import sys
import hypercorn

gpgui_dir = Path(gpgui.__path__[0])
extra_assets_dir = gpgui_dir / "extra_assets"


def get_dash_app(
    layout: Callable[[], html.Div], name="__main__", log_level=None
) -> MyDash:
    configure_plotly()

    if log_level is not None:
        hypercorn.Config.loglevel = log_level

    quart = Quart(name)
    quart.secret_key = "secret"

    # @quart.errorhandler(exceptions.CallbackException)
    # async def callback_exception_handler(e):
    #     sys.exit(e)

    dash_app = MyDash(
        name,
        server=quart,
        external_stylesheets=[
            # "/extra_assets/style.css",
            # "/extra_assets/sandstone.css",
        ],
        external_scripts=[
            # "extra_assets/midi.js",
            "/extra_assets/watchdog.js",
            # "extra_assets/requests.js",
        ],
        use_pages=True,
        pages_folder="pages",
        suppress_callback_exceptions=True,
    )

    dash_app.layout = layout()

    hashval = time.time()

    @cbm.route("/hartbeat")
    async def hartbeat():
        return str(hashval)

    @cbm.route("/extra_assets/<path:path>")
    async def extra_assets(path):
        return await send_from_directory(extra_assets_dir, path)

    cbm.register(dash_app)
    idp.generate_code()

    return dash_app

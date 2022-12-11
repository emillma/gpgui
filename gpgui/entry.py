from typing import Callable
from gpgui import MyDash, CbManager

# from gpgui.layout import navbar, page_container
import gpgui
from pathlib import Path

from quart import send_from_directory


gpgui_dir = Path(gpgui.__path__[0])
extra_assets_dir = gpgui_dir / "extra_assets"


def get_dash_app(layout: Callable, name="__main__"):
    dash_app = MyDash(
        name,
        external_stylesheets=[
            "extra_assets/style.css",
            # "extra_assets/sandstone.css",
        ],
        external_scripts=["extra_assets/midi.js"],
        use_pages=True,
        pages_folder="pages",
    )

    dash_app.layout = layout()
    CbManager.register(dash_app)

    @dash_app.server.route("/extra_assets/<path:path>")
    async def extra_assets(path):
        return await send_from_directory(extra_assets_dir, path)

    return dash_app

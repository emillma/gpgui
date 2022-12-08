from gpgui import Dash, dcc, html, Input, Output, State, idp
from gpgui.layout import navbar, page_container
import gpgui
from pathlib import Path

from quart import send_from_directory


gpgui_dir = Path(gpgui.__path__[0])


def get_dash_app(layout, name="__main__"):
    dash_app = Dash(
        name,
        external_stylesheets=[
            "extra_assets/style.css",
            "extra_assets/sandstone.css",
        ],
        use_pages=True,
    )

    dash_app.layout = layout

    @dash_app.server.route("/extra_assets/<path:path>")
    async def extra_assets(path):
        return await send_from_directory(gpgui_dir / "extra_assets", path)

    return dash_app

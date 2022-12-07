"""Main app module."""
import os
import logging

import dash
import dash_labs as dl

from dash import html, dcc, Dash

from async_dash import Dash
from dash_extensions.enrich import html, dcc

from gpgui.idprovider import idp
from gpgui.layout import stylesheets, navbar, configure_plotly

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


@app.server.route("/favicon.ico")
async def favicon():
    return {"hello": "world"}


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
    app.run(debug=True, use_reloader=True, port=8050)

    run()

from gpgui import Dash, dcc, html, Input, Output, State, idp
from gpgui.layout import navbar, page_container
import gpgui
from pathlib import Path
from gpgui.entry import get_dash_app
import dash

layout = html.Div(
    [
        navbar(),
        page_container(),
    ],
)
dash_app = get_dash_app(layout)


dash_app.run(debug=True, use_reloader=False, port=8050)

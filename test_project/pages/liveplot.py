"""analytics"""
import dash
from dash_extensions import WebSocket
from dash_extensions.enrich import (
    html,
    dcc,
    Input,
    Output,
)

# from gpgui.cbtools import callback

dash.register_page(__name__, path="/liveplot")

layout = html.Div([WebSocket(id="ws"), dcc.Graph(id="graph")])

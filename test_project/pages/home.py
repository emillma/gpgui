"""analytics"""
import dash
from dash import html, dcc
from dash_extensions import 


dash.register_page(__name__, path="/")

layout = html.Div(
    [
        dcc.Markdown("Analytics"),
    ]
)

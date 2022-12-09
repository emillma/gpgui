"""analytics"""
import dash
from dash import html, dcc

dash.register_page(__name__, path="/home")

layout = html.Div(
    [
        dcc.Markdown("Analytics"),
    ]
)

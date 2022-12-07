"""Page to test scrollbar"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = dbc.Container(
    dbc.Card(
        dcc.Markdown("\n\n".join(f"abc_{i:02d}" for i in range(100))),
        style={"max-height": "12rem", "overflow": "auto"},
    )
)

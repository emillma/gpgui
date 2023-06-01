import asyncio
from gpgui import dash, dmc, idp, html, dash_player, dcc, colors
from gpgui.cbtools import cbm
from quart import make_response
from gpgui.sockets import Message, SocketComponentPath
from dash_extensions import WebSocket
from websockets.legacy import server
import plotly.express as px
import time
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__)
idp = idp.plot_colors

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5


# Create traces
texts = []
fig = go.Figure()
for i, (color, cname) in enumerate(zip(colors.defaults, colors.names)):
    fig.add_trace(
        go.Scatter(
            x=random_x,
            y=np.random.randn(N) - 4 * i,
            mode="lines+markers",
            name=f"Plot {i}",
        )
    )
    texts.append(
        dmc.Text(
            dcc.Markdown(r"$\sum_{n=1}^{\infty} 2^{-n} = 1$ in " + cname, mathjax=True),
            color=color,
        ),
    )

layout = dmc.Paper(
    [
        dcc.Graph(figure=fig, config={"scrollZoom": True}),
        dmc.Grid(children=[dmc.Col(t, span=2) for t in texts], gutter="xl"),
    ],
    p="xl",
)

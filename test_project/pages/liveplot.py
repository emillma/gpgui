"""analytics"""
import dash
from dash_extensions import WebSocket
from dash_extensions.enrich import (
    html,
    dcc,
    Input,
    Output,
)
import plotly.express as px

# from gpgui.cbtools import callback

dash.register_page(__name__, path="/liveplot")
df = px.data.gapminder()
fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)

layout = html.Div(
    [
        dcc.Markdown("hello world"),
        WebSocket(id="ws"),
        dcc.Graph(id="graph", figure=fig),
    ]
)

"""analytics"""
import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import plotly.io as pio
import dash_bootstrap_components as dbc
import plotly.express as px
from collections import UserDict
from dash.dependencies import Input, Output

dash.register_page(__name__)


df = px.data.gapminder().query("continent=='Europe'")
fig = px.line_3d(df, x="gdpPercap", y="pop", z="year", color="country")
fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})


layout = html.Div(
    children=[
        html.H1(children="This is our Analytics page"),
        html.Div(
            [
                "Select a city: ",
                dcc.RadioItems(
                    ["New York City", "Montreal", "San Francisco"],
                    "Montreal",
                    id="analytics-input",
                ),
            ]
        ),
        html.Br(),
        html.Div(id="analytics-output"),
        html.Br(),
        dbc.Container(
            dbc.Card(
                dcc.Graph(
                    figure=fig,
                    className="w-100 h-100 m-0 p-0",
                ),
                style={"height": "50rem", "width": "50rem"},
            )
        ),
    ]
)


@callback(
    Output(component_id="analytics-output", component_property="children"),
    Input(component_id="analytics-input", component_property="value"),
)
async def update_city_selected(input_value):
    """Update city selected."""
    return f"You selected: {input_value}"

"""analytics"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__)


df = px.data.gapminder().query("continent=='Europe'")
fig = px.line_3d(df, x="gdpPercap", y="pop", z="year", color="country")

layout = html.Div("hello")
# (
#     dbc.Container(
#         [
#             dcc.Markdown("hello"),
#             dbc.Card(
#                 dcc.Graph(
#                     figure=fig,
#                     className="w-100 h-100 m-0 p-0",
#                 ),
#                 className="w-100 h-100 m-0 p-0",
#             ),
#         ]
#     ),
# )


# @callback(
#     Output(component_id="analytics-output", component_property="children"),
#     Input(component_id="analytics-input", component_property="value"),
# )
# def update_city_selected(input_value):
#     """Update city selected."""
#     return f"You selected: {input_value}"

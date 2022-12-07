import plotly.express as px
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)
df = px.data.gapminder()
fig = px.scatter(
    df,
    x="gdpPercap",
    y="lifeExp",
    animation_frame="year",
    animation_group="country",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=55,
    range_x=[100, 100000],
    range_y=[25, 90],
)
speed = 800
# args =
# fig.update_layout(
#     updatemenus=[
#         {
#             "type": "buttons",
#             "buttons": [
#                 {"label": "Your Label", "method": "animate", "args": ["country"]}
#             ],
#         }
#     ]
# )

# fig.layout.updatemenus[0].buttons[0].args = (
#     fig.layout.updatemenus[0].buttons[0],
#     fig.layout.updatemenus[0].buttons[0].args[1],
# )
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = speed
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["easing"] = "linear"
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = speed

# fig.layout.updatemenus[0].buttons[0].args[0] = "counsdftry"

# fig.update_layout(
#     transition={"duration": 0, "easing": "cubic"},
# )
layout = html.Div(dcc.Graph(figure=fig, className="h-100"))

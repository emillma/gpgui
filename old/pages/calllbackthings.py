import dash
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, callback

dash.register_page(__name__)


layout = html.Div(
    [
        html.Button("Add Filter", id="dynamic-add-filter", n_clicks=0),
        html.Div(id="dynamic-dropdown-container", children=[]),
    ]
)


@callback(
    Output("dynamic-dropdown-container", "children"),
    Input("dynamic-add-filter", "n_clicks"),
    State("dynamic-dropdown-container", "children"),
)
async def display_dropdowns(n_clicks, children):
    new_element = html.Div(
        [
            dcc.Dropdown(
                ["NYC", "MTL", "LA", "TOKYO"],
                id={"type": "dynamic-dropdown", "index": n_clicks},
            ),
            html.Div(id={"type": "dynamic-output", "index": n_clicks}),
        ]
    )
    children.append(new_element)
    return children


@callback(
    Output({"type": "dynamic-output", "index": MATCH}, "children"),
    Input({"type": "dynamic-dropdown", "index": MATCH}, "value"),
    State({"type": "dynamic-dropdown", "index": MATCH}, "id"),
)
async def display_output(value, id):
    return html.Div("Dropdown {} = {}".format(id["index"], value))

from gpgui import dmc, idp, html, dash
from gpgui.cbtools import cbm
from gpgui import cbtools as cbt

dash.register_page(__name__)
idp = idp.local_name

layout = dmc.Paper(
    [dmc.Button("Start", id=idp.button, n_clicks=0), dmc.Text(id=idp.text)]
)


# # default server side callback
# @app.callback(
#     Output(component_id="local_name-text", component_property="children"),
#     Input(component_id="local_name-button", component_property="n_clicks"),
# )
# def update_image(clicks):
#     return int(clicks) + 1


# # default cliend side callback
# app.clientside_callback(
#     """
#     update_image(clicks) {
#         return parseInt(clicks) + 1;
#     }
#     """,
#     Output("local_name-text", "children"),
#     Input("local_name-button", "n_clicks"),
# )


# mew server side callback
@cbm.callback(idp.text.children.as_output())
async def update_image(clicks: int = idp.button.n_clicks.as_input()):
    return clicks + 1


# # new client side callback
# @cbm.js_callback(idp.text.children.as_output())
# async def update_image(clicks: int = idp.button.as_input("n_clicks")):
#     """
#     return parseInt(clicks) + 1;
#     """

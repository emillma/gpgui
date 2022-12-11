"""analytics"""
from typing import TypeVar
import dash
from gpgui import dcc, html, dmc, idp, CbManager as cbm

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        dmc.TextInput(id=idp.text_input, placeholder="Enter a value...", value=""),
        dmc.Textarea(
            id=idp.text_area,
            label="Autosize with no rows limit",
            placeholder="Autosize with no rows limit",
            style={"width": 500},
            autosize=True,
            minRows=6,
            maxRows=6,
            value="",
        ),
    ]
)


# @cbm.callback(idp.text_area.output("value"))
# async def set_text(value=idp.text_input.input("value")):
#     return value

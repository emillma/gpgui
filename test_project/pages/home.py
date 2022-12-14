"""analytics"""
from typing import TypeVar
import dash
from gpgui import dcc, html, dmc, idp, EventListener, exceptions, colors
from gpgui.cbtools import cbm, events
import json

dash.register_page(__name__, path="/")


event = {"event": "click", "props": ["type", "timeStamp", "target.children"]}

layout = dmc.Stack(
    [
        dmc.TextInput(id=idp.input, placeholder="Enter a value..."),
        dmc.Paper(
            dmc.ScrollArea(
                dmc.Text(
                    dcc.Markdown(
                        id=idp.log,
                        children="hello, this is a test $x=2^2$\n\n" * 10,
                        mathjax=True,
                    ),
                    color="dimmed",
                ),
                style={"height": "100%"},
            ),
            withBorder=True,
            pl="sm",
            style={"height": "10em"},
        ),
    ],
)


# @cbm.callback(idp.text_area.output("value"))
# async def set_text(value=idp.text_input.input("value")):
#     return value


# @cbm.callback(idp.log.output("children"), prevent_initial_call=True)
# async def click_event(e: events.click | events.keydown = idp.el.input("event")):
#     # print(e)
#     return "clicked!"


@cbm.callback(idp.log.output("children"), prevent_initial_call=True)
async def testfunc(text: str = idp.input.input("value")):
    raise IndexError("test")
    return text

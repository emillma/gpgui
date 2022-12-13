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
        dmc.TextInput(id=idp.text_input, placeholder="Enter a value...", value=""),
        dmc.Textarea(
            id=idp.text_area,
            label="Autosize with no rows limit",
            placeholder="Autosize with no rows limit",
            # style={"width": "md"},
            # size="lg",
            autosize=True,
            minRows=6,
            maxRows=6,
            value="hello\n" * 10,
        ),
        EventListener(
            dmc.TextInput("Click here!"),
            events=[
                events.click.event_dict(),
                events.keydown.event_dict(),
            ],
            logging=True,
            id=idp.el,
        ),
        # dcc.Markdown(id=idp.log, mathjax=True),
        dmc.Paper(
            dmc.Text(
                dcc.Markdown(
                    id=idp.log, children="hello, this is a test $x=2^2$", mathjax=True
                ),
                color="blue",
            ),
            withBorder=True,
            pl="sm",
        ),
    ],
)


# @cbm.callback(idp.text_area.output("value"))
# async def set_text(value=idp.text_input.input("value")):
#     return value


@cbm.callback(idp.log.output("children"), prevent_initial_call=True)
async def click_event(e: events.click | events.keydown = idp.el.input("event")):
    if e is None:
        raise exceptions.PreventUpdate()
    print(e)
    return "clicked!"

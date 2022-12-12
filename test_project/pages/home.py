"""analytics"""
from typing import TypeVar
import dash
from gpgui import dcc, html, dmc, idp, EventListener, exceptions
from gpgui.cbtools import cbm, events
import json

dash.register_page(__name__, path="/")


event = {"event": "click", "props": ["type", "timeStamp", "target.children"]}

layout = html.Div(
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
            dmc.Text("Click here! 1234"),
            events=[events.click.edict()],
            logging=True,
            id=idp.el,
        ),
        dcc.Markdown(id=idp.log, mathjax=True),
    ]
)


# @cbm.callback(idp.text_area.output("value"))
# async def set_text(value=idp.text_input.input("value")):
#     return value


@cbm.callback(idp.log.output("children"))
async def click_event(e: events.click = idp.el.input("event")):
    if e is None:
        raise exceptions.PreventUpdate()
    return json.dumps(e, indent=2)

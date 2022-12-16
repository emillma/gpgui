"""analytics"""
from typing import TypeVar
import dash
from gpgui import dcc, html, dmc, idp, exceptions, colors, sockets
from gpgui.cbtools import cbm, events, PreventUpdate
import json
from urllib.parse import urlparse

dash.register_page(__name__, path="/")


event = {"event": "click", "props": ["type", "timeStamp", "target.children"]}

layout = dmc.Stack(
    [
        sockets.SocketComponent(id=idp.ws, in_topics="stuff"),
        events.EventListener(
            id=idp.event_listener,
            events=[events.change.event_dict()],
            children=dmc.TextInput(
                id=idp.input, type="search", value=["hello", "world"]
            ),
        ),
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


# @cbm.callback(idp.ws.url.as_output())
# async def set_text(href: str = idp.url.href.as_input()):
#     parsed = urlparse(href)
#     parsed = parsed._replace(scheme="ws")._replace(path=f"/{idp.socketmanager}")
#     url_str = parsed.geturl()
#     return url_str


# @cbm.callback()
# async def ws_state(state=idp.ws.state.as_input()):
#     print("socite status", state)


# @cbm.callback(idp.log.output("children"), prevent_initial_call=True)
# async def click_event(e: events.click | events.keydown = idp.el.input("event")):
#     # print(e)
#     return "clicked!"


@cbm.callback(idp.log.children.as_output())
async def testfunc(value: str = idp.input.value.as_input()):
    return str(value)


@cbm.callback(idp.log.children.as_output())
async def eventcb(change: events.change = idp.event_listener.event.as_input()):
    return f"change from {change.target.value}"


# @cbm.callback(idp.log.output("children"), prevent_initial_call=False)
# async def eventcb(input=idp.event_listener.input("event")):
#     return str(input)

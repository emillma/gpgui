"""analytics"""
from typing import TypeVar
import dash
from gpgui import dcc, html, dmc, idp, exceptions, colors, sockets
from gpgui.cbtools import cbm, events, PreventUpdate, no_update
import json
from urllib.parse import urlparse
import time
from dash_extensions import WebSocket

dash.register_page(__name__, path="/")


layout = dmc.Stack(
    [
        sockets.SocketComponent(
            name=idp.server_socket, url="/testsocket", topics=["testtopic"]
        ),
        events.EventListener(
            id=idp.event_listener,
            events=[events.change.event_dict(), events.keydown.event_dict()],
            children=dmc.TextInput(id=idp.input, type="text"),
        ),
        dmc.Paper(
            dmc.ScrollArea(
                dmc.Text(
                    dcc.Markdown(
                        id=idp.log,
                        children="hello, this is a test $x=2^2$\n\n" * 100,
                        mathjax=True,
                    ),
                    color="dimmed",
                ),
                style={"height": "20em"},
            ),
            withBorder=True,
            pl="sm",
            # style={"height": "100em"},
        ),
    ],
)


# @cbm.callback(idp.log.children.as_output())
# async def set_text(data: sockets.types.Publication = idp.myws.ws.message.as_input()):
#     if not data:
#         return no_update

#     return data.data.data


# @cbm.callback()
# async def ws_state(state=idp.ws.state.as_input()):
#     print("socite status", state)


# @cbm.callback(idp.log.output("children"), prevent_initial_call=True)
# async def click_event(e: events.click | events.keydown = idp.el.input("event")):
#     # print(e)
#     return "clicked!"


# @cbm.callback(idp.log.children.as_output())
# async def debounce(value: str = idp.input.debounce.as_input()):
#     if not value:
#         return no_update
#     return str(value)


# @cbm.callback(idp.log.children.as_output())
# async def testfunc(
#     value: str = idp.input.value.as_input(),
#     debounce: str = idp.input.debounce.as_input(),
# ):
#     if not value:
#         return no_update
#     return str(value)


# @cbm.callback(idp.log.children.as_output())
# async def eventcb(
#     event=idp.event_listener.event.as_input(),
# ):
#     if not event:
#         return no_update

# return f"change from {change.target.value}"

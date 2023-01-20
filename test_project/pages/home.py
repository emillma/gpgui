"""analytics"""
from typing import TypeVar
import dash
from gpgui import dcc, html, dmc, idp, exceptions, colors, sockets
from gpgui.cbtools import cbm, events, no_update
from gpgui.sockets import Message

dash.register_page(__name__, path="/")


layout = dmc.Stack(
    [
        sockets.SocketComponent(id=idp.mysocket, pub="topic1", sub="topic1"),
        events.EventListener(
            id=idp.event_listener,
            events=[events.keydown.event_dict()],
            children=dmc.TextInput(id=idp.input, type="text"),
        ),
        dmc.Paper(
            dmc.ScrollArea(
                dmc.Text(
                    dcc.Markdown(
                        id=idp.log,
                        children="",
                        mathjax=True,
                    ),
                    color="dimmed",
                ),
                style={"height": "20em"},
            ),
            withBorder=True,
            pl="sm",
        ),
    ],
)


@cbm.js_callback(idp.log.as_output("children"), prevent_initial_call=True)
async def set_text(message: Message = idp.mysocket.as_input("message")):
    """return message.data"""
    return message.data


@cbm.js_callback(
    idp.mysocket.as_output("send"),
    idp.input.as_output("value"),
    prevent_initial_call=True,
)
async def commit_message(
    event: events.keydown = idp.event_listener.as_input("event"),
):
    """
    if (event.key === "Enter") return [event['target.value'], ""];
    return no_update;
    """
    if event.key == "Enter":
        return [event.target.value, ""]
    return no_update

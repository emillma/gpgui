"""analytics"""
from typing import TypeVar
import dash
from gpgui import dcc, html, dmc, idp, exceptions, colors, sockets
from gpgui.cbtools import cbm, events, no_update
from gpgui.sockets import Message

dash.register_page(__name__, path="/")


layout = dmc.Stack(
    [
        # sockets.SocketComponent(
        #     name=idp.server_socket, url="/testsocket", topics=["testtopic"]
        # ),
        sockets.SocketComponent(id=idp.mysocket, pub="topic1"),
        sockets.SocketComponent(id=idp.mysocket2, sub="topic1"),
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


# @cbm.callback(idp.log.as_output("children"), prevent_initial_call=True)
# async def set_text(message: Message = idp.mysocket2.as_input("message")):
#     return message.data


@cbm.js_callback(
    # idp.mysocket.as_output("send"),
    idp.log.as_output("children"),
    idp.input.as_output("value"),
    prevent_initial_call=True,
)
async def commit_message(
    event: events.keydown = idp.event_listener.as_input("event"),
    text=idp.input.as_state("value"),
):
    """return [text, ""];"""
    if event.key == "Enter":
        return text, ""
    return no_update


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

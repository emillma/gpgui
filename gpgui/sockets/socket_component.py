from dash_extensions import WebSocket
from gpgui.cbtools import cbm, PreventUpdate
from gpgui.idprovider import StrWithChildren

from .annotations import SocketState, Message, CONNECTING, OPEN, CLOSING, CLOSED
import asyncio
import json


class SocketComponent(WebSocket):
    def __init__(self, id: StrWithChildren, in_topics: str | list[str]):
        if isinstance(in_topics, str):
            in_topics = [in_topics]
        self.id = id
        super().__init__(id=id)

        @cbm.callback(id.as_output("send"), prevent_initial_call=True)
        async def initialize(state: SocketState = id.as_input("state")):
            if state.readyState == OPEN:
                return Message(type="subscribe", data=json.dumps(in_topics)).dumps()

            elif state.readyState == CLOSING:
                raise Exception("socket closing")
            elif state.readyState == CONNECTING:
                raise Exception("socket connecting")
            elif state.readyState == CLOSED:
                raise PreventUpdate
            else:
                raise Exception("socket not ready")

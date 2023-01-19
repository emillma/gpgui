from dash_extensions import WebSocket
from gpgui.cbtools import cbm, PreventUpdate, no_update
from gpgui.idprovider import StrWithChildren
from gpgui import html, dcc, idp

from urllib.parse import urlparse, ParseResult

from .types import SocketState, SubscriptionData, CONNECTING, OPEN, CLOSING, CLOSED
import asyncio
import json
import time


class SocketComponent(html.Div):
    """name, name.ws, name.topics, name.url"""

    def __init__(self, name: StrWithChildren, url: str, topics: list[str]):
        self.name = name

        self.static_children = [
            dcc.Store(id=name.topics, data=topics),
            dcc.Store(id=name.target_url, data=url),
            html.Div(id=name.ws_container),
        ]

        super().__init__(id=name, children=self.static_children)

        @cbm.callback(self.name.ws_container.as_output("children"))
        async def register(
            target_url: str = name.target_url.as_input("data"),
            url_page: str = idp.url.as_state("href"),
        ):
            """Called when the url of the socket changes (only once)"""
            url_p = urlparse(target_url)
            url_page_p = urlparse(url_page)

            socket_url = ParseResult(
                scheme="ws",
                netloc=url_p.netloc or url_page_p.netloc,
                path=url_p.path or url_page_p.path,
                params=url_p.params or url_page_p.params,
                query=url_p.query or url_page_p.query,
                fragment=url_p.fragment or url_page_p.fragment,
            ).geturl()

            return WebSocket(id=name.ws + str(time.time()), url=socket_url)

        @cbm.callback(name.ws.as_output("send"))
        async def initialize(
            state: SocketState = name.ws.as_input("state"),
            topics: list[str] = name.topics.as_state("data"),
        ):
            if not state:
                return no_update
            elif state.readyState == OPEN:
                return SubscriptionData(topics=topics or []).dumps()

            elif state.readyState == CLOSING:
                raise Exception("socket closing")
            elif state.readyState == CONNECTING:
                raise Exception("socket connecting")
            elif state.readyState == CLOSED:
                return no_update
            else:
                raise Exception("socket not ready")

        @cbm.callback(None, prevent_initial_call=True)
        async def error(error=name.ws.as_input("error")):
            if error:
                raise Exception(str(error))

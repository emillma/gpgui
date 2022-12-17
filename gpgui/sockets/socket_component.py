from dash_extensions import WebSocket
from gpgui.cbtools import cbm, PreventUpdate, no_update
from gpgui.idprovider import StrWithChildren
from gpgui import html, dcc, idp

from urllib.parse import urlparse, ParseResult

from .types import SocketState, SubscriptionData, CONNECTING, OPEN, CLOSING, CLOSED
import asyncio
import json


class SocketComponent(html.Div):
    """name, name.ws, name.topics, name.url"""

    def __init__(self, name: StrWithChildren, url: str, topics: list[str]):
        self.name = name

        self.static_children = [
            dcc.Store(id=name.topics, data=topics),
            dcc.Store(id=name.url, data=url),
        ]

        super().__init__(id=name, children=self.static_children)

        @cbm.callback(name.as_output("children"))
        async def register(
            url: str = name.url.as_input("data"),
            url_page: str = idp.url.as_state("href"),
        ):
            url_p = urlparse(url)
            url_page_p = urlparse(url_page)

            socket_url = ParseResult(
                scheme="ws",
                netloc=url_p.netloc or url_page_p.netloc,
                path=url_p.path or url_page_p.path,
                params=url_p.params or url_page_p.params,
                query=url_p.query or url_page_p.query,
                fragment=url_p.fragment or url_page_p.fragment,
            ).geturl()

            return self.static_children + [WebSocket(id=name.ws, url=socket_url)]

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

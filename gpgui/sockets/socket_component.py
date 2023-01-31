from dash_extensions import WebSocket
from gpgui.cbtools import cbm, PreventUpdate, no_update, monkey_callback_context
from gpgui.idprovider import StrWithChildren
from gpgui import html, dcc, idp, dash
import dash

from urllib.parse import urlparse, ParseResult

from gpgui.config import PORT, HOST


class SocketComponentPubSub(WebSocket):
    """name, name.ws, name.topics, name.url"""

    def __init__(
        self,
        id: StrWithChildren,  # pylint: disable=redefined-builtin
        pub: str | list[str] | None = None,
        sub: str | list[str] | None = None,
    ):
        pub = [pub] if isinstance(pub, str) else pub or []
        sub = [sub] if isinstance(sub, str) else sub or []
        pub_str = "&".join(f"pub={p}" for p in pub)
        sub_str = "&".join(f"sub={s}" for s in sub)

        url = f"ws://{HOST}:{PORT}/pubsub?{pub_str}&{sub_str}"
        super().__init__(id=id, url=url)


class SocketComponentPath(WebSocket):
    """name, name.ws, name.topics, name.url"""

    def __init__(
        self,
        id: StrWithChildren,  # pylint: disable=redefined-builtin
        path: str,
    ):
        url = f"ws://{HOST}:{PORT}/{path}"
        super().__init__(id=id, url=url)


# @cbm.callback(idp.websockets.as_output("children"))
# async def register(
#     ws_infos=idp.ws_info.as_type_input("data", id=dash.ALL),
#     pathname: str = idp.url.as_input("pathname"),
#     url: str = idp.url.as_state("href"),
#     websockets_old=idp.websockets.as_state("children"),
# ):
#     """Called when the url of the socket changes (only once)"""
#     if monkey_callback_context.triggered_id == idp.url:
#         return []

#     elif monkey_callback_context.triggered_id is None:
#         return no_update

#     elif monkey_callback_context.triggered_id.get("type", None) == "ws_info":
#         websockets_new = []
#         for ws_info in ws_infos:
#             target_p = urlparse(ws_info["url"])
#             url_p = urlparse(url)

#             socket_url = ParseResult(
#                 scheme="ws",
#                 netloc=target_p.netloc or url_p.netloc,
#                 path=target_p.path or url_p.path,
#                 params=target_p.params or url_p.params,
#                 query=target_p.query or url_p.query,
#                 fragment=target_p.fragment or url_p.fragment,
#             ).geturl()
#             websockets_new.append(
#                 WebSocket(id=idp.ws.as_type(id=ws_info["id"]), url=socket_url)
#             )

#         # ws_ids = [ws.id for ws in websockets_new]
#         # for ws in websockets_old or []:
#         #     if ws["props"]["id"] not in ws_ids:
#         #         websockets_new.append(ws)
#         return websockets_new
#     else:
#         raise Exception("unknown callback")


# @cbm.callback(idp.ws.as_type_output("send", id=dash.MATCH))
# async def initialize(
#     state: SocketState = idp.ws.as_type_input("state", id=dash.MATCH),
#     ws_info=idp.ws_info.as_type_input("data", id=dash.MATCH),
# ):
#     if not state:
#         return no_update
#     elif state.readyState == OPEN:
#         return SubscriptionData(topics=ws_info["topics"]).dumps()

#     elif state.readyState == CLOSING:
#         raise Exception("socket closing")

#     elif state.readyState == CONNECTING:
#         raise Exception("socket connecting")

#     elif state.readyState == CLOSED:
#         return no_update

#     else:
#         raise Exception("socket not ready")


# @cbm.callback(None, prevent_initial_call=True)
# async def error(error=name.ws.as_input("error")):
#     if error:
#         raise Exception(str(error))

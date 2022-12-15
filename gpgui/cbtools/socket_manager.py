from quart import Websocket, websocket
from gpgui.cbtools import cbm


class SocketServer:
    sockets: list[Websocket]

    def __init__(self):
        sockets = []

    @cbm.websocket("/socketmanager/<path:socket_id>")
    async def socket_handler(self, socket_id: str):
        pass

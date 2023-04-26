import asyncio
from gpgui import dash, dmc, idp, html, dash_player, dcc
from gpgui.cbtools import cbm
from quart import make_response
from gpgui.sockets import Message, SocketComponentPath
from dash_extensions import WebSocket
from websockets.legacy import server
import plotly.express as px
import time

dash.register_page(__name__)
idp = idp.calibration


def otherthing():
    import numpy as np
    import asyncio
    from websockets.legacy import server
    from websockets.legacy.server import WebSocketServerProtocol
    import cv2

    async def serve_img():
        async def serve(websocket: WebSocketServerProtocol):
            for i in range(100000):
                img = np.zeros((1440, 2560, 3), dtype=np.uint8)
                img[i : i + 4, i : i + 4] = [255, 255, 255]
                data = cv2.imencode(".png", img)[1].tobytes()
                await websocket.send(data)
                await asyncio.sleep(0.05)

        async with server.serve(serve, "10.53.58.89", 9876):
            for i in range(100000):
                print("running", i)
                await asyncio.sleep(1)

    if __name__ == "__main__":
        asyncio.run(serve_img())


layout = dmc.Paper(
    [
        WebSocket(id=idp.socket, url="ws://10.53.58.89:9876"),
        dmc.Affix(
            html.Img(
                id=idp.img,
                src="",
                width="100%",
                height="100%",
            ),
            position={"top": "0", "left": "0"},
            style={"height": "100%", "width": "100%"},
            zIndex=10000,
        ),
    ],
    p="xl",
)


@cbm.js_callback(idp.img.as_output("src"))
async def update_image(message: Message = idp.socket.as_input("message")):
    """
    if (message) {
        return message.data.arrayBuffer().then(buffer => {
            let b64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));
            return "data:image/png;base64," + b64;
        });
    } else {
        return no_update
    };
    """

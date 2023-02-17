import asyncio
from io import BytesIO
import itertools
import time

import base64
from PIL import Image
import numpy as np
import quart
import plotly.graph_objects as go
import cv2

from gpgui import dcc, dash, dmc, idp, html, dash_player, html
from gpgui.cbtools import cbm, no_update
from gpgui.sockets import Message, SocketComponentPath
from gpgui.streaming import TestVideoSource
from dash_extensions import WebSocket
from websockets.legacy import client
import time

dash.register_page(__name__)
idp = idp.videoplayer2


layout = dmc.Paper(
    [
        # SocketComponentPath(id=idp.socket, path="/video"),
        # WebSocket(id=idp.socket, url="ws://10.53.58.89:8083"),
        html.Img(id=idp.img, src="/emil"),
        dmc.Text(id=idp.text_output, p="xl"),
    ],
    p="xl",
)


@cbm.route("/emil")
async def emil():
    async def gen():
        async with client.connect("ws://10.53.58.89:8083") as websocket:
            while True:
                await websocket.send(str(time.time_ns()))
                try:
                    data = await asyncio.wait_for(websocket.recv(), 10)
                    yield (
                        b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + data + b"\r\n"
                    )
                except asyncio.TimeoutError:
                    pass

    resp = await quart.make_response(gen())
    resp.mimetype = "multipart/x-mixed-replace; boundary=frame"
    resp.timeout = None
    return resp

    # resp = await quart.make_response(
    #     gen(),
    #     206,
    #     {"mimetype": "multipart/x-mixed-replace; boundary=frame"},
    # )
    # resp.timeout = None
    # return resp


# @cbm.js_callback(idp.img.as_output("src"))
# async def update_image(message: Message = idp.socket.as_input("message")):
#     """
#     if (message) return message.data; else return no_update;
#     """
#     if message:
#         return message.data
#     else:
#         return no_update

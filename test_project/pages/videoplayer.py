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

dash.register_page(__name__)
idp = idp.videoplayer2


def img_to_str(img: np.ndarray, format="jpeg"):
    with BytesIO() as f:
        Image.fromarray(img).save(f, format=format)
        img_bytes = f.getvalue()
    prefix = f"data:image/{format};base64,"
    img_str = prefix + base64.b64encode(img_bytes).decode("utf-8")
    return img_str


init_img = img_to_str(np.zeros((512, 512, 3), dtype=np.uint8))

layout = dmc.Paper(
    [
        SocketComponentPath(id=idp.socket, path="/video"),
        html.Img(id=idp.img),
        dmc.Text(id=idp.text_output, p="xl"),
    ],
    p="xl",
)


@cbm.websocket("/video")
async def get_image_video():
    socket = quart.websocket

    while True:
        cap = cv2.VideoCapture("assets/lions.mp4")
        for i in itertools.count():
            ret, frame = cap.read()
            if not ret:
                break
            img_str = img_to_str(frame[::2, ::2, ::-1])
            await socket.send(img_str)


@cbm.js_callback(idp.img.as_output("src"))
async def update_image(message: Message = idp.socket.as_input("message")):
    """
    if (message) return message.data; else return no_update;
    """

import asyncio
from PIL import Image
from io import BytesIO
import base64
import time

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from gpgui import dcc, dash, dmc, idp, html
from gpgui.cbtools import cbm, no_update
from gpgui.sockets import Message, SocketComponent, SocketClient

dash.register_page(__name__)


def img_to_str(img: np.ndarray, format="jpeg"):
    with BytesIO() as f:
        Image.fromarray(img).save(f, format=format)
        img_bytes = f.getvalue()
    prefix = f"data:image/{format};base64,"
    img_str = prefix + base64.b64encode(img_bytes).decode("utf-8")
    return img_str


init_img = img_to_str(np.random.randint(0, 255, (1000, 1000, 3), dtype=np.uint8))

layout = dmc.Paper(
    [
        SocketComponent(id=idp.mysocket, sub="video"),
        dcc.Graph(id=idp.graph, figure=go.Figure(go.Image(source=init_img))),
        dmc.Text(id=idp.text),
        html.Div(id=idp.dummy),
    ],
    p="xl",
)

lock = asyncio.Lock()


@cbm.callback(None)
async def socket_publish(dummy=idp.dummy.as_input("id")):
    if lock.locked():
        return

    async with lock, SocketClient(pub="video") as socket:
        for i in range(100000):
            img = np.random.randint(0, 255, (1000, 1000, 3), dtype=np.uint8)
            img_str = img_to_str(img, format="jpeg")

            await socket.send(img_str)
            print("sent")
            await asyncio.sleep(1)


@cbm.js_callback(idp.graph.as_output("figure"), idp.text.as_output("children"))
async def update_graph(
    message: Message = idp.mysocket.as_input("message"),
    figure=idp.graph.as_state("figure"),
):
    """
    if (message){
        figure["data"][0]["source"] = message.data;
        console.log(figure)
        return [figure, message.data.slice(1000, 1100)];
    } else {
        return no_update;
    }
    """
    if not message:
        return no_update
    figure["data"][0]["source"] = message.data
    return figure, message.data[1000:1100]

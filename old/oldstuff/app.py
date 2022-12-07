from flask import Flask, Response
from dash import Dash, dcc, html
from multiprocessing import shared_memory
import numpy as np
import cv2
import time
server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/'
)

app.layout = html.Div([
    html.H1("Webcam Test"),
    html.Img(src="/video_feed")
], id='dash-container')


@server.route("/dash")
def my_dash_app():
    return app.index()


def gen():
    existing_shm = shared_memory.SharedMemory(name='imagedata')
    img = np.ndarray((1024, 1224, 3), dtype=np.uint8, buffer=existing_shm.buf)
    while True:
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        time.sleep(0.01)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@server.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


print('hello')
# app.run_server(debug=True)

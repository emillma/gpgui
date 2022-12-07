"""Video example"""
import numpy as np
import cv2
from flask import Response
import dash
from dash import html
from dash.dependencies import Input, Output, State

def gen():
    """Video streaming generator function."""
    while True:
        img = np.random.randint(0, 256, (400, 400, 3), np.uint8)
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

app = dash.Dash(__name__)

@app.server.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    return Response(gen(), mimetype=mimetype)

app.layout = html.Div([
    html.H1("Webcam Test"),
    html.Img(src="/video_feed")
])

if __name__ == '__main__':
    app.run_server()

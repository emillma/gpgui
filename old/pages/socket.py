from dash_extensions import WebSocket
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy
from dash import clientside_callback, callback, Input, Output, State
import dash
import time

# Client-side function (for performance) that updates the grap

dash.register_page(__name__)

update_graph = """function(msg) {
    if(!msg){return {};}  // no data, just return
    const data = JSON.parse(msg.data);  // read the data
    return {data: [{y: data, type: "scatter"}]}};  // plot the data
"""

update_md = """function(msg) {
    console.log(msg);
    if(!msg){return "";}  // no data, just return
    return msg.data;
    };
"""
# Create small example app.
layout = html.Div(
    [
        WebSocket(id="ws", url="ws://127.0.0.1:5000/time"),
        # html.P(children="hello", id="markdown"),
        dcc.Markdown(children="hello", id="markdown"),
        # dcc.Markdown(children="hello", id="markdown", mathjax=True, className="p-5"),
    ]
)
clientside_callback(update_md, Output("markdown", "children"), Input("ws", "message"))


# @callback(Output("markdown", "children"), Input("ws", "message"))
# def sockcb(msg):
#     print(msg)
#     return f"test {time.time()}"

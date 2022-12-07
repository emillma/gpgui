import logging
import re
import requests
import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import flask

dash.register_page(__name__)


tmap_provider = "https://norgeskart.no/ws/gatekeeper.py?key={key}"

link = (
    "http://gatekeeper1.geonorge.no/BaatGatekeeper/gk/gk.nib_web_mercator_wmts_v2"
    "?gkt={gkt}"
    "&layer=Nibcache_UTM33_EUREF89"
    "&style=default"
    "&tilematrixset=default028mm"
    "&Service=WMTS"
    "&Request=GetTile&Version=1.0.0"
    "&Format=image%2Fpng"
    "&TileMatrix={z}"
    "&TileRow={y}"
    "&TileCol={x}"
)


# @flask_app.route("/tilemap_norway")
# def display_page():
#     """Gets the tile from norgeskart"""
#     args = flask.request.args
#     session = flask.session
#     if session.get("kartverket_url") is None:
#         url = "https://www.norgeskart.no/norgeskart3-2.0.72.js"
#         r = requests.get(url)
#         key = re.search(rb"gatekeeper.py\?key=(\w+)", r.content).group(1).decode()
#         r = requests.get(f"https://norgeskart.no/ws/gatekeeper.py?key={key}")
#         gkt = re.search(rb"\"(\w+)\"", r.content).group(1).decode()
#         session["kartverket_url"] = link.format(gkt=gkt, x="{x}", y="{y}", z="{z}")

#     url = session["kartverket_url"].format(**args)

#     if int(args["z"]) > 19:
#         logging.debug("Zoom level too high")
#         flask.abort(404)
#     return flask.redirect(url)


us_cities = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv"
)

fig = px.scatter_mapbox(
    us_cities,
    lat="lat",
    lon="lon",
    hover_name="City",
    hover_data=["State", "Population"],
    color_discrete_sequence=["fuchsia"],
    zoom=5,
)
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    mapbox_layers=[
        {
            "below": "traces",
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": ["/tilemap_norway?z={z}&x={x}&y={y}"],
            "opacity": 1,
            "maxzoom": 24,
        }
    ],
)


layout = html.Div(dcc.Graph(figure=fig, className="h-100"), className="fullscreen")
# className="h-100"
# className="vh-100",
# style={"flex-direction": "column"},

# className="vh-100",

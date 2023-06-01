import logging
import re
import aiohttp
import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from gpgui.cbtools import cbm
import quart
import asyncio
import plotly.graph_objects as go
import numpy as np

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


lock = asyncio.Lock()


@cbm.route("/tilemap_norway")
async def display_page():
    """Gets the tile from norgeskart"""
    args = quart.request.args
    session = quart.session

    if session.get("kartverket_url", None) is None and not lock.locked():
        await lock.acquire()
        url = "https://www.norgeskart.no/norgeskart3-2.0.72.js"
        async with aiohttp.ClientSession() as req_session:
            async with req_session.get(url) as resp:
                content = await resp.read()
            key = re.search(rb"gatekeeper.py\?key=(\w+)", content).group(1).decode()
            url = f"https://norgeskart.no/ws/gatekeeper.py?key={key}"
            async with req_session.get(url) as resp:
                content = await resp.read()
        gkt = re.search(rb"\"(\w+)\"", content).group(1).decode()
        session["kartverket_url"] = link.format(gkt=gkt, x="{x}", y="{y}", z="{z}")
        await lock.release()

    url = session["kartverket_url"].format(**args)

    if int(args["z"]) > 19:
        logging.debug("Zoom level too high")
        quart.abort(404)
    return quart.redirect(url)


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
    zoom=8,
    center={"lat": 63.4, "lon": 10.4},
)

pos = np.array(
    [
        [63.419949, 10.401514],
        [63.419774, 10.401167],
        [63.419468, 10.401100],
        [63.419347, 10.400831],
        [63.418905, 10.401300],
        [63.418791, 10.402092],
        [63.418143, 10.402714],
        [63.418104, 10.402569],
        [63.416453, 10.404302],
        [63.416686, 10.405469],
        [63.417699, 10.404485],
        [63.417828, 10.404621],
        [63.418369, 10.404031],
    ]
).T
fig.add_trace(
    go.Scattermapbox(
        lat=pos[0],
        lon=pos[1],
        mode="lines+markers",
        name="My line",
    )
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    mapbox_layers=[
        {
            "below": "traces",
            "sourcetype": "raster",
            # "sourceattribution": "United States Geological Survey",
            "source": ["/tilemap_norway?z={z}&x={x}&y={y}"],
            "opacity": 1,
            "maxzoom": 24,
        }
    ],
)


layout = dcc.Graph(figure=fig, style={"width": "100%"})

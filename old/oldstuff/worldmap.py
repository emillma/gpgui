import plotly.express as px
import pandas as pd

us_cities = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv"
)

gkt = "FE7208ADDFAEC03EB650CFED5A95236426718018597E5F00783FEBBA0380FD780B0CE671A5A3FB64272E5068E489ABC2C794D2672D45D69E8D018F0853CD0DA1"
link1 = "http://gatekeeper1.geonorge.no/BaatGatekeeper/gk/gk.nib_web_mercator_wmts_v2"
query = dict(
    gkt=gkt,
    layer="Nibcache_UTM33_EUREF89",
    style="default",
    tilematrixset="default028mm",
    Service="WMTS",
    Request="GetTile&Version=1.0.0",
    Format="image%2Fpng",
    TileMatrix="{z}",
    TileRow="{y}",
    TileCol="{x}",
)
link1 = link1 + "?" + "&".join(f"{k}={v}" for k, v in query.items())

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
    mapbox_layers=[
        {
            "below": "traces",
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [link1],
            "opacity": 1,
            "maxzoom": 17,
        }
    ],
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()

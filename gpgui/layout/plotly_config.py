from typing import Any
import plotly.io as pio
from gpgui import dmc
from dash_bootstrap_components import themes
from gpgui import dmc
from dash_bootstrap_templates import load_figure_template
from gpgui.layout import colors
from plotly.graph_objs.layout import Template
from gpgui import inspect


def configure_plotly():
    template = pio.templates["plotly_dark"]
    layout = template.layout

    layout.font.family = "'Inter', sans-serif"
    layout.xaxis.gridcolor = colors.gray_shades[8]
    layout.yaxis.gridcolor = colors.gray_shades[8]
    layout.colorway = colors.defaults
    layout.paper_bgcolor = colors.transparent
    layout.plot_bgcolor = colors.gray_shades[9]
    inspect.set_props_matching(
        layout, r"marker\.line\.color$", colors.gray_shades[8], regex=True
    )
    pio.templates["mytemplate"] = template
    pio.templates.default = "mytemplate"

import json
import logging
from pathlib import Path

import plotly.io as pio
from plotly.graph_objs.layout import Template

from gpgui.layout import colors
from gpgui import inspect


def configure_plotly(use_cache: bool = True) -> None:
    cache_file = Path(__file__).parent / "plotly_template.json"

    if use_cache and cache_file.exists():
        template = Template(json.loads(cache_file.read_text()))
        logging.info("Using cached plotly template")
    else:
        template = pio.templates["plotly_dark"]
        layout = template.layout

        layout.font.family = "'Inter', sans-serif"
        layout.font.color = colors.white
        layout.paper_bgcolor = colors.transparent

        layout.plot_bgcolor = colors.darks[5]
        layout.xaxis.gridcolor = colors.darks[6]
        layout.yaxis.gridcolor = colors.darks[6]

        layout.colorway = colors.defaults

        layout.margin.t = 40
        layout.margin.r = 40
        layout.margin.b = 40
        layout.margin.l = 40

        layout.modebar.color = colors.darks[3]
        layout.modebar.bgcolor = colors.darks[5]
        layout.modebar.activecolor = colors.darks[0]

        layout.legend.bgcolor = colors.darks[5]
        inspect.set_props(template, r"marker.line.color$", colors.darks[5])
        # inspect.set_props(template, r"marker.line.width$", 1)
        cache_file.write_text(json.dumps(template.to_plotly_json(), indent=2))

    pio.templates["mytemplate"] = template
    pio.templates.default = "mytemplate"

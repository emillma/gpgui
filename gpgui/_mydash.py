from async_dash import Dash as QuartDash
from dash_extensions.enrich import Dash as DashEnrich
from dash import Dash as DashBase


class MyDash(DashEnrich, QuartDash):
    ...

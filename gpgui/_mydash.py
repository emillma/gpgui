from async_dash import Dash as QuartDash
from dash_extensions.enrich import Dash as DashEnrich


class MyDash(DashEnrich, QuartDash):
    ...

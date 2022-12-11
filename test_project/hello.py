from gpgui import dcc, html, idp, dmc
from gpgui.cbtools import Output, Input, DashLogger

from gpgui.layout import navbar, page_container, configure_plotly
from gpgui.entry import get_dash_app
from datetime import date
from gpgui.layout import colors

configure_plotly()


def layout():
    return dmc.MantineProvider(
        theme=dict(
            colorScheme="dark",
            colors=colors.DEFAULT_COLORS,
            fontFamily="'Inter', sans-serif",
        ),
        withGlobalStyles=True,
        withNormalizeCSS=True,
        children=dmc.Paper(
            dmc.Group(
                grow=True,
                direction="column",
                children=[
                    dcc.Markdown("Analytics"),
                    page_container(),
                    dmc.DatePicker(
                        style={"width": 200},
                        label="Select Date",
                        value=date.today(),
                    ),
                    dmc.Alert("This is an alert!", title="An Alert", color="red"),
                ],
            ),
            p="xl",
            # m="xl",
        ),
    )


dash_app = get_dash_app(layout, name=__name__)


# @dash_app.callback(Output("txt", "children"), Input("btn", "n_clicks"), log=True)
# def do_stuff(n_clicks, dash_logger: DashLogger):
#     if not n_clicks:
#         raise PreventUpdate()
#     dash_logger.info("Here goes some info")
#     dash_logger.warning("This is a warning")
#     dash_logger.error("Some error occurred")
#     return f"Run number {n_clicks} completed"

print(type(idp.hello.apekatt))
idp.generate_code()
dash_app.run(
    debug=True, use_reloader=False, dev_tools_hot_reload_max_retry=3, port=8050
)

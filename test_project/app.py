from gpgui import dcc, html, idp, dmc, sockets, config

from gpgui.layout import configure_plotly, page_registry, page_container
from gpgui.entry import get_dash_app
from datetime import date
from gpgui.layout import colors

configure_plotly()


def layout():
    NAVBAR_HEIGHT = "4em"
    NAVBAR_WIDTH = "10em"

    return dmc.MantineProvider(
        theme=dict(
            colorScheme="dark",
            colors=colors.DEFAULT_COLORS,
            fontFamily="'Inter', sans-serif",
            primaryShade=colors.DEFAULT_SHADE,
        ),
        withGlobalStyles=True,
        withNormalizeCSS=True,
        children=[
            dmc.Header(
                dmc.Group(
                    [
                        dmc.Center(dmc.Burger(size="md")),
                        dmc.Center(dmc.Text("GPGUI", size="xl", inline=True)),
                    ],
                    align="left",
                    style={"height": "100%"},
                ),
                pl="xl",
                height="4em",
                fixed=True,
            ),
            dmc.Navbar(
                dmc.ScrollArea(
                    dmc.Stack(
                        [
                            dmc.Anchor(page["name"], href=page["relative_path"])
                            for page in page_registry.values()
                        ],
                        style={"textAlign": "left"},
                    ),
                    dir="rtl",
                    style={"height": "100%", "width": "100%"},
                    p="xl",
                ),
                width={"base": NAVBAR_WIDTH},
                position={"top": NAVBAR_HEIGHT, "left": "0", "bottom": "0"},
                fixed=True,
            ),
            dmc.ScrollArea(
                page_container,
                style={
                    "position": "fixed",
                    "top": NAVBAR_HEIGHT,
                    "left": NAVBAR_WIDTH,
                    "bottom": "0",
                    "right": "0",
                },
            ),
        ],
    )


dash_app = get_dash_app(layout, name=__name__)
app = dash_app.server

idp.generate_code()
dash_app.run(
    debug=True,
    use_reloader=False,
    dev_tools_hot_reload=False,
    # dev_tools_prune_errors=False,
    port=config.PORT,
)

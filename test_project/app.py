from gpgui import dcc, html, idp, dmc, sockets

from gpgui.layout import configure_plotly, page_registry, page_container
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
            primaryShade=colors.DEFAULT_SHADE,
        ),
        withGlobalStyles=True,
        withNormalizeCSS=True,
        children=[
            dmc.Header(
                pl="xl",
                height="4em",
                fixed=True,
                children=dmc.Group(
                    [
                        dmc.Center(dmc.Burger(size="md")),
                        dmc.Center(dmc.Text("GPGUI", size="xl", inline=True)),
                    ],
                    align="left",
                    style={"height": "100%"},
                ),
            ),
            dmc.Navbar(
                dmc.ScrollArea(
                    dmc.Stack(
                        [
                            dmc.Anchor(page["name"], href=page["relative_path"])
                            for page in page_registry.values()
                        ]
                        * 20,
                        style={
                            "width": "100%",
                            "textAlign": "left",
                        },
                    ),
                    dir="rtl",
                    style={"height": "100%", "width": "100%"},
                    px="xl",
                ),
                width={"base": "9em"},
                # height="calc(100vh - 4em)",
                position={"top": "4em", "left": "0", "bottom": "0"},
                fixed=True,
            ),
            html.Div(
                style={
                    "position": "fixed",
                    "top": "4em",
                    "left": "9em",
                    "bottom": "0",
                    "right": "0",
                },
                children=dmc.ScrollArea(
                    dmc.Paper(page_container, p="xl", withBorder=False),
                    style={
                        "height": "100%",
                        "width": "100%",
                    },
                )
                #     # children=dmc.ScrollArea(
                #     #     p="xl",
                #     #     children=[
                #     #         page_container,
                #     #     ],
                #     # style={"height": "100%m", "width": "100%"},
                #     # ),
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
    port=8050,
)

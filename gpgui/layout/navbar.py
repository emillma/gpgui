"""Video example"""
import dash
from dash import html
import dash_bootstrap_components as dbc
from gpgui import idp

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


def navbar():
    """stuff"""
    links = [
        dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["relative_path"]))
        for i, page in enumerate(dash.page_registry.values())
    ]
    return dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Hei ", className="ms-2")),
                        ],
                        className="g-0",
                    ),
                    href="https://plotly.com",
                    style={"textDecoration": "none"},
                    className="me-3",
                ),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            *links,
                            dbc.DropdownMenu(
                                [
                                    dbc.DropdownMenuItem("Item 1"),
                                    dbc.DropdownMenuItem("Item 2"),
                                ],
                                label="Dropdown",
                                nav=True,
                            ),
                        ]
                    ),
                    id=idp.navbar_collapse,
                    is_open=False,
                    navbar=True,
                ),
            ],
            fluid=True,
            className="mx-0",
        ),
        color="primary",
        dark=True,
        style={"height": "3rem"},
    )

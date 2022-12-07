import plotly.io as pio


def configure_plotly():
    mytemplate = pio.templates["seaborn"]
    mytemplate.layout.update(
        # plot_bgcolor="rgba(0, 0, 0, 0)",
        # paper_bgcolor="rgba(0, 0, 0, 0)"
    )
    pio.templates["mytemplate"] = mytemplate
    pio.templates.default = "mytemplate"

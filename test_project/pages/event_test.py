from gpgui import dmc, idp, html, dash
from gpgui.cbtools import cbm, EventListener
from gpgui import cbtools as cbt

dash.register_page(__name__)
idp = idp.event_test
event = {
    "event": "keydown",
    "props": [
        "altKey",
        "shiftKey",
        "ctrlKey",
        "timeStamp",
        "type",
        "code",
        "key",
        "location",
        "repeat",
        "target.value",
        "target.id",
    ],
}
layout = dmc.Paper(
    EventListener(
        html.Div(
            [dmc.Button("Start", id=idp.button, n_clicks=0), dmc.Text(id=idp.text)]
        ),
        id=idp.listener,
        events=[event],
    )
)
print(cbt.events.keydown.event_dict())


@cbm.callback()
async def print_keydown(
    nevents=idp.listener.n_events.as_input(), event=idp.listener.event.as_state()
):
    print(event)


@cbm.callback(idp.text.children.as_output())
async def update_image(clicks: int = idp.button.n_clicks.as_input()):
    return clicks + 1

from gpgui import dmc, idp, html, dash
from gpgui.cbtools import cbm, EventListener, no_update
from gpgui import cbtools as cbt

dash.register_page(__name__)
idp = idp.event_test
layout = dmc.Paper(
    EventListener(
        [dmc.Button("Start", id=idp.button, n_clicks=0), dmc.Text(id=idp.text)],
        id=idp.listener,
        events=[cbt.events.keydown.event_dict()],
    )
)
print(cbt.events.keydown.event_dict())


@cbm.callback(idp.text.children.as_output())
async def print_keydown(
    n: int | None = idp.listener.n_events.as_input(),
    event: cbt.events.keydown = idp.listener.event.as_state(),
):
    target = event.target.id
    if event._valid:
        return event.toJSON()
    else:
        return no_update


@cbm.callback(idp.text.children.as_output())
async def update_image(clicks: int = idp.button.n_clicks.as_input()):
    return clicks + 1

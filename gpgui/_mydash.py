import asyncio
from async_dash import Dash as QuartDash
from gpgui import config
from dash_extensions.enrich import (
    Dash as DashEnrich,
    DashProxy,
    TriggerTransform,
    LogTransform,
    MultiplexerTransform,
    NoOutputTransform,
    CycleBreakerTransform,
    BlockingCallbackTransform,
    OperatorTransform,
)


# class MyDash(QuartDash):
#     ...


class MyDash(DashProxy, QuartDash):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            transforms=[
                # TriggerTransform(),
                # LogTransform(),
                MultiplexerTransform(),
                NoOutputTransform(),
                # CycleBreakerTransform(),
                # BlockingCallbackTransform(),
                # ServersideOutputTransform(**output_defaults),
                OperatorTransform(),
            ],
            **kwargs
        )
        self.loop = asyncio.new_event_loop()

    def myrun(self, debug=True):
        super().run(
            debug=debug,
            use_reloader=False,
            dev_tools_hot_reload=False,
            # dev_tools_prune_errors=False,
            port=config.PORT,
            loop=self.loop,  # used in cbm for background tasks
        )

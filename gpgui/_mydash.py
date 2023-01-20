from async_dash import Dash as QuartDash
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

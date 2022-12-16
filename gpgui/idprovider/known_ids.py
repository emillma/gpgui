from .str_with_children import StrWithChildren


class KnownIds:
    class _event_listener(StrWithChildren):
        event: StrWithChildren

    event_listener: _event_listener

    class _ws(StrWithChildren):
        message: StrWithChildren

    ws: _ws

    class _log(StrWithChildren):
        children: StrWithChildren

    log: _log

    class _input(StrWithChildren):
        value: StrWithChildren

    input: _input

    url: StrWithChildren

    class _hello(StrWithChildren):
        apekatt: StrWithChildren

    hello: _hello

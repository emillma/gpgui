from .str_with_children import StrWithChildren


class KnownIds:
    class _hello(StrWithChildren):
        apekatt: StrWithChildren

    hello: _hello

    class _event_listener(StrWithChildren):
        event: StrWithChildren

    event_listener: _event_listener

    class _log(StrWithChildren):
        children: StrWithChildren

    log: _log

    class _myws(StrWithChildren):
        class _ws(StrWithChildren):
            message: StrWithChildren

        ws: _ws

        url: StrWithChildren

        topics: StrWithChildren

    myws: _myws

    url: StrWithChildren

    class _input(StrWithChildren):
        value: StrWithChildren

    input: _input

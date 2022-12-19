from .str_with_children import StrWithChildren


class KnownIds:
    class _hello(StrWithChildren):
        apekatt: StrWithChildren

    hello: _hello

    class _myws(StrWithChildren):
        url: StrWithChildren

        class _ws(StrWithChildren):
            message: StrWithChildren

        ws: _ws

        topics: StrWithChildren

    myws: _myws

    url: StrWithChildren

    class _log(StrWithChildren):
        children: StrWithChildren

    log: _log

    class _input(StrWithChildren):
        value: StrWithChildren

    input: _input

    class _event_listener(StrWithChildren):
        event: StrWithChildren

    event_listener: _event_listener

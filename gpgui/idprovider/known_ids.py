from .str_with_children import StrWithChildren


class KnownIds:
    event_listener: StrWithChildren

    class _hello(StrWithChildren):
        apekatt: StrWithChildren

    hello: _hello

    log: StrWithChildren

    input: StrWithChildren

from .str_with_children import StrWithChildren


class KnownIds:
    log: StrWithChildren

    class _hello(StrWithChildren):
        apekatt: StrWithChildren

    hello: _hello

    input: StrWithChildren

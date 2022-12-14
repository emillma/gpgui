from .str_with_children import StrWithChildren


class KnownIds:
    input: StrWithChildren

    log: StrWithChildren

    class _hello(StrWithChildren):
        apekatt: StrWithChildren

    hello: _hello

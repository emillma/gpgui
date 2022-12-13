from .str_with_children import StrWithChildren


class KnownIds:
    log: StrWithChildren

    el: StrWithChildren

    class _hello(StrWithChildren):
        apekatt: StrWithChildren

    hello: _hello

    text_input: StrWithChildren

    text_area: StrWithChildren

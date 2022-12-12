from .str_with_children import StrWithChildren


class KnownIds:
    el: StrWithChildren

    class _hello(StrWithChildren):
        apekatt: StrWithChildren

    hello: _hello

    text_area: StrWithChildren

    text_input: StrWithChildren

    log: StrWithChildren

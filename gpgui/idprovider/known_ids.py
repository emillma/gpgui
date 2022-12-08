from .str_with_children import StrWithChildren


class KnownIds:
    class _a(StrWithChildren):
        class _b(StrWithChildren):
            c: StrWithChildren

        b: _b

    a: _a

    navbar_collapse: StrWithChildren

    class _b(StrWithChildren):
        c: StrWithChildren

    b: _b

    intermediate_value: StrWithChildren

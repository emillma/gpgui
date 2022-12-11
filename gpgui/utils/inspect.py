import re
from plotly.basedatatypes import BasePlotlyType
from functools import cache
from plotly.graph_objs.layout import Template


def get_props_all(obj: BasePlotlyType, max_depth=-1):
    def recursive(obj: BasePlotlyType, pre: str, depth: int):
        if depth == 0:
            yield pre[:-1]

        elif isinstance(obj, BasePlotlyType):
            for prop in [p for p in obj._valid_props if p not in ("template",)]:
                yield from recursive(getattr(obj, prop), pre + prop + ".", depth - 1)

        elif isinstance(obj, tuple):
            for i, item in enumerate(obj):
                yield from recursive(item, pre + f"[{i}].", depth - 1)
        else:
            yield pre[:-1]

    return sorted(list(recursive(obj, "", max_depth)))


def get_prop_recursive(obj, attr: str):
    pre, _, post = attr.rpartition(".")
    obj = obj if not pre else get_prop_recursive(obj, pre)
    if re.match(r"\[\d+\]", post):
        return obj[int(post[1:-1])]
    else:
        return getattr(obj, post)


def set_prop_recursive(obj, attr: str, value):
    pre, _, post = attr.rpartition(".")
    obj = obj if not pre else get_prop_recursive(obj, pre)
    if re.match(r"\[\d+\]", post):
        obj[int(post[1:-1])] = value
    else:
        setattr(obj, post, value)


def get_props(obj: BasePlotlyType, key: str = "*", regex=False):
    valid_props = list(get_props_all(obj))
    key = key if regex else key.replace("*", ".*").replace(".", r"\.")
    matchings = []
    for prop in valid_props:
        if re.search(key, prop):
            matchings.append(prop)
    return matchings


def set_props(obj: BasePlotlyType, key: str, value, regex=False):
    matching = get_props(obj, key, regex)
    assert matching, f"No matching props found for {key}"
    for prop in matching:
        set_prop_recursive(obj, prop, value)
    return matching

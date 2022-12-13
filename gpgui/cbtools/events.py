class target:
    """DOM element that triggered the event."""

    children: str
    id: str


class event:
    target: target
    timeStamp: int
    type: str

    @classmethod
    def event_dict(cls):
        props = []
        todo = list(cls.annotations().items())
        while todo:
            k, v = todo.pop()
            if annotations := getattr(v, "__annotations__", None):
                props.extend(f"{k}.{ann}" for ann in annotations)
            else:
                props.append(k)

        return dict(event=cls.__name__, props=props)

    @classmethod
    def annotations(cls):
        return dict(j for i in cls.__mro__[:-1] for j in i.__annotations__.items())

    def __init__(self, event_dict):
        ann = self.annotations()
        for k, v in event_dict.items():
            if k in ann:
                setattr(self, k, ann[k](v))

    @classmethod
    def get_union_factory(cls, others: tuple[type]):
        type_dict = {t.__name__: t for t in [cls] + list(others)}

        def factory(value):
            return type_dict[value["type"]](value)

        return factory

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"
        )


class with_modifiers:
    altKey: bool
    shiftKey: bool
    ctrlKey: bool


class click(event, with_modifiers):
    button: str
    buttons: str


class keydown(event, with_modifiers):
    target: target
    key: str
    # code: str

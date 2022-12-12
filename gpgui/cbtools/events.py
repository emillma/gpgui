class event:
    timeStamp: int
    type: str

    @classmethod
    def edict(cls):
        props = []
        todo = [j for i in cls.__mro__[:-1] for j in i.__annotations__.items()]
        while todo:
            k, v = todo.pop()
            if annotations := getattr(v, "__annotations__", None):
                props.extend(f"{k}.{ann}" for ann in annotations)
            else:
                props.append(k)

        return dict(event=cls.__name__, props=props)


class target:
    children: str


class click(event):
    target: target

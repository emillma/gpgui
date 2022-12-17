from pathlib import Path
from typing import Type
import jinja2
from black import format_str, FileMode
import re
import inspect

from .known_ids import KnownIds
from .str_with_children import StrWithChildren


class MetaIdProvider(type):
    """Metaclass for IdProvider."""

    def __getattr__(cls: Type["IdProvider"], item):  # type: ignore
        """Return the item."""

        if re.match("__.*__", item):
            raise AttributeError(item)
        return cls.register_return(item)


class IdProvider(KnownIds, metaclass=MetaIdProvider):
    """Class used to avoid littering code with id strings"""

    ids: set[str] = set()

    @classmethod
    def register_return(cls, item):
        """Return the item."""
        cls.ids.add(item)
        return StrWithChildren(item, cls)

    @classmethod
    def get_tree(cls):
        """Get a tree of the known IDs."""
        tree = {}
        for id_ in cls.ids:
            parts = id_.split("-")
            current: dict = tree.setdefault(parts[0], {})  # type: ignore
            for part in parts[1:]:
                current = current.setdefault("_children", {}).setdefault(part, {})

            current["_fullname"] = id_
            current["_name"] = parts[-1]

        return tree

    @classmethod
    def generate_code(cls):
        """Generate code for the known IDs."""
        this_dir = Path(__file__).parent
        fname = "known_ids"

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(this_dir),
            lstrip_blocks=True,
            trim_blocks=True,
            undefined=jinja2.StrictUndefined,
        )
        template = env.get_template(f"{fname}.j2")
        tree = cls.get_tree()
        content = template.render(id_tree=tree)
        content = format_str(content, mode=FileMode(preview=True))
        this_dir.joinpath(f"{fname}.py").write_text(content)

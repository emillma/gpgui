import re
import time
from pathlib import Path
from inspect import currentframe, getframeinfo
from collections import OrderedDict
import jinja2
from black import format_str, FileMode

from .str_with_children import StrWithChildren
from .known_ids import KnownIds


THIS_DIR = Path(__file__).parent
FILENAME = "known_ids"


class IdProvider(KnownIds):
    """Class used to avoid littering code with id strings"""

    locations = {}

    def register_return(self, item):
        """Return the item."""
        frame = getframeinfo(currentframe().f_back.f_back)
        loc = f"{frame.filename}:{frame.lineno}"
        self.locations.setdefault(item, OrderedDict())[loc] = time.time()
        return StrWithChildren(item, self.register_return, self.get_position)

    def get_position(self, item) -> set:
        return self.locations[item]

    def __getattr__(self, item):
        if re.match("__.*__", item):
            raise AttributeError(item)
        return self.register_return(item)

    def get_tree(self):
        """Get a tree of the known IDs."""
        tree = {}
        for id_ in self.locations:
            parts = id_.split(".")
            current = tree.setdefault(parts[0], {})
            for part in parts[1:]:
                current = current.setdefault("_children", {}).setdefault(part, {})

            current["_fullname"] = id_
            current["_name"] = parts[-1]

        return tree

    def generate_code(self):
        """Generate code for the known IDs."""
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(THIS_DIR),
            lstrip_blocks=True,
            trim_blocks=True,
            undefined=jinja2.StrictUndefined,
        )
        template = env.get_template(f"{FILENAME}.j2")
        tree = self.get_tree()
        content = template.render(id_tree=tree)
        content = format_str(content, mode=FileMode(preview=True))
        THIS_DIR.joinpath(f"{FILENAME}.py").write_text(content)

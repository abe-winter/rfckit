"htmtree -- thing for generating html from tree"
# etree is verbose and yattag requires with-blocks

from typing import List
from dataclasses import dataclass, field

INDENT = '  '

@dataclass
class Node:
    tag: str
    attrs: dict = field(default=None)

    @classmethod
    def mk(cls, tag, **kwargs):
        return cls(tag=tag, attrs=kwargs or None)

    def open_tag(self, prefix, self_closing=False):
        # todo: escape strings
        attrs = [(key if val is None else f'{key}="{val}"') for key, val in self.attrs.items()] if self.attrs else ()
        if self_closing:
            return f'{prefix}<{self.tag} {" ".join(attrs)} />'
        else:
            return f'{prefix}<{self.tag} {" ".join(attrs)}>'

    def close_tag(self, prefix):
        return f'{prefix}</{self.tag}>'

@dataclass
class Tree:
    node: Node
    children: list = field(default_factory=list)

    @classmethod
    def mk(cls, tag_or_node, children=None):
        node = Node.mk(tag=tag_or_node) if isinstance(tag_or_node, str) else tag_or_node
        return cls(node=node, children=children or [])

    def render(self, nindent=0, lines=None):
        lines = lines or []
        prefix = INDENT * nindent
        lines.append(self.node.open_tag(prefix))
        for child in self.children:
            if isinstance(child, str):
                lines.append(prefix + INDENT + child)
            elif isinstance(child, Node):
                lines.append(child.open_tag(prefix + INDENT, self_closing=True))
            else:
                child.render(nindent + 1, lines)
        lines.append(self.node.close_tag(prefix))
        return lines

    def append(self, x): self.children.append(x)
    def extend(self, arr): self.children.extend(arr)

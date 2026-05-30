from dataclasses import dataclass, field
from typing import Set

@dataclass
class GraphNode:
    name: str
    parents: Set[GraphNode] = field(default_factory=set)
    children: Set[GraphNode] = field(default_factory=set)

    def add_child(self, node: GraphNode):
        self.children.add(node)
        node.parents.add(self)
    
    def __repr__(self):
        return f"Node({self.name})"
    
    def __hash__(self):
        return hash(self.name)
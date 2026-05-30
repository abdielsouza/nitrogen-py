from .node import GraphNode
from .exceptions import CyclicDependencyError
from typing import Dict, List

class DependencyGraph:
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
    
    def node(self, name: str) -> GraphNode:
        if name not in self.nodes:
            self.nodes[name] = GraphNode(name)
            
        return self.nodes[name]
    
    def add_dependency(self, source: str, target: str):
        src = self.node(source)
        tgt = self.node(target)

        src.add_child(tgt)

        if self.has_cycle():
            raise CyclicDependencyError("a cycle between dependencies has been detected")

    def has_cycle(self) -> bool:
        visited = set()
        stack = set()

        def visit(node: GraphNode):
            if node in stack:
                return True

            if node in visited:
                return False
            
            visited.add(node)
            stack.add(node)

            for child in node.children:
                if visit(child):
                    return True
                
            stack.remove(node)
            return False

        return any(visit(n) for n in self.nodes.values())
    
    def execution_order(self) -> List[str]:
        visited = set()
        order = []

        def dfs(node: GraphNode):
            if node in visited:
                return
            
            visited.add(node)

            for child in node.children:
                dfs(child)
            
            order.append(node.name)
        
        for node in self.nodes.values():
            dfs(node)
        
        return list(reversed(order))
    
    def affected_by(self, name: str) -> List[str]:
        start = self.node(name)
        visited = set()
        result = []

        def walk(node: GraphNode):
            for child in node.children:
                if child not in visited:
                    visited.add(child)
                    result.append(child.name)
                    walk(child)
                else:
                    continue
        
        walk(start)

        return result
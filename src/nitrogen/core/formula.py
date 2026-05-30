from dataclasses import dataclass
from .expressions.base import Expression
from typing import Optional

@dataclass
class Formula:
    expr: Expression
    name: Optional[str] = None

    def contribute_to_sheet(self, name: str):
        self.name = name

    @property
    def dependencies(self):
        return self.expr.dependencies()
    
    def __repr__(self):
        return f"Formula({self.expr})"
from .base import Expression
from .arithmethic import *
from dataclasses import dataclass
from typing import Any

@dataclass
class BasicReference(Expression):
    column: Any

    @property
    def name(self):
        if getattr(self.column, "name", None) is None:
            raise ValueError("the column must have a name.")
        return self.column.name

    def dependencies(self):
        return {self.name}
    
    def __repr__(self):
        return f"Reference({self.name})"
    
    def __add__(self, other: BasicReference):
        return Add(self, other)
    
    def __sub__(self, other: BasicReference):
        return Subtract(self, other)
    
    def __mul__(self, other: BasicReference):
        return Multiply(self, other)
    
    def __truediv__(self, other: BasicReference):
        return Divide(self, other)
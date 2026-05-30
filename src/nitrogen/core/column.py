from dataclasses import dataclass
from typing import Any, Optional
from .expressions.references import BasicReference

@dataclass
class Column:
    dtype:      type
    name:       Optional[str] = None
    default:    Any = None
    nullable:   bool = False

    def contribute_to_sheet(self, name: str):
        self.name = name

    def ref(self):
        return BasicReference(self)
    
    def __add__(self, other: Column):
        return self.ref() + other.ref()
    
    def __sub__(self, other: Column):
        return self.ref() - other.ref()

    def __mul__(self, other: Column):
        return self.ref() * other.ref()
    
    def __truediv__(self, other: Column):
        return self.ref() / other.ref()
    
    def __repr__(self):
        return f"Column({self.name or ''})"
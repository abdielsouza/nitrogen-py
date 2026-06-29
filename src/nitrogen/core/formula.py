from dataclasses import dataclass
from typing import Optional
from .expressions.base import Expression
from .column import Column

@dataclass
class Formula:
    """
    The formula is a dynamic component which value can be auto-updated when
    the variables change.
    """
    expr: Expression
    name: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.expr, Column):
            self.expr = self.expr.ref()

        if not isinstance(self.expr, Expression):
            raise TypeError("formula expression must be an Expression instance.")

    def contribute_to_sheet(self, name: str):
        if self.name is not None and self.name != name:
            raise ValueError("formula name is already assigned and cannot be changed.")

        self.name = name

    def compile(self, compiler):
        return compiler.compile(self.expr)

    @property
    def dependencies(self):
        return self.expr.dependencies()

    def __repr__(self):
        if self.name is not None:
            return f"Formula({self.expr}, name={self.name})"
        return f"Formula({self.expr})"
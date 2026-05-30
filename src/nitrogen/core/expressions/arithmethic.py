from .base import Expression
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class BinaryOperator(Expression):
    left: Expression
    right: Expression
    symbol: Literal["+", "-", "*", "/"] = field(init=False)

    def dependencies(self):
        return self.left.dependencies() | self.right.dependencies()
    
    def compile(self, backend):
        raise NotImplementedError()
    
@dataclass
class Add(BinaryOperator):
    symbol = "+"

@dataclass
class Subtract(BinaryOperator):
    symbol = "-"

@dataclass
class Multiply(BinaryOperator):
    symbol = "*"

@dataclass
class Divide(BinaryOperator):
    symbol = "/"
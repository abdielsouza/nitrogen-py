from nitrogen.backends.base import Compiler
from nitrogen.core.expressions.references import BasicReference
from nitrogen.core.expressions.arithmethic import (
    Multiply,
    Add,
    Divide,
    Subtract
)

class ExcelCompiler(Compiler):
    def compile(self, expr) -> str:
        if isinstance(expr, BasicReference):
            return expr.name
        
        if isinstance(expr, Multiply):
            return f"{self.compile(expr.left)}*{self.compile(expr.right)}"
        
        if isinstance(expr, Divide):
            return f"{self.compile(expr.left)}/{self.compile(expr.right)}"

        if isinstance(expr, Add):
            return f"{self.compile(expr.left)}+{self.compile(expr.right)}"
        
        if isinstance(expr, Subtract):
            return f"{self.compile(expr.left)}-{self.compile(expr.right)}"
        
        raise TypeError("Expression type not supported!")
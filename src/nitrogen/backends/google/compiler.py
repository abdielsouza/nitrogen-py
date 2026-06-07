from nitrogen.backends.base import Compiler

class GoogleSheetsCompiler(Compiler):
    def compile(self, expr):
        return str(expr)
from nitrogen.engine.compiler import QueryCompiler
from nitrogen.engine.contexts import ExcelContext
from nitrogen.engine.query import (
    FetchQuery,
    InsertQuery,
    UpdateQuery,
    DeleteQuery
)
from openpyxl.worksheet.worksheet import Worksheet
import openpyxl as xl

class ExcelCompiler(QueryCompiler[ExcelContext]):
    def compile(self, query, context):
        if isinstance(query, FetchQuery):
            return self._compile_fetch(query, context.worksheet)
        else:
            raise ValueError("unsupported query type")
    
    def _compile_fetch(self, query: FetchQuery, worksheet: Worksheet):
        pass
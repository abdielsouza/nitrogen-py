from nitrogen.engine.source import DataSource
from nitrogen.engine.contexts import ExcelContext
from nitrogen.engine.compilers.excel import ExcelCompiler
from typing import cast, Any
import openpyxl as xl

class ExcelDataSource(DataSource):
    """Implementation of Excel data source."""

    def __init__(self, filepath: str):
        self._workbook = xl.load_workbook(filepath)
        self._context = ExcelContext()
        self._compiler = ExcelCompiler()

    def execute(self, query):
        self._context.worksheet = self._workbook[query.sheet]
        result = self._compiler.compile(query, self._context)
        result = cast(Any, result)
        
        return result
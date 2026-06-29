from nitrogen.engine.source import DataSource
from nitrogen.engine.contexts import ExcelContext
from nitrogen.engine.compilers.excel import ExcelCompiler
from typing import cast, Any
import openpyxl as xl
import os

class ExcelDataSource(DataSource):
    """Implementation of Excel data source."""

    def __init__(self, filepath: str):
        if os.path.exists(filepath):
            self._workbook = xl.load_workbook(filepath)
        else:
            self._workbook = xl.Workbook()

        self._context = ExcelContext()
        self._compiler = ExcelCompiler()
        self._filepath = filepath

    def execute(self, query):
        self._context.worksheet = self._workbook[query.sheet]
        result = self._compiler.compile(query, self._context)
        result = cast(Any, result)
        
        return result
    
    @property
    def context(self):
        return self._context

    @property
    def workbook(self):
        return self._workbook
    
    @property
    def filepath(self):
        return self._filepath
from typing import Any

from nitrogen.engine.query import (
    cast_query_to_fetch,
    cast_query_to_insert,
    cast_query_to_update,
    cast_query_to_delete,
)
from nitrogen.engine.source import DataSource
from nitrogen.engine.contexts import ExcelContext
import openpyxl as xl

class ExcelDataSource(DataSource):
    """Implementation of Excel data source."""

    def __init__(self, filepath: str):
        self._workbook = xl.load_workbook(filepath)
        self._context = ExcelContext()

    def fetch(self, query):
        query = cast_query_to_fetch(query)
        self._context.worksheet = self._workbook[query.sheet]
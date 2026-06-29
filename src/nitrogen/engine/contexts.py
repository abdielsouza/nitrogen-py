from dataclasses import dataclass
from typing import Any
import sqlalchemy as sql
from openpyxl.worksheet.worksheet import Worksheet

@dataclass
class CompilationContext:
    """
    Every compiler needs to receive a context to work into.
    When a query is compiled, the result is normally written
    in some external source, making state changes that are
    unreachable without a context abstraction.
    """

    # it's just a test :)
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        if not cls.__doc__:
            cls.__doc__ = cls.__base__.__doc__

@dataclass(init=False)
class SQLAlchemyContext(CompilationContext):
    """Implementation of CompilationContext for any sources compatible with SQLAlchemy."""

    table: sql.Table

@dataclass(init=False)
class ExcelContext(CompilationContext):
    """Implementation of CompilationContext for Excel."""

    worksheet: Worksheet

@dataclass(init=False)
class GoogleSheetsContext(CompilationContext):
    """Implementation of CompilationContext for Google Sheets."""

    spreadsheet_id: str
    worksheet: Any
    spreadsheet: Any
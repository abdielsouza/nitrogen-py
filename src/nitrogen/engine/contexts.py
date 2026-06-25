from dataclasses import dataclass
import sqlalchemy as sql
from openpyxl.worksheet.worksheet import Worksheet

@dataclass
class CompilationContext:
    pass

@dataclass(init=False)
class SQLAlchemyContext(CompilationContext):
    table: sql.Table

@dataclass(init=False)
class ExcelContext(CompilationContext):
    worksheet: Worksheet

@dataclass(init=False)
class GoogleSheetsContext(CompilationContext):
    spreadsheet_id: str
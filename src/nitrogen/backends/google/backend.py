from nitrogen.backends.base import Backend
from nitrogen.backends.google.compiler import GoogleSheetsCompiler
import gspread

class GoogleSheetsBackend(Backend):
    def __init__(self, **kwargs):
        creds_path: str | None = kwargs.get("credentials")
        spreadsheet_name: str | None = kwargs.get("spreadsheet")

        if creds_path is not None and spreadsheet_name is not None:
            self.__gc = gspread.service_account(creds_path)
            self.__spreadsheet = self.__gc.open(spreadsheet_name)
        
        self.__compiler = GoogleSheetsCompiler()
    
    def create_sheet(self, sheet):
        self.__spreadsheet.add_worksheet(
            title=sheet.__name__,
            rows=1000,
            cols=23,
        )

    def write_column(self, sheet, column) -> None:
        ws = self.__spreadsheet.worksheet(sheet.__name__)

        col_idx = 1

        while ws.cell(row=1, col=col_idx).value is not None:
            col_idx += 1

        if column.name is not None:
            ws.update_cell(row=1, col=col_idx, value=column.name)
        else:
            raise ValueError("column name cannot be null.")

        rows = getattr(sheet, "__rows__", [])

        for row_idx, row in enumerate(rows):
            value = row.get(column.name)
            ws.update_cell(row=2 + row_idx, col=col_idx, value=value)
    
    def write_formula(self, sheet, formula) -> None:
        compiled = self.__compiler.compile(formula.expr)

        ws = self.__spreadsheet.worksheet(sheet.__name__)

        col_idx = 1
        while ws.cell(row=1, col=col_idx).value is not None:
            col_idx += 1

        if formula.name is not None:
            ws.update_cell(row=1, col=col_idx, value=formula.name)
        else:
            raise ValueError("formula name cannot be null.")

        rows = getattr(sheet, "__rows__", [])

        for row_idx, _ in enumerate(rows):
            row_number = 2 + row_idx
            formula_value = compiled
            if isinstance(compiled, str) and "{row}" in compiled:
                formula_value = compiled.format(row=row_number)
            ws.update_cell(row=row_number, col=col_idx, value=formula_value)
    
    def save(self, path = None):
        pass
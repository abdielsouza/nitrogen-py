from nitrogen.backends.base import Backend
from nitrogen.backends.excel.compiler import ExcelCompiler
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import re
from typing import Type
from nitrogen.core import Sheet, Column, Formula


class ExcelBackend(Backend):
    def __init__(self, workbook: Workbook):
        self.__workbook = workbook
        self.__compiler = ExcelCompiler()

    def create_sheet(self, sheet: Type[Sheet]) -> None:
        # create the worksheet for the Sheet subclass
        self.__workbook.create_sheet(title=sheet.__name__)

    def write_column(self, sheet: Type[Sheet], column: Column) -> None:
        ws = self.__workbook[sheet.__name__]

        # find next empty column in header (row 1)
        col_idx = 1
        while ws.cell(row=1, column=col_idx).value is not None:
            col_idx += 1

        # write header
        ws.cell(row=1, column=col_idx, value=column.name)

        # write existing data rows for this column (if any)
        rows = getattr(sheet, "__rows__", [])
        for row_idx, row in enumerate(rows):
            value = row.get(column.name)
            ws.cell(row=2 + row_idx, column=col_idx, value=value)

    def write_formula(self, sheet: Type[Sheet], formula: Formula) -> None:
        ws = self.__workbook[sheet.__name__]

        # compiled formula uses column names (e.g. "col_a+col_b")
        compiled = self.__compiler.compile(formula.expr)

        # build header map: name -> column index
        header_map: dict[str, int] = {}

        for idx, cell in enumerate(ws[1], start=1):
            if cell.value is not None:
                header_map[str(cell.value)] = idx

        # ensure formula column exists in header
        if formula.name is not None:
            target_col = header_map.get(formula.name)

            if target_col is None:
                # find next empty column
                target_col = 1

                while ws.cell(row=1, column=target_col).value is not None:
                    target_col += 1

                ws.cell(row=1, column=target_col, value=formula.name)
                header_map[formula.name] = target_col

            # prepare list of names to replace, sort by length desc to avoid partial matches
            names = [n for n in header_map.keys() if n != formula.name]
            names.sort(key=len, reverse=True)

            rows = getattr(sheet, "__rows__", [])

            for row_idx, _ in enumerate(rows):
                row_number = 2 + row_idx
                fstr = compiled

                for name in names:
                    col_idx = header_map.get(name)

                    if col_idx is None:
                        continue

                    col_letter = get_column_letter(col_idx)
                    
                    # replace whole-word occurrences of the column name with the cell reference
                    fstr = re.sub(r"\b" + re.escape(name) + r"\b", f"{col_letter}{row_number}", fstr)

                # write formula into target cell (must start with '=')
                ws.cell(row=row_number, column=target_col, value=f"={fstr}")
            else:
                pass

    def save(self, path: str | None = None) -> None:
        if path:
            self.__workbook.save(path)
        else:
            raise ValueError("missing path for excel file saving")
from nitrogen.engine.sources.excel import ExcelDataSource
from nitrogen.engine.sources.google import GoogleSheetsSource
from nitrogen.core import Workbook
from typing import cast

class WorkbookEngine:
    """Builtin engine to process changes for spreadsheet sources."""

    def __init__(self, source: ExcelDataSource | GoogleSheetsSource):
        self._source = source

    def save(self, workbook: Workbook):
        """
        Save changes from virtual workbook to the spreadsheet sources.
        
        :param workbook: The workbook to be saved.
        :type workbook: Workbook
        """

        if isinstance(self._source, ExcelDataSource):
            self._save_excel(workbook)
        elif isinstance(self._source, GoogleSheetsSource):
            self._save_google(workbook)

    def _save_excel(self, workbook: Workbook):
        ds = cast(ExcelDataSource, self._source)

        for sheet in workbook:
            try:
                ws = ds.workbook[sheet.default_name()]
            except KeyError:
                ds.workbook.create_sheet(sheet.default_name())
                ws = ds.workbook[sheet.default_name()]

            ds.context.worksheet = ws

            # Clear existing rows
            if ws.max_row > 0:
                ws.delete_rows(1, ws.max_row)

            headers = list(sheet.columns().keys())

            if headers:
                ws.append(headers)

            for record in sheet.__rows__:
                ws.append([record.get(header) for header in headers])
        
        ds.workbook.save(ds.filepath)

    def _save_google(self, workbook: Workbook):
        ds = cast(GoogleSheetsSource, self._source)

        for sheet in workbook:
            worksheet = ds.spreadsheet.worksheet(sheet.default_name())
            ds.context.worksheet = worksheet
            worksheet.clear()

            headers = list(sheet.columns().keys())
            values = []

            if headers:
                values.append(headers)

                for record in sheet.__rows__:
                    values.append([record.get(header) for header in headers])

            if values:
                worksheet.update(values)
from nitrogen.engine.source import DataSource
from nitrogen.engine.contexts import GoogleSheetsContext
from nitrogen.engine.compilers.google import GoogleSheetsCompiler
from nitrogen.engine.query import Query
from typing import cast, Any
import gspread


class GoogleSheetsSource(DataSource):
    """Implementation of Google Sheets data source."""

    def __init__(self, spreadsheet_id: str, credentials_file: str | None = None):
        self._spreadsheet_id = spreadsheet_id
        self._credentials_file = credentials_file

        if credentials_file:
            self._client = gspread.service_account(filename=credentials_file)
        else:
            self._client = gspread.service_account()

        self._context = GoogleSheetsContext()
        self._compiler = GoogleSheetsCompiler()

    def execute(self, query: Query) -> Any:
        self._context.spreadsheet_id = self._spreadsheet_id
        self._context.spreadsheet = self._client.open_by_key(self._spreadsheet_id)
        self._context.worksheet = self._context.spreadsheet.worksheet(query.sheet)

        result = self._compiler.compile(query, self._context)
        result = cast(Any, result)

        return result

    @property
    def context(self):
        return self._context

    @property
    def spreadsheet(self):
        return self._client.open_by_key(self._spreadsheet_id)

    @property
    def client(self):
        return self._client
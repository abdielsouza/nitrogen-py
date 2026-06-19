from nitrogen.backends.base import Backend
from nitrogen.backends.google.compiler import GoogleSheetsCompiler
from typing import Optional, Type, TYPE_CHECKING
import gspread
import re
import logging

if TYPE_CHECKING:
    from nitrogen.core import Sheet, Column, Formula
else:
    Sheet = Column = Formula = object

logger = logging.getLogger(__name__)

class GoogleSheetsBackend(Backend):
    """The backend for Google Sheets"""

    def __init__(self, **kwargs):
        """
        :param str credentials: The path to the 'credentials.json' for integration with Google Sheets.
        :param str spreadsheet: The spreadsheet file name.
        """
        creds_path: str | None = kwargs.get("credentials")
        spreadsheet_name: str | None = kwargs.get("spreadsheet")

        if not creds_path or not spreadsheet_name:
            raise ValueError(
                "You must provide both 'credentials' (path to service account JSON) "
                "and 'spreadsheet' (spreadsheet name) for the Google Sheets backend."
            )
        
        try:
            self.__gc = gspread.service_account(creds_path)
            self.__spreadsheet = self.__gc.open(spreadsheet_name)
        except FileNotFoundError as e:
            raise ValueError(f"Credentials file not found: {creds_path}") from e
        except gspread.exceptions.SpreadsheetNotFound as e:
            raise ValueError(f"Spreadsheet not found: {spreadsheet_name}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Google Sheets backend: {e}") from e
        
        self.__compiler = GoogleSheetsCompiler()
        self.__header_cache: dict[str, dict[str, int]] = {}  # sheet_name -> {column_name: col_idx}
    
    def create_sheet(self, sheet: Type[Sheet]) -> None:
        """Create a worksheet for the given sheet class."""
        sheet_name = sheet.default_name()

        try:
            self.__spreadsheet.add_worksheet(
                title=sheet_name,
                rows=1000,
                cols=23,
            )
            # Clear cache for this sheet
            self.__header_cache.pop(sheet_name, None)
            logger.info(f"Created worksheet: {sheet_name}")
        except gspread.exceptions.APIError as e:
            if "already exists" in str(e):
                logger.warning(f"Worksheet '{sheet_name}' already exists")
            else:
                raise RuntimeError(f"Failed to create worksheet '{sheet_name}': {e}") from e

    def write_column(self, sheet: Type[Sheet], column) -> None:
        """Write a column (header + data) to the worksheet."""
        if not column.name:
            raise ValueError("column.name cannot be null or empty")
        
        sheet_name = sheet.default_name()

        try:
            ws = self.__spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            raise RuntimeError(f"Worksheet '{sheet_name}' not found. Create it first with create_sheet().")
        
        # Get header map (fetch once, cache it)
        header_map = self._get_header_map(sheet_name, ws)
        
        # Find next empty column
        col_idx = max(header_map.values()) + 1 if header_map else 1
        
        rows = getattr(sheet, "__rows__", [])
        
        # Prepare batch updates
        updates = []
        updates.append({
            "range": f"{self._col_letter(col_idx)}1",
            "values": [[column.name]]
        })
        
        # Add data rows
        for row_idx, row in enumerate(rows):
            value = row.get(column.name)
            updates.append({
                "range": f"{self._col_letter(col_idx)}{2 + row_idx}",
                "values": [[value]]
            })
        
        # Batch update
        try:
            ws.batch_update(updates)
            # Update cache
            header_map[column.name] = col_idx
            self.__header_cache[sheet_name] = header_map
            logger.info(f"Wrote column '{column.name}' to worksheet '{sheet_name}'")
        except gspread.exceptions.APIError as e:
            raise RuntimeError(f"Failed to write column '{column.name}': {e}") from e
    
    def write_formula(self, sheet: Type[Sheet], formula) -> None:
        """Write a formula column to the worksheet."""
        if not formula.name:
            raise ValueError("formula.name cannot be null or empty")
        
        sheet_name = sheet.default_name()
        
        try:
            ws = self.__spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            raise RuntimeError(f"Worksheet '{sheet_name}' not found. Create it first with create_sheet().")
        
        compiled = self.__compiler.compile(formula.expr)
        if not isinstance(compiled, str):
            raise ValueError(f"Compiled formula must be a string, got {type(compiled)}")
        
        # Get header map and build column references
        header_map = self._get_header_map(sheet_name, ws)
        
        # Find or create target column for formula
        target_col = header_map.get(formula.name)
        if target_col is None:
            target_col = max(header_map.values()) + 1 if header_map else 1
            header_map[formula.name] = target_col
        
        rows = getattr(sheet, "__rows__", [])
        if not rows:
            logger.warning(f"No data rows found for formula '{formula.name}'")
            return
        
        # Sort column names by length (longest first) to avoid partial replacements
        column_names = [name for name in header_map.keys() if name != formula.name]
        column_names.sort(key=len, reverse=True)
        
        # Prepare batch updates
        updates = []
        updates.append({
            "range": f"{self._col_letter(target_col)}1",
            "values": [[formula.name]]
        })
        
        # Generate formula for each row
        for row_idx, _ in enumerate(rows):
            row_number = 2 + row_idx
            formula_text = compiled
            
            # Replace column references with cell references
            for col_name in column_names:
                col_idx = header_map.get(col_name)
                if col_idx is None:
                    continue
                
                col_letter = self._col_letter(col_idx)
                # Use word boundaries to avoid partial matches
                formula_text = re.sub(
                    r"(?<![A-Za-z0-9_])" + re.escape(col_name) + r"(?![A-Za-z0-9_])",
                    f"{col_letter}{row_number}",
                    formula_text,
                )
            
            updates.append({
                "range": f"{self._col_letter(target_col)}{row_number}",
                "values": [[formula_text]]
            })
        
        # Batch update
        try:
            ws.batch_update(updates)
            self.__header_cache[sheet_name] = header_map
            logger.info(f"Wrote formula '{formula.name}' to worksheet '{sheet_name}'")
        except gspread.exceptions.APIError as e:
            raise RuntimeError(f"Failed to write formula '{formula.name}': {e}") from e
    
    def save(self, path: Optional[str] = None) -> None:
        """Save the spreadsheet (no-op for Google Sheets as it auto-saves)."""
        logger.info("Google Sheets auto-saves changes")
    
    def _get_header_map(self, sheet_name: str, ws) -> dict[str, int]:
        """Get or fetch the header map for a worksheet (cached)."""
        if sheet_name in self.__header_cache:
            return self.__header_cache[sheet_name]
        
        header_map = {}
        try:
            headers = ws.row_values(1)
            for idx, header in enumerate(headers, start=1):
                if header:  # Skip empty cells
                    header_map[header] = idx
        except gspread.exceptions.APIError as e:
            logger.warning(f"Failed to fetch headers for '{sheet_name}': {e}")
        
        self.__header_cache[sheet_name] = header_map
        return header_map
    
    @staticmethod
    def _col_letter(col_idx: int) -> str:
        """Convert column index (1-based) to letter (A, B, C, ..., Z, AA, etc)."""
        result = ""
        while col_idx > 0:
            col_idx -= 1
            result = chr(65 + (col_idx % 26)) + result
            col_idx //= 26
        return result
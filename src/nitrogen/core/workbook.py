from dataclasses import dataclass, field
from typing import Dict, Optional, Type
from .sheet import Sheet
from nitrogen.backends.base import Backend

@dataclass
class Workbook:
    """
    The workbook normally represents a kind of workspace where the sheets
    are contained in.
    """

    sheets: Dict[str, Type[Sheet]] = field(default_factory=dict)

    def add(self, sheet: Type[Sheet]):
        """add a sheet to the workbook."""

        self.sheets[sheet.__name__] = sheet
    
    def sync(self, backend: Backend, path: Optional[str] = None):
        """synchronize the updates in the workbook to the remote location or file path."""
        
        for sheet in self.sheets.values():
            backend.rescue_sheet(sheet)

            if not backend.data_rescue_lock:
                for col in sheet.columns().values():
                    backend.write_column(sheet, col)
                
                for formula in sheet.formulas().values():
                    backend.write_formula(sheet, formula)
        
        try:
            backend.save(path)
        finally:
            backend.disable_data_rescue_lock()
from dataclasses import dataclass, field
from typing import Dict, Optional
from .sheet import Sheet
from nitrogen.backends.base import Backend

@dataclass
class Workbook:
    sheets: Dict[str, Sheet] = field(default_factory=dict)

    def add(self, sheet: Sheet):
        self.sheets[sheet.__name__] = sheet
    
    def sync(self, backend: Backend, path: Optional[str] = None):
        for sheet in self.sheets.values():
            backend.create_sheet(sheet)

            for col in sheet.columns().values():
                backend.write_column(sheet, col)
            
            for formula in sheet.formulas().values():
                backend.write_formula(sheet, formula)
            
        backend.save(path)
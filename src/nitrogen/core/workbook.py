from dataclasses import dataclass, field
from typing import Dict, Type, Optional
from .sheet import Sheet

@dataclass
class Workbook:
    """
    The workbook normally represents a kind of workspace where the sheets
    are contained in.
    """

    sheets: Dict[str, Type[Sheet]] = field(default_factory=dict)

    def add_sheet(self, sheet: Type[Sheet]) -> None:
        self.sheets[sheet.default_name()] = sheet
    
    def pop_sheet(self, sheet_name: str) -> Optional[Type[Sheet]]:
        return self.sheets.pop(sheet_name, None)

    def get_sheet(self, sheet_name: str) -> Optional[Type[Sheet]]:
        return self.sheets.get(sheet_name)

    def __iter__(self):
        return iter(self.sheets.values())
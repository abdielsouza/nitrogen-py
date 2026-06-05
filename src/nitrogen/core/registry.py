from dataclasses import dataclass, field
from typing import Dict
from .sheet import Sheet

@dataclass
class Registry:
    """A registry of sheets. Each sheet is identified by its own name."""
    sheets: Dict[str, Sheet] = field(default_factory=dict)

    @classmethod
    def register(cls, sheet: Sheet):
        cls.sheets[sheet.__name__] = sheet
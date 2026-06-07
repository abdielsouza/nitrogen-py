from typing import Type, Dict
from .sheet import Sheet

class Record:
    def __init__(self, sheet: Type[Sheet], data: Dict):
        self._sheet = sheet
        self._data = data
    
    def __getattr__(self, item: str):
        if item in self._data:
            return self._data[item]
        
        rel = self._sheet._relationships.get(item)

        if rel:
            return rel.resolve(self._data)

        raise AttributeError
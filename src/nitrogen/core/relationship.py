from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sheet import Sheet
    from typing import Type

class Relationship:
    def __init__(self, target: Type[Sheet], local_key: str, remote_key: str = "id"):
        self._name = None
        self._target = target
        self._local_key = local_key
        self._remote_key = remote_key
    
    def contribute_to_sheet(self, name: str):
        self._name = name

    def resolve(self, row: dict):
        value = row.get(self._local_key)

        return self._target.find(**{self._remote_key: value})

    def __repr__(self):
        return f"Relationship({self._target.__name__})"
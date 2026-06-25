from abc import ABC, abstractmethod
from typing import Any

from .query import Query

class DataSource(ABC):
    @abstractmethod
    def fetch(self, query: Query) -> Any:
        pass

    @abstractmethod
    def insert(self, query: Query) -> Any:
        pass

    @abstractmethod
    def update(self, query: Query) -> Any:
        pass

    @abstractmethod
    def delete(self, query: Query) -> Any:
        pass
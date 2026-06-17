from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TextIO, Optional, Any
from result import Result
from dataclasses import dataclass, field

class DatabaseConnector(ABC):
    """it represents a database connection interface."""

    def __init__(self):
        self._connection = None
    
    @abstractmethod
    def connect(self) -> Result[None, str]:
        """connect to the database"""
        pass

    @abstractmethod
    def close(self) -> Result[None, str]:
        """close the connection with the database"""
        pass

    @abstractmethod
    def execute(self, query: str | TextIO, *args, **kwargs) -> Result[object, str]:
        """execute a query in the database"""
        pass

class DataSource(ABC):
    """This class normally represents a data source or a database itself."""

    @dataclass
    class __FetchParams:
        fields: list[str]
        where: Optional[dict] = field(default=None)
        group_by: Optional[str] = field(default=None)
        order_by: Optional[str] = field(default=None)

    @dataclass
    class __InsertParams:
        registry: dict
    
    type __UpsertParams = __InsertParams

    @dataclass
    class __UpdateParams:
        registry: dict
        where: Optional[dict] = field(default=None)
    
    @dataclass
    class __DeleteParams:
        where: Optional[dict] = field(default=None)

    @abstractmethod
    def fetch(self, sheet: str, params: __FetchParams) -> Result[Any, Any]:
        pass

    @abstractmethod
    def insert(self, sheet: str, params: __InsertParams) -> Result[Any, Any]:
        pass

    @abstractmethod
    def upsert(self, sheet: str, params: __UpsertParams) -> Result[Any, Any]:
        pass

    @abstractmethod
    def update(self, sheet: str, params: __UpdateParams) -> Result[Any, Any]:
        pass

    @abstractmethod
    def delete(self, sheet: str, params: __DeleteParams) -> Result[Any, Any]:
        pass
from typing import Optional, Any, cast
from dataclasses import dataclass, field
from enum import Enum

class QueryType(Enum):
    FETCH   = 0
    INSERT  = 1
    UPDATE  = 2
    DELETE  = 3

class Operator(Enum):
    EQ          = "="
    GT          = ">"
    LT          = "<"
    GTE         = ">="
    LTE         = "<="
    IN          = "IN"
    CONTAINS    = "CONTAINS"

class Query:
    pass

@dataclass
class Filter:
    field: str
    operator: Operator
    value: Any

@dataclass
class FetchQuery(Query):
    sheet: str
    fields: list[str] = field(default_factory=list)
    filters: list[Filter] = field(default_factory=list)
    group_by: Optional[str] = field(default=None)
    order_by: Optional[str] = field(default=None)

@dataclass
class InsertQuery(Query):
    sheet: str
    registry: dict[str, Any]

@dataclass
class UpdateQuery(Query):
    sheet: str
    registry: dict[str, Any]
    filters: list[Filter] = field(default_factory=list)

@dataclass
class DeleteQuery(Query):
    sheet: str
    filters: list[Filter] = field(default_factory=list)

class QueryBuilder:
    """builder pattern for custom queries"""

    def __init__(self):
        self._query_type: Optional[QueryType] = None
        self._sheet: Optional[str] = None
        self._fields: list[str] = []
        self._registry: dict[str, Any] = {}        
        self._filters: list[Filter] = []
        self._group_by: Optional[str] = None
        self._order_by: Optional[str] = None

    @classmethod
    def fetch(cls, sheet: str):
        builder = cls()
        builder._query_type = QueryType.FETCH
        builder._sheet = sheet

        return builder
    
    @classmethod
    def insert(cls, sheet: str):
        builder = cls()
        builder._query_type = QueryType.INSERT
        builder._sheet = sheet

        return builder
    
    @classmethod
    def update(cls, sheet: str):
        builder = cls()
        builder._query_type = QueryType.UPDATE
        builder._sheet = sheet

        return builder
    
    def select(self, *fields: str):
        self._fields.extend(fields)
        return self
    
    def where(self, field: str, operator: Operator, value: Any):
        self._filters.append(Filter(field, operator, value))
        return self
    
    def order_by(self, field: str):
        self._order_by = field
        return self
    
    def group_by(self, field: str):
        self._group_by = field
        return self

    def values(self, **kwargs):
        self._registry = kwargs
        return self
    
    def build(self):
        match self._query_type:
            case QueryType.FETCH:
                return FetchQuery(
                    sheet=cast(str, self._sheet),
                    fields=self._fields,
                    filters=self._filters,
                    group_by=self._group_by,
                    order_by=self._order_by,
                )

            case QueryType.INSERT:
                return InsertQuery(
                    sheet=cast(str, self._sheet),
                    registry=self._registry,
                )

            case QueryType.UPDATE:
                return UpdateQuery(
                    sheet=cast(str, self._sheet),
                    registry=self._registry,
                    filters=self._filters,
                )
            
            case _:
                raise NotImplementedError("invalid query type")

    # @classmethod
    # def build_fetch(
    #     cls,
    #     sheet: str,
    #     fields: list[str] = [],
    #     filters: FilterType = {},
    #     group_by: Optional[str] = None,
    #     order_by: Optional[str] = None
    # ):
    #     return FetchQuery(sheet, fields, filters, group_by, order_by)
    
    # @classmethod
    # def build_insert(
    #     cls,
    #     sheet: str,
    #     registry: dict
    # ):
    #     return InsertQuery(sheet, registry)
    
    # @classmethod
    # def build_update(
    #     cls,
    #     sheet: str,
    #     registry: dict,
    #     filters: FilterType
    # ):
    #     return UpdateQuery(sheet, registry, filters)
    
    # @classmethod
    # def build_delete(
    #     cls,
    #     sheet: str,
    #     filters: FilterType
    # ):
    #     return DeleteQuery(sheet, filters)

def _is_fetch_query(query: Query):
    return isinstance(query, FetchQuery)

def _is_insert_query(query: Query):
    return isinstance(query, InsertQuery)

def _is_update_query(query: Query):
    return isinstance(query, UpdateQuery)

def _is_delete_query(query: Query):
    return isinstance(query, DeleteQuery)

def cast_query_to_fetch(query: Query):
    assert _is_fetch_query(query)
    return cast(FetchQuery, query)

def cast_query_to_insert(query: Query):
    assert _is_insert_query(query)
    return cast(InsertQuery, query)

def cast_query_to_update(query: Query):
    assert _is_update_query(query)
    return cast(UpdateQuery, query)

def cast_query_to_delete(query: Query):
    assert _is_delete_query(query)
    return cast(DeleteQuery, query)
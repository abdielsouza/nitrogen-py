from typing import Any, ClassVar, Dict, Tuple, Optional
from .column import Column
from .formula import Formula
from .relationship import Relationship
from .record import Record
from .graph.dependency import DependencyGraph

class SheetMeta(type):
    """
    metaclass for Sheet class.
    It's used to add a kind of 'metaprogramming' to describe spreadsheets as
    Python classes.
    """

    def __new__(cls, name: str, bases: Tuple, attrs: Dict, **kwargs):
        columns = {}
        formulas = {}
        relationships = {}
        graph = DependencyGraph()

        for key, value in attrs.items():
            if isinstance(value, Column):
                value.contribute_to_sheet(key)
                columns[key] = value
            
            elif isinstance(value, Formula):
                value.contribute_to_sheet(key)
                formulas[key] = value

            elif isinstance(value, Relationship):
                value.contribute_to_sheet(key)
                relationships[key] = value
        
        for formula_name, formula in formulas.items():
            for dep in formula.dependencies:
                graph.add_dependency(dep, formula_name)
        
        # Each Sheet subclass needs its own independent row storage.
        attrs["__rows__"] = []
        attrs["_columns"] = columns
        attrs["_formulas"] = formulas
        attrs["_relationships"] = relationships
        attrs["_graph"] = graph
        attrs["__sheet_name__"] = kwargs.get("alt_name", name)

        return super().__new__(cls, name, bases, attrs)

class Sheet(metaclass=SheetMeta):
    """It represents a single sheet or tab inside a workspace."""

    __rows__: ClassVar[list[dict]] = []
    __sheet_name__: Optional[str] = None #: the custom sheet name

    _columns:   ClassVar[Dict[str, Any]]    = {}
    _formulas:  ClassVar[Dict[str, Any]]    = {}
    _graph:     ClassVar[DependencyGraph]   = DependencyGraph()
    
    _relationships:  ClassVar[Dict[str, Any]]    = {}

    @classmethod
    def default_name(cls):
        if not cls.__sheet_name__:
            return cls.__name__
        
        return cls.__sheet_name__

    @classmethod
    def schema(cls):
        """it returns a single schema with information about columns and formulas in the sheet."""
        return {"columns": cls._columns, "formulas": cls._formulas}

    @classmethod
    def sheet_name(cls) -> str:
        """Returns the configured sheet name or the class name by default."""
        return getattr(cls, "__sheet_name__", cls.__name__)
    
    @classmethod
    def insert(cls, **kwargs):
        """it inserts a record as a row in the sheet."""
        cls.__rows__.append(kwargs)

    @classmethod
    def graph(cls) -> DependencyGraph:
        """it returns the dependency graph. It can be util when analyzing formulas."""
        return cls._graph

    @classmethod
    def columns(cls) -> Dict[str, Any]:
        """It returns the sheet columns."""
        return cls._columns
    
    @classmethod
    def formulas(cls) -> Dict[str, Any]:
        """it returns the sheet formulas."""
        return cls._formulas
    
    @classmethod
    def find(cls, **filters) -> Optional[Record]:
        for row in cls.__rows__:
            matching = True

            for key, value in filters.items():
                if row.get(key) != value:
                    matching = False
                    break
            
            if matching:
                return Record(cls, row)
        
        return None
    
    @classmethod
    def all(cls):
        return [Record(cls, row) for row in cls.__rows__]

    @classmethod
    def filter(cls, **filters) -> list[Record]:
        results = []

        for row in cls.__rows__:
            matching = True

            for key, value in filters.items():
                if row.get(key) != value:
                    matching = False
                    break

            if matching:
                results.append(Record(cls, row))
        
        return results
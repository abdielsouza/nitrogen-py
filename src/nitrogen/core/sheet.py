from typing import Any, ClassVar, Dict, Tuple, Optional
from .column import Column
from .formula import Formula
from .relationship import Relationship
from .graph.dependency import DependencyGraph

class SheetMeta(type):
    """
    metaclass for Sheet class.
    It's used to add a kind of 'metaprogramming' to describe spreadsheets as
    Python classes.
    """

    def __new__(cls, name: str, bases: Tuple, attrs: Dict):
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

        return super().__new__(cls, name, bases, attrs)

class Sheet(metaclass=SheetMeta):
    """It represents a single sheet or tab inside a workspace."""

    __rows__: ClassVar[list[dict]] = []

    _columns:   ClassVar[Dict[str, Any]]    = {}
    _formulas:  ClassVar[Dict[str, Any]]    = {}
    _graph:     ClassVar[DependencyGraph]   = DependencyGraph()
    
    _relationships:  ClassVar[Dict[str, Any]]    = {}

    @classmethod
    def schema(cls):
        """it returns a single schema with information about columns and formulas in the sheet."""
        return {"columns": cls._columns, "formulas": cls._formulas}
    
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
    def find(cls, **filters) -> Optional[Dict]:
        for row in cls.__rows__:
            matching = True

            for key, value in filters.items():
                if row.get(key) != value:
                    matching = False
                    break
            
            if matching:
                return row
        
        return None
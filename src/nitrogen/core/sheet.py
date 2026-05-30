from typing import Any, ClassVar, Dict, Tuple, Final
from .column import Column
from .formula import Formula
from .graph.dependency import DependencyGraph

class SheetMeta(type):
    def __new__(cls, name: str, bases: Tuple, attrs: Dict):
        columns = {}
        formulas = {}
        graph = DependencyGraph()

        for key, value in attrs.items():
            if isinstance(value, Column):
                value.contribute_to_sheet(key)
                columns[key] = value
            
            elif isinstance(value, Formula):
                value.contribute_to_sheet(key)
                formulas[key] = value
        
        for formula_name, formula in formulas.items():
            for dep in formula.dependencies:
                graph.add_dependency(dep, formula_name)
        
        attrs["_columns"] = columns
        attrs["_formulas"] = formulas
        attrs["_graph"] = graph

        return super().__new__(cls, name, bases, attrs)

class Sheet(metaclass=SheetMeta):
    __rows__: ClassVar[list] = []

    _columns:   ClassVar[Dict[str, Any]]    = {}
    _formulas:  ClassVar[Dict[str, Any]]    = {}
    _graph:     ClassVar[DependencyGraph]   = DependencyGraph()

    @classmethod
    def schema(cls):
        return {"columns": cls._columns, "formulas": cls._formulas}
    
    @classmethod
    def insert(cls, **kwargs):
        cls.__rows__.append(kwargs)

    @classmethod
    def graph(cls) -> DependencyGraph:
        return cls._graph

    @classmethod
    def columns(cls) -> Dict[str, Any]:
        return cls._columns
    
    @classmethod
    def formulas(cls) -> Dict[str, Any]:
        return cls._formulas
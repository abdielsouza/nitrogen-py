from abc import ABC, abstractmethod
from .query import Query
from .contexts import CompilationContext
from typing import Type, Any

class QueryCompiler[T: CompilationContext](ABC):
    @abstractmethod
    def compile(self, query: Query, context: T) -> Any:
        pass
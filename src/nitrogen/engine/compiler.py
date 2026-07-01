from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .contexts import CompilationContext
from .query import Query

T = TypeVar("T", bound=CompilationContext)

class QueryCompiler(ABC, Generic[T]):
    """
    The query compiler is responsible for processing the query
    and return the compilation result.

    :param T: A generic type for compilation context.
    """

    @abstractmethod
    def compile(self, query: Query, context: T) -> Any:
        """
        It does the compiling process of the query.

        :param query: The query object.
        :type query: Query

        :param context: The compilation context.
        :type context: T

        :returns: The result of the query compilation. It can be anything.
        :rtype: Any
        """
        pass

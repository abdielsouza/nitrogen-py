from abc import ABC, abstractmethod
from typing import Any

from .query import Query
from .contexts import CompilationContext

class DataSource(ABC):
    @abstractmethod
    def execute(self, query: Query) -> Any:
        """
        Send the query to an appropriated compiler and return the result.

        :param query: The query instance.
        :type query: Query

        :returns: Anything.
        :rtype: Any
        """
        pass

    @property
    @abstractmethod
    def context(self) -> CompilationContext:
        pass
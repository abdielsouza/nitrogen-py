from abc import ABC
from abc import abstractmethod
from typing import Optional, Type, Protocol, TYPE_CHECKING
if TYPE_CHECKING:
    from nitrogen.core import Sheet, Column, Formula
    from nitrogen.core.expressions.base import Expression
else:
    # avoid importing runtime symbols to prevent circular imports; use string annotations
    Sheet = Column = Formula = object
    Expression = object


class Backend(ABC):
    @abstractmethod
    def create_sheet(self, sheet: Type[Sheet]) -> None:
        """Create a destination sheet (given a Sheet subclass)."""

    @abstractmethod
    def write_column(self, sheet: Type[Sheet], column: Column) -> None:
        """Write a single column (header + data) for `sheet`."""

    @abstractmethod
    def write_formula(self, sheet: Type[Sheet], formula: Formula) -> None:
        """Write a formula column for `sheet` (populate cells with formulas)."""

    @abstractmethod
    def save(self, path: Optional[str] = None) -> None:
        """Persist the backend output to `path` (or raise if missing)."""


class Compiler(ABC):
    @abstractmethod
    def compile(self, expr: Expression) -> str:
        pass

class IRemoteBehavior(Protocol):
    def connect(self, **kwargs) -> None: ...
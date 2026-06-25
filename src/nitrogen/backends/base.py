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
    @property
    @abstractmethod
    def data_rescue_lock(self) -> bool:
        pass

    @abstractmethod
    def disable_data_rescue_lock(self):
        pass

    @abstractmethod
    def create_sheet(self, sheet: Type[Sheet]) -> None:
        """Create a destination sheet (given a Sheet subclass).

        Args:
            sheet (Type[Sheet]): The sheet object to create in the platform.
        
        Returns:
            None
        """
    
    @abstractmethod
    def rescue_sheet(self, sheet: Type[Sheet]) -> None:
        """Rescue an existent sheet from the platform (given a Sheet subclass).

        Args:
            sheet (Type[Sheet]): The sheet object to rescue from the platform.
        
        Returns:
            None
        """

    @abstractmethod
    def write_column(self, sheet: Type[Sheet], column: Column) -> None:
        """Write a single column (header + data) for `sheet`.
        
        Args:
            sheet (Type[Sheet]): The sheet object
            column (Column): The column to write
        
        Returns:
            None
        """

    @abstractmethod
    def write_formula(self, sheet: Type[Sheet], formula: Formula) -> None:
        """Write a formula column for `sheet` (populate cells with formulas).

        Args:
            sheet (Type[Sheet]): The sheet object
            formula (Formula): The formula to write
        
        Returns:
            None
        """

    @abstractmethod
    def save(self, path: Optional[str] = None) -> None:
        """Persist the backend output to `path` (or raise if missing).

        Args:
            path (Optional[str]): The path where the sheet will be saved. Defaults to `None`
        
        Returns:
            None
        """


class Compiler(ABC):
    @abstractmethod
    def compile(self, expr: Expression) -> str:
        pass
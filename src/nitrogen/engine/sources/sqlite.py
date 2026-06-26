from nitrogen.engine.source import DataSource
from nitrogen.engine.compilers.sqlalchemy import SQLAlchemyCompiler
from nitrogen.engine.contexts import SQLAlchemyContext
from typing import cast, Any
import pathlib
import sqlalchemy as sql

class SQLiteDataSource(DataSource):
    """Implementation of SQLite data source."""
    
    def __init__(self, db_path: str):
        self._db_path = pathlib.Path(db_path).absolute().resolve()
        self._engine = sql.create_engine(f"sqlite://{self._db_path}")
        self._context = SQLAlchemyContext()
        self._compiler = SQLAlchemyCompiler()

    def execute(self, query):
        self._context.table = sql.Table(query.sheet, sql.MetaData())
        stmt = self._compiler.compile(query, self._context)

        with self._engine.connect() as conn:
            result = conn.execute(stmt)
            result = cast(Any, result)
            conn.commit()

            return result
from pathlib import Path
from typing import Any

import sqlalchemy as sql
from sqlalchemy.exc import NoSuchTableError

from nitrogen.engine.compiler import QueryCompiler
from nitrogen.engine.compilers.sqlalchemy import SQLAlchemyCompiler
from nitrogen.engine.contexts import SQLAlchemyContext
from nitrogen.engine.query import (
    DeleteQuery,
    FetchQuery,
    InsertQuery,
    Query,
    UpdateQuery,
)
from nitrogen.engine.source import DataSource

class SQLiteDataSource(DataSource):
    """Implementation of SQLite data source."""

    def __init__(self, db_path: str):
        self._db_path = Path(db_path).absolute().resolve()
        self._engine = sql.create_engine(f"sqlite:///{self._db_path}")
        self._metadata = sql.MetaData()
        self._context = SQLAlchemyContext()
        self._compiler = SQLAlchemyCompiler()

    def execute(self, query: Query):
        self._context.table = self._get_table(query.sheet, query)

        if self._context.table is None:
            if isinstance(query, FetchQuery):
                return []
            return 0

        stmt = self._compiler.compile(query, self._context)

        with self._engine.connect() as conn:
            result = conn.execute(stmt)

            if isinstance(query, FetchQuery):
                return [dict(row) for row in result.mappings().all()]

            conn.commit()
            return result.rowcount

    @property
    def context(self):
        return self._context

    def _get_table(self, sheet: str, query: Query):
        if sheet in self._metadata.tables:
            return self._metadata.tables[sheet]

        try:
            table = sql.Table(sheet, self._metadata, autoload_with=self._engine)
            return table
        except NoSuchTableError:
            if isinstance(query, InsertQuery):
                return self._create_table_from_registry(sheet, query.registry)
            return None

    def _create_table_from_registry(self, sheet: str, registry: dict[str, Any]):
        columns = []
        for key, value in registry.items():
            column_type = self._infer_column_type(value)
            columns.append(sql.Column(key, column_type, primary_key=(key == 'id')))

        table = sql.Table(sheet, self._metadata, *columns)
        table.create(self._engine, checkfirst=True)
        return table

    def _infer_column_type(self, value: Any):
        if isinstance(value, bool):
            return sql.Boolean
        if isinstance(value, int):
            return sql.Integer
        if isinstance(value, float):
            return sql.Float
        return sql.Text

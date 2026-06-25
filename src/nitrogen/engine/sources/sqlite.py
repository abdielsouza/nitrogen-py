from nitrogen.engine.source import DataSource
from nitrogen.engine.compilers.sqlalchemy import SQLAlchemyCompiler
from nitrogen.engine.contexts import SQLAlchemyContext
from nitrogen.engine.query import (
    cast_query_to_fetch,
    cast_query_to_insert,
    cast_query_to_update,
    cast_query_to_delete,
)
import sqlalchemy as sql

class SQLiteDataSource(DataSource):
    def __init__(self, db_path: str):
        self._engine = sql.create_engine(f"sqlite://{db_path}")
        self._context = SQLAlchemyContext()
        self._compiler = SQLAlchemyCompiler()

    def fetch(self, query):
        query = cast_query_to_fetch(query)

        self._context.table = sql.Table(query.sheet, sql.MetaData())
        stmt = self._compiler.compile(query, self._context)

        with self._engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()

            return result
    
    def insert(self, query):
        query = cast_query_to_insert(query)

        self._context.table = sql.Table(query.sheet, sql.MetaData())
        stmt = self._compiler.compile(query, self._context)

        with self._engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            
            return result

    def update(self, query):
        query = cast_query_to_update(query)

        self._context.table = sql.Table(query.sheet, sql.MetaData())
        stmt = self._compiler.compile(query, self._context)

        with self._engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            
            return result

    def delete(self, query):
        query = cast_query_to_delete(query)

        self._context.table = sql.Table(query.sheet, sql.MetaData())
        stmt = self._compiler.compile(query, self._context)

        with self._engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            
            return result
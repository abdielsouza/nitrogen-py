import sqlalchemy as sql
from nitrogen.engine.compiler import QueryCompiler
from nitrogen.engine.contexts import SQLAlchemyContext
from nitrogen.engine.query import (
    DeleteQuery,
    FetchQuery,
    Filter,
    InsertQuery,
    Operator,
    UpdateQuery,
)

class SQLAlchemyCompiler(QueryCompiler[SQLAlchemyContext]):
    def compile(self, query, context):
        if isinstance(query, FetchQuery):
            return self._compile_fetch(query, context.table)
        elif isinstance(query, InsertQuery):
            return self._compile_insert(query, context.table)
        elif isinstance(query, UpdateQuery):
            return self._compile_update(query, context.table)
        elif isinstance(query, DeleteQuery):
            return self._compile_delete(query, context.table)
        else:
            raise ValueError("unsupported query instance")

    def _compile_fetch(self, query: FetchQuery, table: sql.Table):
        columns = [getattr(table.c, field) for field in query.fields] if query.fields else [table]
        stmt = sql.select(*columns)

        for filter in query.filters:
            stmt = stmt.where(self._compile_filter(table, filter))
        
        if query.order_by is not None:
            stmt = stmt.order_by(getattr(table.c, query.order_by))
        
        if query.group_by is not None:
            stmt = stmt.group_by(getattr(table.c, query.group_by))
        
        return stmt
    
    def _compile_insert(self, query: InsertQuery, table: sql.Table):
        return sql.insert(table).values(query.registry)

    def _compile_update(self, query: UpdateQuery, table: sql.Table):
        stmt = sql.update(table)

        for filter in query.filters:
            stmt = stmt.where(self._compile_filter(table, filter))

        return stmt.values(query.registry)

    def _compile_delete(self, query: DeleteQuery, table: sql.Table):
        stmt = sql.delete(table)

        for filter in query.filters:
            stmt = stmt.where(self._compile_filter(table, filter))
        
        return stmt

    def _compile_filter(self, table: sql.Table, filter: Filter):
        column = getattr(table.c, filter.field)

        match filter.operator:
            case Operator.EQ:
                return column == filter.value
            case Operator.GT:
                return column > filter.value
            case Operator.LT:
                return column < filter.value
            case Operator.GTE:
                return column >= filter.value
            case Operator.LTE:
                return column <= filter.value
            case _:
                raise ValueError("unsupported operator")

from nitrogen.engine.compiler import QueryCompiler
from nitrogen.engine.contexts import GoogleSheetsContext
from nitrogen.engine.query import (
    FetchQuery,
    InsertQuery,
    UpdateQuery,
    DeleteQuery,
    Filter,
    Operator,
)
from typing import Callable, Any, cast
from collections import defaultdict


class GoogleSheetsCompiler(QueryCompiler[GoogleSheetsContext]):
    def compile(self, query, context):
        if isinstance(query, FetchQuery):
            return self._compile_fetch(query, context.worksheet)
        elif isinstance(query, InsertQuery):
            return self._compile_insert(query, context.worksheet)
        elif isinstance(query, UpdateQuery):
            return self._compile_update(query, context.worksheet)
        elif isinstance(query, DeleteQuery):
            return self._compile_delete(query, context.worksheet)
        else:
            raise ValueError("unsupported query type")

    def _compile_fetch(self, query: FetchQuery, worksheet):
        records = worksheet.get_all_records()

        for filter_ in query.filters:
            predicate = self._compile_filter(filter_)
            records = list(filter(predicate, records))

        if query.fields:
            records = [{k: record[k] for k in query.fields if k in record} for record in records]

        if query.order_by:
            records.sort(key=lambda r: r[query.order_by])

        return records

    def _compile_insert(self, query: InsertQuery, worksheet):
        headers = worksheet.row_values(1)
        row = [query.registry.get(str(column)) for column in headers]
        worksheet.append_row(row)

    def _compile_update(self, query: UpdateQuery, worksheet):
        headers = worksheet.row_values(1)
        records = worksheet.get_all_records()

        for index, record in enumerate(records, start=2):
            if all(self._compile_filter(f)(record) for f in query.filters):
                for i, column in enumerate(headers):
                    if column in query.registry:
                        worksheet.update_cell(index, i + 1, query.registry[str(column)])

    def _compile_delete(self, query: DeleteQuery, worksheet):
        records = worksheet.get_all_records()
        rows_to_delete = []
        headers = worksheet.row_values(1)

        for index, record in enumerate(records, start=2):
            if all(self._compile_filter(f)(record) for f in query.filters):
                rows_to_delete.append(index)

        for index in reversed(rows_to_delete):
            worksheet.delete_rows(index)

    def _compile_filter(self, filter: Filter) -> Callable[[dict[str, Any]], bool]:
        match filter.operator:
            case Operator.EQ:
                return lambda r: r[filter.field] == filter.value
            case Operator.GT:
                return lambda r: r[filter.field] > filter.value
            case Operator.LT:
                return lambda r: r[filter.field] < filter.value
            case Operator.GTE:
                return lambda r: r[filter.field] >= filter.value
            case Operator.LTE:
                return lambda r: r[filter.field] <= filter.value
            case _:
                raise ValueError("unsupported operator")

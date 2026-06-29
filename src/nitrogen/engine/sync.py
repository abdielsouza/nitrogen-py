from .diff import DiffEngine
from .query import QueryBuilder, Operator
from .source import DataSource
from .plan import SyncPlan

class SyncEngine:
    def __init__(self, source_a: DataSource, source_b: DataSource):
        self._source_a = source_a
        self._source_b = source_b
        self._diff_engine = DiffEngine()
    
    def sync(self, sheet: str, pk: str = "id"):
        """
        This method will synchronize the sheet changes between two sources

        :param sheet: The sheet where the changes were made.
        :type sheet: str

        :param pk: The primary key the be used as reference in the sync plan.
        :type pk: str

        :returns: The sync plan object.
        :rtype: SyncPlan
        """

        query = QueryBuilder.fetch(sheet).build()

        records_a = self._source_a.execute(query)
        records_b = self._source_b.execute(query)
        plan = self._diff_engine.compare(records_a, records_b, pk)

        self._apply_sync(plan, sheet, pk)

        return plan

    def _apply_sync(self, plan: SyncPlan, sheet: str, pk: str):
        for row in plan.inserts_a:
            query = QueryBuilder.insert(sheet).values(**row).build()
            self._source_a.execute(query)

        for row in plan.inserts_b:
            query = QueryBuilder.insert(sheet).values(**row).build()
            self._source_b.execute(query)
        
        for row in plan.updates_a:
            query = QueryBuilder.update(sheet).where(pk, Operator.EQ, row[pk]).values(**row).build()
            self._source_a.execute(query)

        for row in plan.updates_b:
            query = QueryBuilder.update(sheet).where(pk, Operator.EQ, row[pk]).values(**row).build()
            self._source_b.execute(query)

        for row in plan.deletes_a:
            query = QueryBuilder.delete(sheet).where(pk, Operator.EQ, row[pk]).build()
            self._source_a.execute(query)

        for row in plan.deletes_b:
            query = QueryBuilder.delete(sheet).where(pk, Operator.EQ, row[pk]).build()
            self._source_b.execute(query)

from nitrogen.engine.sources.excel import ExcelDataSource
from nitrogen.engine.sources.sqlite import SQLiteDataSource

__all__ = [
    'SyncEngine',
    'ExcelDataSource',
    'SQLiteDataSource',
]
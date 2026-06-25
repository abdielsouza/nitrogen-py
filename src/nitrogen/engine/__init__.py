from .diff import DiffEngine
from .query import QueryBuilder
from .source import DataSource
from .plan import SyncPlan

class SyncEngine:
    def __init__(self, source_a: DataSource, source_b: DataSource):
        self._source_a = source_a
        self._source_b = source_b
        self._diff_engine = DiffEngine()
    
    def sync(self, sheet: str, pk: str = "id"):
        query = QueryBuilder.fetch(sheet).build()

        records_a = self._source_a.fetch(query)
        records_b = self._source_b.fetch(query)
        plan = self._diff_engine.compare(records_a, records_b, pk)

        self._apply(plan, sheet)

        return plan

    def _apply(self, plan: SyncPlan, sheet: str):
        for row in plan.inserts_a:
            query = QueryBuilder.insert(sheet).values(**row).build()
            self._source_a.insert(query)

        for row in plan.inserts_b:
            query = QueryBuilder.insert(sheet).values(**row).build()
            self._source_b.insert(query)
        
        for row in plan.updates_a:
            query = QueryBuilder.update(sheet).values(**row).build()
            self._source_a.update(query)

        for row in plan.updates_b:
            query = QueryBuilder.update(sheet).values(**row).build()
            self._source_b.update(query)
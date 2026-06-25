from .plan import SyncPlan

class DiffEngine:
    def compare(self, records_a: list[dict], records_b: list[dict], pk: str = "id") -> SyncPlan:
        plan = SyncPlan()

        map_a = {row[pk]: row for row in records_a}
        map_b = {row[pk]: row for row in records_b}

        ids_a = set(map_a.keys())
        ids_b = set(map_b.keys())

        for id_ in ids_a - ids_b:
            plan.inserts_b.append(map_a[id_])
        
        for id_ in ids_b - ids_a:
            plan.inserts_a.append(map_b[id_])
        
        for id_ in ids_a & ids_b:
            row_a = map_a[id_]
            row_b = map_b[id_]

            if row_a != row_b:
                plan.updates_a.append(row_b)
                plan.updates_b.append(row_a)
        
        return plan
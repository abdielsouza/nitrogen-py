from dataclasses import dataclass, field

@dataclass
class SyncPlan:
    inserts_a: list[dict] = field(default_factory=list)
    updates_a: list[dict] = field(default_factory=list)
    deletes_a: list[dict] = field(default_factory=list)

    inserts_b: list[dict] = field(default_factory=list)
    updates_b: list[dict] = field(default_factory=list)
    deletes_b: list[dict] = field(default_factory=list)
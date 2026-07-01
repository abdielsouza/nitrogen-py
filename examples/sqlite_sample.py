from nitrogen.engine import SQLiteDataSource
from nitrogen.engine.query import QueryBuilder, Operator

source = SQLiteDataSource("examples/sqlite_sample.db")

source.execute(QueryBuilder.insert("Users").values(id=1, name="john", email="john@example.com", role="member").build())
source.execute(QueryBuilder.insert("Users").values(id=2, name="anna", email="anna@example.com", role="admin").build())

print("Users after insert:", source.execute(QueryBuilder.fetch("Users").build()))

source.execute(QueryBuilder.update("Users").where("id", Operator.EQ, 2).values(role="guest").build())
print("Users after update:", source.execute(QueryBuilder.fetch("Users").build()))

source.execute(QueryBuilder.delete("Users").where("id", Operator.EQ, 1).build())
print("Users after delete:", source.execute(QueryBuilder.fetch("Users").build()))

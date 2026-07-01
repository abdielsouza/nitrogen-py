from nitrogen.engine import GoogleSheetsSource
from nitrogen.engine.query import QueryBuilder, Operator

SPREADSHEET_ID = "<YOUR_SPREADSHEET_ID>"
CREDENTIALS_FILE = "examples/credentials.json"

source = GoogleSheetsSource(SPREADSHEET_ID, CREDENTIALS_FILE)

source.execute(QueryBuilder.insert("Users").values(id=1, name="john", email="john@example.com", role="member").build())
source.execute(QueryBuilder.insert("Users").values(id=2, name="anna", email="anna@example.com", role="admin").build())

print("Users after insert:", source.execute(QueryBuilder.fetch("Users").build()))

source.execute(QueryBuilder.update("Users").where("id", Operator.EQ, 2).values(role="owner").build())
print("Users after update:", source.execute(QueryBuilder.fetch("Users").build()))

source.execute(QueryBuilder.delete("Users").where("id", Operator.EQ, 1).build())
print("Users after delete:", source.execute(QueryBuilder.fetch("Users").build()))

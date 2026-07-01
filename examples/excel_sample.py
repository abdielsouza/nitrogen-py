import nitrogen.core as nt
from nitrogen.engine import ExcelDataSource, WorkbookEngine
from nitrogen.engine.query import QueryBuilder, Operator

class Users(nt.Sheet):
    id = nt.Column(int)
    name = nt.Column(str)
    email = nt.Column(str)
    role = nt.Column(str)

workbook = nt.Workbook()
source = ExcelDataSource("examples/excel_sample.xlsx")
engine = WorkbookEngine(source)

Users.insert(id=1, name="john", email="john@example.com", role="member")
Users.insert(id=2, name="anna", email="anna@example.com", role="admin")

workbook.add_sheet(Users)
engine.save(workbook)

print("Saved Excel workbook to examples/excel_sample.xlsx")

query = QueryBuilder.fetch("Users").where("role", Operator.EQ, "admin").build()
admin_records = source.execute(query)
print("Admin records:", admin_records)

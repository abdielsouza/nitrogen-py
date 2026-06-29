import nitrogen.core as nt
import nitrogen.engine as nte
from typing import Literal

class Users(nt.Sheet):
    type Role = Literal["visitant", "member", "admin"]

    id = nt.Column(int)
    name = nt.Column(str)
    email = nt.Column(str)
    role = nt.Column(type[Role])

workbook = nt.Workbook()
source = nte.ExcelDataSource("excel_sample.xlsx")
engine = nte.WorkbookEngine(source)

Users.insert(id=1, name="john", email="johnnymail@hotmail.com", role="member")
Users.insert(id=2, name="anna", email="annagirlly@hotmail.com", role="admin")

workbook.add_sheet(Users)
engine.save(workbook)
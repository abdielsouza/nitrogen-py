import openpyxl
import nitrogen.core as nt
from nitrogen.backends.excel.backend import ExcelBackend
from nitrogen.core.workbook import Workbook as NitrogenWorkbook

class Products(nt.Sheet, alt_name="Tabela de Produtos"):
	quantity = nt.Column(int)
	price = nt.Column(float)
	total = nt.Formula(quantity * price)

# insert rows
Products.insert(quantity=2, price=3.5)
Products.insert(quantity=10, price=1.2)

# write to an Excel workbook using the provided backend
wb = openpyxl.Workbook()
backend = ExcelBackend(wb)

nwb = NitrogenWorkbook()
nwb.add(Products)
nwb.sync(backend, path="products.xlsx")
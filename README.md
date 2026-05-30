
Nitrogen
========

Lightweight Python framework for defining spreadsheet-style data models (Sheets) with typed Columns and computed Formula columns. Nitrogen provides a dependency graph for formulas and pluggable backends to render data and formulas to destinations such as Excel workbooks.

Key features
------------
- Define data schemas as `Sheet` subclasses composed of `Column` and `Formula` members.
- Build formula expressions using Python operators (`+`, `-`, `*`, `/`) on column references.
- Automatic dependency graph generation and execution ordering for formula evaluation.
- Pluggable backend system (example: Excel backend using `openpyxl`).

Installation
------------
Install from source (recommended for development) or add as a dependency in your project:

```bash
python -m pip install -e .
```

Requirements are declared in [pyproject.toml](pyproject.toml#L1-L40). Nitrogen depends on `openpyxl`, `gspread` and `polars` for optional backends and data handling.

Quick start
-----------
Create a `Sheet` by subclassing `nitrogen.Sheet`, declare `Column` fields and `Formula` fields composed from column references:

```python
import openpyxl
import nitrogen as nt
from nitrogen.backends.excel.backend import ExcelBackend

class Products(nt.Sheet):
	quantity = nt.Column(int)
	price = nt.Column(float)
	total = nt.Formula(quantity * price)

# insert rows
Products.insert(quantity=2, price=3.5)
Products.insert(quantity=10, price=1.2)

# write to an Excel workbook using the provided backend
wb = openpyxl.Workbook()
backend = ExcelBackend(wb)
from nitrogen.core.workbook import Workbook as NitrogenWorkbook
nwb = NitrogenWorkbook()
nwb.add(Products)
nwb.sync(backend, path="products.xlsx")
```

API & internals
---------------
- Sheet metaclass and schema: [src/nitrogen/core/sheet.py](src/nitrogen/core/sheet.py#L1-L200)
- Column and Formula primitives: [src/nitrogen/core/column.py](src/nitrogen/core/column.py#L1-L200), [src/nitrogen/core/formula.py](src/nitrogen/core/formula.py#L1-L200)
- Expression system and arithmetic operators: [src/nitrogen/core/expressions](src/nitrogen/core/expressions/references.py#L1-L200)
- Excel backend and compiler example: [src/nitrogen/backends/excel/backend.py](src/nitrogen/backends/excel/backend.py#L1-L300), [src/nitrogen/backends/excel/compiler.py](src/nitrogen/backends/excel/compiler.py#L1-L200)

Testing
-------
Run the test suite with `pytest`:

```bash
python -m pip install -r requirements-dev.txt  # if you maintain dev deps
pytest -q
```

Project status & contribution
-----------------------------
This repository is an early-stage implementation. Contributions, bug reports and feature requests are welcome. To contribute:

1. Open an issue describing the desired change.
2. Open a pull request with tests and clear description of the change.

License
-------
See the repository LICENSE file.


Nitrogen
========

Lightweight Python framework for defining spreadsheet-style data models (Sheets) with typed Columns and computed Formula columns. Nitrogen provides a dependency graph for formulas and pluggable backends to render data and formulas to destinations such as Excel workbooks.

Key features
------------

- Define data schemas as `Sheet` subclasses composed of `Column` and `Formula` members.
- Build formula expressions using Python operators (`+`, `-`, `*`, `/`) on column references.
- Automatic dependency graph generation and execution ordering for formula evaluation.
- Pluggable data source system (example: Excel data source using `openpyxl`).
- Synchronization engine with external data sources, like Postgres or SQLite.

Project modules
---------------

The framework is divided into many small modules to separate features and responsibilities.

- `core`: The fundamental pillars of the library are located here. It contains the main structures and functionalities of the framework.
- `engine`: The synchronization engine that allows the information of spreadsheets to be sent to external data sources.
- `cli`: The command-line tools to use the Nitrogen framework as executable.

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
```

Testing
-------

Run the test suite with `pytest`:

```bash
python -m pip install -r requirements.txt  # if you maintain dev deps
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

# The main concepts of the Nitrogen Framework

## 1. The Core:

The framework core is divided into several structures that are the pillars of the project. Conceptually, the Nitrogen works with **sheets, columns and formulas** that can be created and updated as Python class fields.

- `Sheet`: It represents the spreadsheet we'll be working into. The spreadsheet is basically a Python class with public properties that can be accessed and modified at any time.
  - `Column`: Represents a sheet column. It has name and type.
  - `Formula`: They are dynamic values that changes when one of its dependencies change.
- `Workbook`: The workbook is a collection of sheets.

## 2. The Engine:

The framework comes with an embedded synchronization engine to make connections between different data sources. For example: you can send data from an Excel spreadsheet to a SQLite database, or send data from a Postgres database to Google Sheets. It's a bidirectional relation.

- `DataSource`: A Python class that represents an external data source. It can be either a database or a spreadsheet platform.
- `Query`: It represents a query action in a data source. In other words, it describes the action of writing, reading or removing data from a data source.
- `SyncPlan`: A kind of "transaction storage" that registers all the queries to be commited by the engine.
- `SyncEngine`: The main entity of this module. It's responsible for connecting two data sources and synchronizing incoming data between them.

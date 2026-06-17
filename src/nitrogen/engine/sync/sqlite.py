from __future__ import annotations

from .abstract import *
from result import Ok, Err
from typing import TextIO
import sqlite3

class SQLiteSource(DataSource):
    def __init__(self, connector: SQLiteConnector | str):
        if isinstance(connector, str):
            self._connector = SQLiteConnector(connector)
        else:
            self._connector = connector

    def fetch(self, sheet, params):
        fields = ", ".join(params.fields) if params.fields else "*"
        query = f"SELECT {fields} FROM {sheet}"
        values: list = []

        if getattr(params, "where", None) and params.where is not None:
            clauses = []
            for k, v in params.where.items():
                clauses.append(f"{k} = ?")
                values.append(v)
            query += " WHERE " + " AND ".join(clauses)

        if getattr(params, "group_by", None) and params.group_by is not None:
            query += f" GROUP BY {params.group_by}"

        if getattr(params, "order_by", None) and params.order_by is not None:
            query += f" ORDER BY {params.order_by}"

        # ensure connection
        if getattr(self._connector, "_connection", None) is None:
            conn_res = self._connector.connect()
            if isinstance(conn_res, Err):
                return conn_res

        return self._connector.execute(query, *values)

    def insert(self, sheet, params):
        field_names = ", ".join(params.registry.keys())
        field_values = ", ".join(params.registry.values())
        query = f"INSERT INTO {sheet} ({field_names}) VALUES ({field_values})"

        if getattr(self._connector, "_connection", None) is None:
            conn_res = self._connector.connect()
            if isinstance(conn_res, Err):
                return conn_res
        
        return self._connector.execute(query)

    def upsert(self, sheet, params):
        field_names = ", ".join(params.registry.keys())
        field_values = ", ".join(params.registry.values())
        query = f"INSERT OR REPLACE INTO {sheet} ({field_names}) VALUES ({field_values})"

        if getattr(self._connector, "_connection", None) is None:
            conn_res = self._connector.connect()
            if isinstance(conn_res, Err):
                return conn_res

        return self._connector.execute(query)

    def update(self, sheet, params):
        set_clauses = []
        for k, v in params.registry.items():
            set_clauses.append(f"{k} = {v}")
        query = f"UPDATE {sheet} SET " + ", ".join(set_clauses)

        if getattr(params, "where", None) and params.where is not None:
            clauses = []
            for k, v in params.where.items():
                clauses.append(f"{k} = {v}")
            query += " WHERE " + " AND ".join(clauses)

        if getattr(self._connector, "_connection", None) is None:
            conn_res = self._connector.connect()
            if isinstance(conn_res, Err):
                return conn_res

        return self._connector.execute(query)

    def delete(self, sheet, params):
        query = f"DELETE FROM {sheet}"

        if getattr(params, "where", None) and params.where is not None:
            clauses = []
            for k, v in params.where.items():
                clauses.append(f"{k} = {v}")
            query += " WHERE " + " AND ".join(clauses)

        if getattr(self._connector, "_connection", None) is None:
            conn_res = self._connector.connect()
            if isinstance(conn_res, Err):
                return conn_res

        return self._connector.execute(query)

class SQLiteConnector(DatabaseConnector):
    def __init__(self, database: str):
        super().__init__()
        self._database = database
    
    def connect(self):
        try:
            self._connection = sqlite3.connect(self._database, timeout=10)
            return Ok(None)
        
        except Exception as err:
            return Err(str(err))
    
    def close(self):
        try:
            self._connection.close()
            return Ok(None)
        
        except Exception as err:
            return Err(str(err))
    
    def execute(self, query, *args, **kwargs):
        try:
            if self._connection is None:
                # lazy connect
                conn_res = self.connect()
                if isinstance(conn_res, Err):
                    return conn_res

            cursor = self._connection.cursor()

            if isinstance(query, TextIO):
                query_text = query.read()
            else:
                query_text = query

            if args:
                cursor.execute(query_text, args)
            else:
                cursor.execute(query_text)

            sql = query_text.strip().lower()
            if sql.startswith("select"):
                rows = cursor.fetchall()
                return Ok(rows)
            else:
                self._connection.commit()
                return Ok(cursor.rowcount)
        
        except Exception as err:
            return Err(str(err))
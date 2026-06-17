from __future__ import annotations

from typing import TextIO

from .abstract import *
from result import Ok, Err

try:
    import psycopg2 as psycopg
except ImportError:  # pragma: no cover
    psycopg = None


class PostgresSource(DataSource):
    def __init__(self, connector: PostgresConnector | str):
        if isinstance(connector, str):
            self._connector = PostgresConnector(connector)
        else:
            self._connector = connector

    def _ensure_connection(self):
        if getattr(self._connector, "_connection", None) is None:
            conn_res = self._connector.connect()
            if isinstance(conn_res, Err):
                return conn_res
        return Ok(None)

    def fetch(self, sheet, params):
        fields = ", ".join(params.fields) if params.fields else "*"
        query = f"SELECT {fields} FROM {sheet}"
        values: list = []

        if getattr(params, "where", None) and params.where is not None:
            clauses = []
            for k, v in params.where.items():
                clauses.append(f"{k} = %s")
                values.append(v)
            query += " WHERE " + " AND ".join(clauses)

        if getattr(params, "group_by", None) and params.group_by is not None:
            query += f" GROUP BY {params.group_by}"

        if getattr(params, "order_by", None) and params.order_by is not None:
            query += f" ORDER BY {params.order_by}"

        conn_res = self._ensure_connection()
        if isinstance(conn_res, Err):
            return conn_res

        return self._connector.execute(query, *values)

    def insert(self, sheet, params):
        field_names = ", ".join(params.registry.keys())
        field_values = ", ".join(str(v) for v in params.registry.values())
        query = f"INSERT INTO {sheet} ({field_names}) VALUES ({field_values})"

        conn_res = self._ensure_connection()
        if isinstance(conn_res, Err):
            return conn_res

        return self._connector.execute(query)

    def upsert(self, sheet, params):
        field_names = ", ".join(params.registry.keys())
        field_values = ", ".join(str(v) for v in params.registry.values())
        query = f"INSERT INTO {sheet} ({field_names}) VALUES ({field_values})"

        if "id" in params.registry:
            update_clauses = [
                f"{k} = {v}" for k, v in params.registry.items() if k != "id"
            ]
            if update_clauses:
                query += f" ON CONFLICT (id) DO UPDATE SET {', '.join(update_clauses)}"
            else:
                query += " ON CONFLICT (id) DO NOTHING"

        conn_res = self._ensure_connection()
        if isinstance(conn_res, Err):
            return conn_res

        return self._connector.execute(query)

    def update(self, sheet, params):
        set_clauses = [f"{k} = {v}" for k, v in params.registry.items()]
        query = f"UPDATE {sheet} SET " + ", ".join(set_clauses)

        if getattr(params, "where", None) and params.where is not None:
            clauses = [f"{k} = {v}" for k, v in params.where.items()]
            query += " WHERE " + " AND ".join(clauses)

        conn_res = self._ensure_connection()
        if isinstance(conn_res, Err):
            return conn_res

        return self._connector.execute(query)

    def delete(self, sheet, params):
        query = f"DELETE FROM {sheet}"

        if getattr(params, "where", None) and params.where is not None:
            clauses = [f"{k} = {v}" for k, v in params.where.items()]
            query += " WHERE " + " AND ".join(clauses)

        conn_res = self._ensure_connection()
        if isinstance(conn_res, Err):
            return conn_res

        return self._connector.execute(query)


class PostgresConnector(DatabaseConnector):
    def __init__(self, dsn: str):
        super().__init__()
        self._dsn = dsn

    def connect(self):
        if psycopg is None:
            return Err("psycopg is required for Postgres support. Install it with `pip install psycopg[binary]`.")

        try:
            if isinstance(self._dsn, dict):
                self._connection = psycopg.connect(self._dsn)
            else:
                self._connection = psycopg.connect(self._dsn)
            return Ok(None)
        except Exception as err:
            return Err(str(err))

    def close(self):
        try:
            if self._connection is not None:
                self._connection.close()
            return Ok(None)
        except Exception as err:
            return Err(str(err))

    def execute(self, query, *args, **kwargs):
        try:
            if self._connection is None:
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

            self._connection.commit()
            return Ok(cursor.rowcount)
        except Exception as err:
            return Err(str(err))

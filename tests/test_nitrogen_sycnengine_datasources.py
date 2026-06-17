import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from result import Ok
from nitrogen.engine.sync import SQLiteConnector, SQLiteSource, PostgresSource


class DummyConnector:
    def __init__(self):
        self.last_query = None
        self.last_args = None
        self._connection = True

    def connect(self):
        return Ok(None)

    def close(self):
        return Ok(None)

    def execute(self, query, *args, **kwargs):
        self.last_query = query
        self.last_args = args
        return Ok([])


def test_sqlite_connector_basic_operations():
    conn = SQLiteConnector(":memory:")
    assert isinstance(conn.connect(), Ok)

    # create table
    res = conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    assert isinstance(res, Ok)

    # insert rows
    res = conn.execute("INSERT INTO users (name) VALUES (?)", "Alice")
    assert isinstance(res, Ok)

    # select rows
    res = conn.execute("SELECT id, name FROM users")
    assert isinstance(res, Ok)


def test_sqlite_source_fetch_with_where_and_order():
    conn = SQLiteConnector(":memory:")
    src = SQLiteSource(conn)
    assert isinstance(conn.connect(), Ok)

    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    conn.execute("INSERT INTO items (name, price) VALUES (?, ?)", "a", 1.0)
    conn.execute("INSERT INTO items (name, price) VALUES (?, ?)", "b", 2.0)

    params = SimpleNamespace(fields=["id", "name", "price"], where={"price": 2.0}, group_by=None, order_by="id")
    res = src.fetch("items", params)
    assert isinstance(res, Ok)


def test_postgres_source_builds_placeholders_and_calls_connector():
    mock = DummyConnector()
    src = PostgresSource(mock)

    params = SimpleNamespace(fields=["id", "name"], where={"id": 5}, group_by=None, order_by=None)
    res = src.fetch("users", params)
    assert isinstance(res, Ok)

    assert "%s" in mock.last_query
    assert mock.last_args == (5,)


def test_postgres_upsert_generates_on_conflict():
    mock = DummyConnector()
    src = PostgresSource(mock)

    params = SimpleNamespace(registry={"id": 1, "name": "'Alice'"})
    res = src.upsert("users", params)
    assert isinstance(res, Ok)

    assert "ON CONFLICT" in mock.last_query.upper()

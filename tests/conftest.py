import sqlite3

import pytest

from app.database import connection as database_connection
from app.database import schema as database_schema
from app.services import transactions
from app.services import reports


@pytest.fixture
def test_db(monkeypatch, tmp_path):
    database_path = tmp_path / "teste.db"

    def get_test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    monkeypatch.setattr(
        database_connection,
        "get_connection",
        get_test_connection,
    )

    monkeypatch.setattr(
        database_schema,
        "get_connection",
        get_test_connection,
    )

    monkeypatch.setattr(
        transactions,
        "get_connection",
        get_test_connection,
    )

    monkeypatch.setattr(
        reports,
        "get_connection",
        get_test_connection,
    )

    database_schema.initialize_database()

    return database_path
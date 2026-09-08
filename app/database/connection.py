import sqlite3
from pathlib import Path

from app.utils.paths import get_database_path


def get_connection() -> sqlite3.Connection:
    """
    Cria uma conexão com o banco de dados SQLite.
    """

    database_path: Path = get_database_path()

    connection = sqlite3.connect(database_path)

    connection.row_factory = sqlite3.Row

    # Garante integridade das chaves estrangeiras.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
import sqlite3

from app.database import schema
from app.database import backup


def test_cria_backup(monkeypatch, tmp_path):
    database_path = tmp_path / "financeiro.db"
    backups_dir = tmp_path / "backups"

    def get_test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    monkeypatch.setattr(
        backup,
        "get_connection",
        get_test_connection,
    )

    monkeypatch.setattr(
        backup,
        "get_backups_dir",
        lambda: backups_dir,
    )

    monkeypatch.setattr(
        schema,
        "get_connection",
        get_test_connection,
    )

    schema.initialize_database()

    with get_test_connection() as connection:
        connection.execute(
            """
            INSERT INTO transacoes (
                tipo,
                descricao,
                valor_centavos,
                data_transacao,
                data_criacao,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "GANHO",
                "Teste backup",
                10000,
                "2026-09-08",
                "2026-09-08T10:00:00",
                "ATIVA",
            ),
        )

    backup_path = backup.create_backup()

    assert backup_path.exists()
    assert backup_path.stat().st_size > 0

    with sqlite3.connect(backup_path) as connection:
        row = connection.execute(
            """
            SELECT descricao, valor_centavos
            FROM transacoes
            WHERE descricao = ?
            """,
            ("Teste backup",),
        ).fetchone()

    assert row is not None
    assert row[0] == "Teste backup"
    assert row[1] == 10000


def test_limita_quantidade_de_backups(
    monkeypatch,
    tmp_path,
):
    backups_dir = tmp_path / "backups"
    backups_dir.mkdir()

    monkeypatch.setattr(
        backup,
        "get_backups_dir",
        lambda: backups_dir,
    )

    for number in range(35):
        backup_file = (
            backups_dir
            / f"financeiro_backup_{number:02d}.db"
        )

        sqlite3.connect(backup_file).close()

    backup.cleanup_old_backups(max_backups=30)

    backups = list(
        backups_dir.glob("financeiro_backup_*.db")
    )

    assert len(backups) == 30


def test_nao_permite_limite_invalido():
    try:
        backup.cleanup_old_backups(0)
        assert False
    except ValueError:
        pass
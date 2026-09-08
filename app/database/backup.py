from pathlib import Path
import sqlite3
from app.utils.logger import logger

from app.database.connection import get_connection
from app.utils.paths import get_backups_dir
from app.utils.dates import now


MAX_BACKUPS = 30


def create_backup() -> Path:
    """
    Cria um backup do banco de dados SQLite.

    O backup é salvo no diretório oficial de backups.
    """
    backups_dir = get_backups_dir()
    backups_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = now().replace(":", "-")
    backup_path = (
        backups_dir
        / f"financeiro_backup_{timestamp}.db"
    )

    source_connection = get_connection()

    try:
        backup_connection = sqlite3.connect(backup_path)

        try:
            source_connection.backup(backup_connection)
        finally:
            backup_connection.close()
    finally:
        source_connection.close()
        
        logger.info(
            "Backup criado | arquivo=%s",
            backup_path,
        )

    return backup_path


def cleanup_old_backups(
    max_backups: int = MAX_BACKUPS,
) -> None:
    """
    Remove backups antigos, mantendo apenas os mais recentes.
    """
    if max_backups < 1:
        raise ValueError(
            "A quantidade máxima de backups deve ser maior que zero."
        )

    backups_dir = get_backups_dir()

    backups = sorted(
        backups_dir.glob("financeiro_backup_*.db"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    for backup in backups[max_backups:]:
        backup.unlink()


def create_backup_and_cleanup() -> Path:
    """
    Cria um novo backup e remove os backups excedentes.
    """
    backup_path = create_backup()
    cleanup_old_backups()
    
    logger.info(
        "Backup criado | arquivo=%s",
        backup_path,
    )

    return backup_path
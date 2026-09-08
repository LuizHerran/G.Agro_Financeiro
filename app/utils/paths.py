from pathlib import Path


APP_NAME = "ControleFinanceiro"


def get_data_dir() -> Path:
    """
    Retorna a pasta onde ficam os dados persistentes da aplicação.
    """
    local_app_data = Path.home() / "AppData" / "Local" / APP_NAME
    local_app_data.mkdir(parents=True, exist_ok=True)

    return local_app_data


def get_database_path() -> Path:
    """
    Retorna o caminho do banco SQLite.
    """
    return get_data_dir() / "financeiro.db"


def get_logs_dir() -> Path:
    """
    Retorna a pasta de logs.
    """
    logs_dir = get_data_dir() / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    return logs_dir


def get_backups_dir() -> Path:
    """
    Retorna a pasta de backups.
    """
    backups_dir = get_data_dir() / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

    return backups_dir
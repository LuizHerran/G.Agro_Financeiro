import logging
from pathlib import Path

from app.utils.paths import get_logs_dir


LOGGER_NAME = "ControleFinanceiro"


def get_logger() -> logging.Logger:
    """
    Retorna o logger principal da aplicação.
    """
    logger = logging.getLogger(LOGGER_NAME)

    if logger.handlers:
        return logger

    logs_dir = get_logs_dir()
    log_path = logs_dir / "sistema.log"

    handler = logging.FileHandler(
        log_path,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


logger = get_logger()
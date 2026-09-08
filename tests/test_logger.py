import logging

from app.utils import logger as logger_module


def test_logger_grava_mensagem(monkeypatch, tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()

    monkeypatch.setattr(
        logger_module,
        "get_logs_dir",
        lambda: logs_dir,
    )

    test_logger = logging.getLogger("TesteControleFinanceiro")

    for handler in test_logger.handlers[:]:
        test_logger.removeHandler(handler)
        handler.close()

    log_path = logs_dir / "sistema.log"

    handler = logging.FileHandler(
        log_path,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)
    test_logger.addHandler(handler)
    test_logger.setLevel(logging.INFO)

    try:
        test_logger.info("Mensagem de teste")
    finally:
        test_logger.removeHandler(handler)
        handler.close()

    assert log_path.exists()

    content = log_path.read_text(
        encoding="utf-8"
    )

    assert "INFO | Mensagem de teste" in content
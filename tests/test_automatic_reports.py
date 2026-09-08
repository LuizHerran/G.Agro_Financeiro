from datetime import date

from app.reports.automatic_reports import (
    get_reports_dir,
)


def test_diretorio_de_relatorios(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "app.reports.automatic_reports.Path.home",
        lambda: tmp_path,
    )

    reports_dir = get_reports_dir()

    assert reports_dir == (
        tmp_path
        / "Documents"
        / "Controle Financeiro"
    )

    assert reports_dir.exists()
    assert reports_dir.is_dir()
import sys
import main

def test_main_sem_argumentos(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py"],
    )

    monkeypatch.setattr(
        main,
        "initialize_database",
        lambda: None,
    )

    main.main()

    captured = capsys.readouterr()

    assert (
        captured.out.strip()
        == "Banco de dados inicializado com sucesso."
    )


def test_main_relatorio_semanal(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py", "--weekly-report"],
    )

    monkeypatch.setattr(
        main,
        "initialize_database",
        lambda: None,
    )

    monkeypatch.setattr(
        main,
        "generate_weekly_report",
        lambda: "relatorio_semanal.csv",
    )

    main.main()

    captured = capsys.readouterr()

    assert (
        captured.out.strip()
        == "Relatório semanal criado: relatorio_semanal.csv"
    )


def test_main_relatorio_mensal(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py", "--monthly-report"],
    )

    monkeypatch.setattr(
        main,
        "initialize_database",
        lambda: None,
    )

    monkeypatch.setattr(
        main,
        "generate_monthly_report",
        lambda: "relatorio_mensal.csv",
    )

    main.main()

    captured = capsys.readouterr()

    assert (
        captured.out.strip()
        == "Relatório mensal criado: relatorio_mensal.csv"
    )
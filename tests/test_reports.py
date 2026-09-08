import pytest

from app.services.transactions import (
    create_income,
    create_expense,
    cancel_transaction,
)

from app.services.reports import get_report_data


def test_relatorio_calcula_totais(test_db):

    create_income(
        "Venda 1",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda 2",
        30000,
        "2026-09-02",
    )

    create_expense(
        "Material",
        5000,
        "2026-09-03",
    )

    relatorio = get_report_data(
        "2026-09-01",
        "2026-09-03",
    )

    assert relatorio["total_ganhos"] == 40000
    assert relatorio["total_gastos"] == 5000
    assert relatorio["lucro_real"] == 35000


def test_relatorio_calcula_percentual_dos_ganhos(test_db):

    create_income(
        "Venda 1",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda 2",
        30000,
        "2026-09-02",
    )

    relatorio = get_report_data(
        "2026-09-01",
        "2026-09-02",
    )

    ganhos = relatorio["ganhos"]

    assert len(ganhos) == 2

    assert ganhos[0]["percentual"] == pytest.approx(25.0)
    assert ganhos[1]["percentual"] == pytest.approx(75.0)


def test_relatorio_ignora_transacao_cancelada(test_db):

    create_income(
        "Venda ativa",
        10000,
        "2026-09-01",
    )

    venda_cancelada = create_income(
        "Venda cancelada",
        50000,
        "2026-09-02",
    )

    cancel_transaction(
        venda_cancelada,
        "Teste de cancelamento.",
    )

    create_expense(
        "Material",
        2000,
        "2026-09-03",
    )

    relatorio = get_report_data(
        "2026-09-01",
        "2026-09-03",
    )

    assert relatorio["total_ganhos"] == 10000
    assert relatorio["total_gastos"] == 2000
    assert relatorio["lucro_real"] == 8000

    assert len(relatorio["ganhos"]) == 1


def test_relatorio_respeita_periodo(test_db):

    create_income(
        "Venda fora",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda dentro",
        20000,
        "2026-09-05",
    )

    relatorio = get_report_data(
        start_date="2026-09-03",
        end_date="2026-09-06",
    )

    assert relatorio["total_ganhos"] == 20000
    assert len(relatorio["ganhos"]) == 1
    assert relatorio["ganhos"][0]["descricao"] == "Venda dentro"


def test_relatorio_rejeita_periodo_invertido(test_db):

    with pytest.raises(ValueError):

        get_report_data(
            "2026-09-10",
            "2026-09-01",
        )
        
def test_relatorio_calcula_percentual_dos_gastos(test_db):

    create_expense(
        "Material",
        10000,
        "2026-09-01",
    )

    create_expense(
        "Transporte",
        30000,
        "2026-09-02",
    )

    create_expense(
        "Equipamento",
        60000,
        "2026-09-03",
    )

    relatorio = get_report_data(
        "2026-09-01",
        "2026-09-03",
    )

    gastos = relatorio["gastos"]

    assert len(gastos) == 3

    assert gastos[0]["percentual"] == pytest.approx(10.0)
    assert gastos[1]["percentual"] == pytest.approx(30.0)
    assert gastos[2]["percentual"] == pytest.approx(60.0)
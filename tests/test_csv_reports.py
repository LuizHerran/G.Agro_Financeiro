from app.reports.csv_reports import generate_csv_report
from app.services.transactions import (
    create_income,
    create_expense,
)


def test_gerar_csv(test_db, tmp_path):

    create_income(
        "Venda de camiseta",
        15000,
        "2026-09-01",
    )

    create_income(
        "Venda de calça",
        35000,
        "2026-09-02",
    )

    create_expense(
        "Compra de material",
        10000,
        "2026-09-03",
    )

    output_path = tmp_path / "relatorio.csv"

    result = generate_csv_report(
        "2026-09-01",
        "2026-09-03",
        output_path,
    )

    assert result == output_path
    assert output_path.exists()

    content = output_path.read_text(
        encoding="utf-8-sig"
    )

    assert "RELATÓRIO FINANCEIRO" in content
    assert "Venda de camiseta" in content
    assert "Venda de calça" in content
    assert "Compra de material" in content

    assert "R$ 150,00" in content
    assert "R$ 350,00" in content
    assert "R$ 100,00" in content

    assert "R$ 500,00" in content
    assert "R$ 100,00" in content
    assert "R$ 400,00" in content


def test_csv_calcula_percentuais(test_db, tmp_path):

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

    output_path = tmp_path / "relatorio.csv"

    generate_csv_report(
        "2026-09-01",
        "2026-09-02",
        output_path,
    )

    content = output_path.read_text(
        encoding="utf-8-sig"
    )

    assert "25.00%" in content
    assert "75.00%" in content


def test_csv_ignora_canceladas(
    test_db,
    tmp_path,
):

    from app.services.transactions import (
        cancel_transaction,
    )

    create_income(
        "Venda ativa",
        10000,
        "2026-09-01",
    )

    cancelled_id = create_income(
        "Venda cancelada",
        50000,
        "2026-09-02",
    )

    cancel_transaction(
        cancelled_id,
        "Teste.",
    )

    output_path = tmp_path / "relatorio.csv"

    generate_csv_report(
        "2026-09-01",
        "2026-09-02",
        output_path,
    )

    content = output_path.read_text(
        encoding="utf-8-sig"
    )

    assert "Venda ativa" in content
    assert "Venda cancelada" not in content

    assert "R$ 100,00" in content
    
    assert "01/09/2026" in content
    assert "02/09/2026" in content

    assert "2026-09-01" not in content
    assert "2026-09-02" not in content
    assert "2026-09-03" not in content

    assert "03/09/2026" not in content
    assert "Compra de material" not in content
    
    assert "RESUMO" in content
    assert "Total de ganhos" in content
    assert "Total de gastos" in content
    assert "LUCRO REAL" in content
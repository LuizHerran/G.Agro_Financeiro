from pathlib import Path

from app.utils.logger import logger
from app.reports.history_excel import generate_history_excel
from app.reports.periods import (
    get_weekly_period,
    get_previous_month_period,
)
from app.services.transactions import (
    calculate_summary,
    get_transactions,
)


REPORTS_DIR_NAME = "Controle Financeiro"


def get_reports_dir() -> Path:
    """
    Retorna o diretório oficial onde os relatórios serão salvos.
    """
    documents_dir = Path.home() / "Documents"
    reports_dir = documents_dir / REPORTS_DIR_NAME

    reports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return reports_dir


def _generate_automatic_excel_report(
    start_date: str,
    end_date: str,
    output_path: Path,
) -> Path:
    """
    Gera um relatório Excel automático usando o mesmo gerador
    utilizado pelo botão de exportação do Histórico.
    """

    filters = {
        "start_date": start_date,
        "end_date": end_date,
        "transaction_type": None,
        "description": None,
        "min_value_centavos": None,
        "max_value_centavos": None,
    }

    transactions = get_transactions(
        **filters,
        include_cancelled=True,
    )

    summary = calculate_summary(
        start_date=start_date,
        end_date=end_date,
    )

    generate_history_excel(
        transactions=transactions,
        summary=summary,
        output_path=output_path,
        filters=filters,
    )

    logger.info(
        "Relatório automático criado | arquivo=%s | período=%s a %s",
        output_path,
        start_date,
        end_date,
    )

    return output_path


def generate_weekly_report() -> Path:
    """
    Gera o relatório semanal da semana atual.

    O arquivo é gerado em Excel usando exatamente o mesmo
    formato utilizado na exportação do Histórico.
    """
    start_date, end_date = get_weekly_period()

    output_path = (
        get_reports_dir()
        / f"Relatorio_Semanal_{start_date}_a_{end_date}.xlsx"
    )

    return _generate_automatic_excel_report(
        start_date=start_date,
        end_date=end_date,
        output_path=output_path,
    )


def generate_monthly_report() -> Path:
    """
    Gera o relatório mensal do mês anterior.

    O arquivo é gerado em Excel usando exatamente o mesmo
    formato utilizado na exportação do Histórico.
    """
    start_date, end_date = get_previous_month_period()

    month = start_date[:7]

    output_path = (
        get_reports_dir()
        / f"Relatorio_Mensal_{month}.xlsx"
    )

    return _generate_automatic_excel_report(
        start_date=start_date,
        end_date=end_date,
        output_path=output_path,
    )

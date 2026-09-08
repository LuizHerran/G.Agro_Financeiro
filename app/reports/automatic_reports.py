from pathlib import Path
from app.utils.logger import logger
from app.reports.csv_reports import generate_csv_report
from app.reports.periods import (
    get_weekly_period,
    get_previous_month_period,
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


def generate_weekly_report() -> Path:
    """
    Gera o relatório da semana atual.
    """
    start_date, end_date = get_weekly_period()

    output_path = (
        get_reports_dir()
        / f"Relatorio_Semanal_{start_date}_a_{end_date}.csv"
    )
    
    logger.info(
            "Relatório semanal criado | arquivo=%s | período=%s a %s",
            output_path,
            start_date,
            end_date,
        )

    return generate_csv_report(
        start_date=start_date,
        end_date=end_date,
        output_path=output_path,
    )


def generate_monthly_report() -> Path:
    """
    Gera o relatório do mês anterior.
    """
    start_date, end_date = get_previous_month_period()

    month = start_date[:7]

    output_path = (
        get_reports_dir()
        / f"Relatorio_Mensal_{month}.csv"
    )
    
    logger.info(
        "Relatório mensal criado | arquivo=%s | período=%s a %s",
        output_path,
        start_date,
        end_date,
    )

    return generate_csv_report(
        start_date=start_date,
        end_date=end_date,
        output_path=output_path,
    )
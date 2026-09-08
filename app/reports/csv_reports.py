import csv
from pathlib import Path
from datetime import datetime

from app.services.reports import get_report_data
from app.utils.money import cents_to_money


def format_date(date_value: str) -> str:
    """
    Converte YYYY-MM-DD para DD/MM/YYYY.
    """
    return datetime.strptime(
        date_value,
        "%Y-%m-%d",
    ).strftime("%d/%m/%Y")


def generate_csv_report(
    start_date: str,
    end_date: str,
    output_path: str | Path,
) -> Path:
    """
    Gera um relatório financeiro CSV para o período informado.
    """

    report = get_report_data(
        start_date=start_date,
        end_date=end_date,
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.writer(
            file,
            delimiter=";",
        )

        # ==========================================
        # CABEÇALHO
        # ==========================================

        writer.writerow([
            "RELATÓRIO FINANCEIRO"
        ])

        writer.writerow([
            "Período",
            f"{format_date(start_date)} a "
            f"{format_date(end_date)}",
        ])

        writer.writerow([])

        # ==========================================
        # RESUMO
        # ==========================================

        writer.writerow([
            "RESUMO"
        ])

        writer.writerow([
            "Indicador",
            "Valor",
        ])

        writer.writerow([
            "Total de ganhos",
            cents_to_money(
                report["total_ganhos"]
            ),
        ])

        writer.writerow([
            "Total de gastos",
            cents_to_money(
                report["total_gastos"]
            ),
        ])

        writer.writerow([
            "LUCRO REAL",
            cents_to_money(
                report["lucro_real"]
            ),
        ])

        writer.writerow([])

        # ==========================================
        # GANHOS
        # ==========================================

        writer.writerow([
            "GANHOS"
        ])

        writer.writerow([
            "Data",
            "Descrição",
            "Valor",
            "Participação",
        ])

        for gain in report["ganhos"]:
            writer.writerow([
                format_date(
                    gain["data_transacao"]
                ),
                gain["descricao"],
                cents_to_money(
                    gain["valor_centavos"]
                ),
                f'{gain["percentual"]:.2f}%',
            ])

        writer.writerow([])

        # ==========================================
        # GASTOS
        # ==========================================

        writer.writerow([
            "GASTOS"
        ])

        writer.writerow([
            "Data",
            "Descrição",
            "Valor",
            "Participação",
        ])

        for expense in report["gastos"]:
            writer.writerow([
                format_date(
                    expense["data_transacao"]
                ),
                expense["descricao"],
                cents_to_money(
                    expense["valor_centavos"]
                ),
                f'{expense["percentual"]:.2f}%',
            ])

        writer.writerow([])

        # ==========================================
        # TOTAIS
        # ==========================================

        writer.writerow([
            "TOTAIS"
        ])

        writer.writerow([
            "Total de ganhos",
            cents_to_money(
                report["total_ganhos"]
            ),
        ])

        writer.writerow([
            "Total de gastos",
            cents_to_money(
                report["total_gastos"]
            ),
        ])

        writer.writerow([
            "LUCRO REAL",
            cents_to_money(
                report["lucro_real"]
            ),
        ])

    return output_path
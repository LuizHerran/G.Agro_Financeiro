import csv
from pathlib import Path
from datetime import datetime

from app.utils.money import cents_to_money


def format_date(date_value: str) -> str:
    return datetime.strptime(
        date_value,
        "%Y-%m-%d",
    ).strftime("%d/%m/%Y")


def generate_history_csv(
    transactions: list,
    summary: dict,
    output_path: str | Path,
    filters: dict,
) -> Path:
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

        # Título
        writer.writerow([
            "HISTÓRICO FINANCEIRO"
        ])

        writer.writerow([])

        # Filtros utilizados
        writer.writerow([
            "FILTROS UTILIZADOS"
        ])

        writer.writerow([
            "Data inicial",
            format_date(filters["start_date"])
            if filters["start_date"]
            else "Não informado",
        ])

        writer.writerow([
            "Data final",
            format_date(filters["end_date"])
            if filters["end_date"]
            else "Não informado",
        ])

        writer.writerow([
            "Tipo",
            filters["transaction_type"]
            if filters["transaction_type"]
            else "Todos",
        ])

        writer.writerow([
            "Descrição",
            filters["description"]
            if filters["description"]
            else "Todas",
        ])

        writer.writerow([
            "Valor mínimo",
            cents_to_money(
                filters["min_value_centavos"]
            )
            if filters["min_value_centavos"] is not None
            else "Não informado",
        ])

        writer.writerow([
            "Valor máximo",
            cents_to_money(
                filters["max_value_centavos"]
            )
            if filters["max_value_centavos"] is not None
            else "Não informado",
        ])

        writer.writerow([])

        # Resumo
        writer.writerow([
            "RESUMO"
        ])

        writer.writerow([
            "Total de ganhos",
            cents_to_money(
                summary["total_ganhos"]
            ),
        ])

        writer.writerow([
            "Total de gastos",
            cents_to_money(
                summary["total_gastos"]
            ),
        ])

        writer.writerow([
            "LUCRO REAL",
            cents_to_money(
                summary["lucro_real"]
            ),
        ])

        writer.writerow([])

        # Transações
        writer.writerow([
            "TRANSAÇÕES"
        ])

        writer.writerow([
            "ID",
            "Data",
            "Tipo",
            "Descrição",
            "Valor",
            "Status",
        ])

        for transaction in transactions:
            writer.writerow([
                transaction["id"],
                format_date(
                    transaction["data_transacao"]
                ),
                transaction["tipo"],
                transaction["descricao"],
                cents_to_money(
                    transaction["valor_centavos"]
                ),
                transaction["status"],
            ])

        writer.writerow([])

        # Totais
        writer.writerow([
            "TOTAIS"
        ])

        writer.writerow([
            "Total de ganhos",
            cents_to_money(
                summary["total_ganhos"]
            ),
        ])

        writer.writerow([
            "Total de gastos",
            cents_to_money(
                summary["total_gastos"]
            ),
        ])

        writer.writerow([
            "LUCRO REAL",
            cents_to_money(
                summary["lucro_real"]
            ),
        ])

    return output_path

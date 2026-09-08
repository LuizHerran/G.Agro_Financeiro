from app.database.connection import get_connection
from app.utils.dates import validate_date


def get_report_data( start_date: str, end_date: str, ):
    """
    Retorna os dados financeiros de um período.

    Apenas transações ATIVAS são consideradas.
    """

    if not validate_date(start_date):
        raise ValueError("Data inicial inválida.")

    if not validate_date(end_date):
        raise ValueError("Data final inválida.")

    if start_date > end_date:
        raise ValueError(
            "A data inicial não pode ser maior que a data final."
        )

    with get_connection() as connection:

        gains = connection.execute(
            """
            SELECT
                id,
                descricao,
                valor_centavos,
                data_transacao
            FROM transacoes
            WHERE tipo = 'GANHO'
              AND status = 'ATIVA'
              AND data_transacao >= ?
              AND data_transacao <= ?
            ORDER BY
                data_transacao ASC,
                id ASC
            """,
            (start_date, end_date)
        ).fetchall()

        expenses = connection.execute(
            """
            SELECT
                id,
                descricao,
                valor_centavos,
                data_transacao
            FROM transacoes
            WHERE tipo = 'GASTO'
              AND status = 'ATIVA'
              AND data_transacao >= ?
              AND data_transacao <= ?
            ORDER BY
                data_transacao ASC,
                id ASC
            """,
            (start_date, end_date)
        ).fetchall()

    total_ganhos = sum(
        row["valor_centavos"]
        for row in gains
    )

    total_gastos = sum(
        row["valor_centavos"]
        for row in expenses
    )

    lucro_real = total_ganhos - total_gastos

    ganhos_com_percentual = []

    for gain in gains:

        if total_ganhos > 0:
            percentual = (
                gain["valor_centavos"] * 100
            ) / total_ganhos
        else:
            percentual = 0

        ganhos_com_percentual.append(
            {
                "id": gain["id"],
                "descricao": gain["descricao"],
                "valor_centavos": gain["valor_centavos"],
                "data_transacao": gain["data_transacao"],
                "percentual": percentual,
            }
        )
        
    gastos_com_percentual = []

    for expense in expenses:

        if total_gastos > 0:
            percentual = (
                expense["valor_centavos"] * 100
            ) / total_gastos
        else:
            percentual = 0

        gastos_com_percentual.append(
            {
                "id": expense["id"],
                "descricao": expense["descricao"],
                "valor_centavos": expense["valor_centavos"],
                "data_transacao": expense["data_transacao"],
                "percentual": percentual,
            }
        )

    return {
        "periodo": {
            "inicio": start_date,
            "fim": end_date,
        },
        "ganhos": ganhos_com_percentual,
        "gastos": gastos_com_percentual,
        "total_ganhos": total_ganhos,
        "total_gastos": total_gastos,
        "lucro_real": lucro_real,
    }
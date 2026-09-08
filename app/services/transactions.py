from app.database.connection import get_connection
from app.utils.logger import logger
from app.utils.dates import ( now, validate_date, validate_transaction_date,)


VALID_TYPES = ("GANHO", "GASTO")
VALID_STATUS = ("ATIVA", "CANCELADA")


def create_transaction(
    transaction_type: str,
    description: str,
    value_centavos: int,
    transaction_date: str,
) -> int:

    if transaction_type not in VALID_TYPES:
        raise ValueError("Tipo de transação inválido.")

    description = description.strip()

    if not description:
        raise ValueError("A descrição não pode estar vazia.")

    if len(description) > 255:
        raise ValueError(
            "A descrição não pode ter mais de 255 caracteres."
        )

    if not isinstance(value_centavos, int):
        raise ValueError(
            "O valor deve ser informado em centavos."
        )

    if value_centavos <= 0:
        raise ValueError(
            "O valor deve ser maior que zero."
        )

    if not validate_transaction_date(transaction_date):
        raise ValueError(
        "A data da transação é inválida ou não pode ser futura."
    )

    creation_date = now()

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO transacoes (
                tipo,
                descricao,
                valor_centavos,
                data_transacao,
                data_criacao,
                status
            )
            VALUES (?, ?, ?, ?, ?, 'ATIVA')
            """,
            (
                transaction_type,
                description,
                value_centavos,
                transaction_date,
                creation_date,
            )
        )

        transaction_id = cursor.lastrowid

        connection.execute(
            """
            INSERT INTO logs (
                data_hora,
                acao,
                transacao_id,
                tipo,
                descricao,
                valor_centavos,
                detalhes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                creation_date,
                "CRIACAO",
                transaction_id,
                transaction_type,
                description,
                value_centavos,
                "Transação criada com sucesso.",
            )
        )
        
        logger.info(
            "Transação criada | id=%s | tipo=%s | descrição=%s | valor_centavos=%s | data=%s",
            transaction_id,
            transaction_type,
            description,
            value_centavos,
            transaction_date,
        )

        return transaction_id


def create_income(
    description: str,
    value_centavos: int,
    transaction_date: str,
) -> int:

    return create_transaction(
        transaction_type="GANHO",
        description=description,
        value_centavos=value_centavos,
        transaction_date=transaction_date,
    )


def create_expense(
    description: str,
    value_centavos: int,
    transaction_date: str,
) -> int:

    return create_transaction(
        transaction_type="GASTO",
        description=description,
        value_centavos=value_centavos,
        transaction_date=transaction_date,
    )


def get_transaction(transaction_id: int):
    """
    Retorna uma transação pelo ID.
    """

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT
                id,
                tipo,
                descricao,
                valor_centavos,
                data_transacao,
                data_criacao,
                status
            FROM transacoes
            WHERE id = ?
            """,
            (transaction_id,)
        ).fetchone()

        return row


def get_transactions(
    start_date: str | None = None,
    end_date: str | None = None,
    transaction_type: str | None = None,
    description: str | None = None,
    min_value_centavos: int | None = None,
    max_value_centavos: int | None = None,
    include_cancelled: bool = False,
):
    """
    Retorna transações aplicando os filtros informados.
    """

    if start_date and not validate_date(start_date):
        raise ValueError("Data inicial inválida.")

    if end_date and not validate_date(end_date):
        raise ValueError("Data final inválida.")

    if transaction_type and transaction_type not in VALID_TYPES:
        raise ValueError("Tipo de transação inválido.")

    if min_value_centavos is not None:
        if not isinstance(min_value_centavos, int):
            raise ValueError(
                "O valor mínimo deve ser informado em centavos."
            )

        if min_value_centavos < 0:
            raise ValueError(
                "O valor mínimo não pode ser negativo."
            )

    if max_value_centavos is not None:
        if not isinstance(max_value_centavos, int):
            raise ValueError(
                "O valor máximo deve ser informado em centavos."
            )

        if max_value_centavos < 0:
            raise ValueError(
                "O valor máximo não pode ser negativo."
            )

    if (
        min_value_centavos is not None
        and max_value_centavos is not None
        and min_value_centavos > max_value_centavos
    ):
        raise ValueError(
            "O valor mínimo não pode ser maior que o valor máximo."
        )

    if description is not None:
        description = description.strip()

    query = """
        SELECT
            id,
            tipo,
            descricao,
            valor_centavos,
            data_transacao,
            data_criacao,
            status
        FROM transacoes
        WHERE 1 = 1
    """

    parameters = []

    if not include_cancelled:
        query += " AND status = 'ATIVA'"

    if start_date:
        query += " AND data_transacao >= ?"
        parameters.append(start_date)

    if end_date:
        query += " AND data_transacao <= ?"
        parameters.append(end_date)

    if transaction_type:
        query += " AND tipo = ?"
        parameters.append(transaction_type)

    if description:
        query += " AND descricao LIKE ?"
        parameters.append(f"%{description}%")

    if min_value_centavos is not None:
        query += " AND valor_centavos >= ?"
        parameters.append(min_value_centavos)

    if max_value_centavos is not None:
        query += " AND valor_centavos <= ?"
        parameters.append(max_value_centavos)

    query += """
        ORDER BY
            data_transacao DESC,
            id DESC
    """

    with get_connection() as connection:

        rows = connection.execute(
            query,
            parameters
        ).fetchall()

        return rows


def calculate_summary(
    start_date: str | None = None,
    end_date: str | None = None,
):
    """
    Calcula ganhos, gastos e lucro real.
    """

    if start_date and not validate_date(start_date):
        raise ValueError("Data inicial inválida.")

    if end_date and not validate_date(end_date):
        raise ValueError("Data final inválida.")

    query = """
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN tipo = 'GANHO'
                        THEN valor_centavos
                        ELSE 0
                    END
                ),
                0
            ) AS total_ganhos,

            COALESCE(
                SUM(
                    CASE
                        WHEN tipo = 'GASTO'
                        THEN valor_centavos
                        ELSE 0
                    END
                ),
                0
            ) AS total_gastos

        FROM transacoes

        WHERE status = 'ATIVA'
    """

    parameters = []

    if start_date:
        query += " AND data_transacao >= ?"
        parameters.append(start_date)

    if end_date:
        query += " AND data_transacao <= ?"
        parameters.append(end_date)

    with get_connection() as connection:

        row = connection.execute(
            query,
            parameters
        ).fetchone()

    total_ganhos = row["total_ganhos"]
    total_gastos = row["total_gastos"]
    lucro_real = total_ganhos - total_gastos

    return {
        "total_ganhos": total_ganhos,
        "total_gastos": total_gastos,
        "lucro_real": lucro_real,
    }


def cancel_transaction(
    transaction_id: int,
    reason: str,
) -> None:
    """
    Cancela uma transação sem apagá-la do banco.
    """

    reason = reason.strip()

    if not reason:
        raise ValueError(
            "É necessário informar o motivo do cancelamento."
        )

    with get_connection() as connection:

        transaction = connection.execute(
            """
            SELECT
                id,
                tipo,
                descricao,
                valor_centavos,
                status
            FROM transacoes
            WHERE id = ?
            """,
            (transaction_id,)
        ).fetchone()

        if transaction is None:
            raise ValueError(
                "Transação não encontrada."
            )

        if transaction["status"] == "CANCELADA":
            raise ValueError(
                "Esta transação já está cancelada."
            )

        cancellation_date = now()

        connection.execute(
            """
            UPDATE transacoes
            SET status = 'CANCELADA'
            WHERE id = ?
            """,
            (transaction_id,)
        )

        connection.execute(
            """
            INSERT INTO logs (
                data_hora,
                acao,
                transacao_id,
                tipo,
                descricao,
                valor_centavos,
                detalhes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cancellation_date,
                "CANCELAMENTO",
                transaction["id"],
                transaction["tipo"],
                transaction["descricao"],
                transaction["valor_centavos"],
                reason,
            )
        )
        
        logger.info(
            "Transação cancelada | id=%s | motivo=%s",
            transaction_id,
            reason,
        )


def get_logs(transaction_id: int | None = None):
    """
    Retorna os logs do sistema ou os logs de uma transação específica.
    """

    query = """
        SELECT
            id,
            data_hora,
            acao,
            transacao_id,
            tipo,
            descricao,
            valor_centavos,
            detalhes
        FROM logs
        WHERE 1 = 1
    """

    parameters = []

    if transaction_id is not None:
        query += " AND transacao_id = ?"
        parameters.append(transaction_id)

    query += " ORDER BY data_hora DESC, id DESC"

    with get_connection() as connection:

        return connection.execute(
            query,
            parameters
        ).fetchall()
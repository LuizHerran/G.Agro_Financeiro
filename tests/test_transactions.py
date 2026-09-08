import pytest
from app.database.schema import initialize_database
from app.services.transactions import (
    create_income,
    create_expense,
    create_transaction,
    get_transaction,
    get_transactions,
    calculate_summary,
    cancel_transaction,
    get_logs,
)


def test_criar_ganho(test_db):
    initialize_database()

    transaction_id = create_income(
        "Venda de camiseta",
        15000,
        "2026-09-08",
    )

    transaction = get_transaction(transaction_id)

    assert transaction["tipo"] == "GANHO"
    assert transaction["descricao"] == "Venda de camiseta"
    assert transaction["valor_centavos"] == 15000
    assert transaction["status"] == "ATIVA"


def test_criar_gasto(test_db):
    initialize_database()

    transaction_id = create_expense(
        "Compra de material",
        4050,
        "2026-09-08",
    )

    transaction = get_transaction(transaction_id)

    assert transaction["tipo"] == "GASTO"
    assert transaction["descricao"] == "Compra de material"
    assert transaction["valor_centavos"] == 4050
    assert transaction["status"] == "ATIVA"
    

def test_rejeitar_descricao_com_mais_de_255_caracteres(test_db):
    initialize_database()

    descricao = "A" * 256

    with pytest.raises(
        ValueError,
        match="descrição não pode ter mais de 255 caracteres",
    ):
        create_income(
            descricao,
            1000,
            "2026-09-08",
        )


def test_rejeitar_valor_zero(test_db):
    initialize_database()

    with pytest.raises(ValueError, match="valor deve ser maior que zero"):
        create_income(
            "Venda",
            0,
            "2026-09-08",
        )


def test_rejeitar_valor_negativo(test_db):
    initialize_database()

    with pytest.raises(ValueError, match="valor deve ser maior que zero"):
        create_expense(
            "Material",
            -100,
            "2026-09-08",
        )


def test_rejeitar_valor_que_nao_e_inteiro(test_db):
    initialize_database()

    with pytest.raises(ValueError, match="valor deve ser informado em centavos"):
        create_income(
            "Venda",
            10.50,
            "2026-09-08",
        )


def test_rejeitar_tipo_invalido(test_db):
    initialize_database()

    from app.services.transactions import create_transaction

    with pytest.raises(ValueError, match="Tipo de transação inválido"):
        create_transaction(
            "INVALIDO",
            "Teste",
            1000,
            "2026-09-08",
        )


def test_rejeitar_data_invalida(test_db):
    initialize_database()

    with pytest.raises(
        ValueError,
        match="data da transação é inválida",
    ):
        create_income(
            "Venda",
            1000,
            "2026-99-99",
        )


def test_rejeitar_data_futura(test_db):
    initialize_database()

    with pytest.raises(
        ValueError,
        match="data da transação é inválida",
    ):
        create_income(
            "Venda",
            1000,
            "2026-09-09",
        )


def test_calcular_lucro_real(test_db):
    initialize_database()

    create_income(
        "Venda",
        15000,
        "2026-09-08",
    )

    create_expense(
        "Material",
        4050,
        "2026-09-08",
    )
    
def test_cancelar_transacao(test_db):
    initialize_database()

    transaction_id = create_expense(
        "Compra de material",
        4050,
        "2026-09-08",
    )

    from app.services.transactions import (
        cancel_transaction,
        get_transaction,
    )

    cancel_transaction(
        transaction_id,
        "Compra cancelada pelo cliente.",
    )

    transaction = get_transaction(transaction_id)

    assert transaction["status"] == "CANCELADA"


def test_transacao_cancelada_nao_entra_no_lucro(test_db):
    initialize_database()

    income_id = create_income(
        "Venda",
        15000,
        "2026-09-08",
    )

    expense_id = create_expense(
        "Material",
        4050,
        "2026-09-08",
    )

    from app.services.transactions import cancel_transaction

    cancel_transaction(
        expense_id,
        "Despesa cancelada.",
    )

    summary = calculate_summary()

    assert summary["total_ganhos"] == 15000
    assert summary["total_gastos"] == 0
    assert summary["lucro_real"] == 15000


def test_nao_permitir_cancelamento_duplo(test_db):
    initialize_database()

    transaction_id = create_expense(
        "Compra",
        5000,
        "2026-09-08",
    )

    from app.services.transactions import cancel_transaction

    cancel_transaction(
        transaction_id,
        "Primeiro cancelamento.",
    )

    with pytest.raises(
        ValueError,
        match="já está cancelada",
    ):
        cancel_transaction(
            transaction_id,
            "Segundo cancelamento.",
        )


def test_nao_permitir_cancelar_transacao_inexistente(test_db):
    initialize_database()

    from app.services.transactions import cancel_transaction

    with pytest.raises(
        ValueError,
        match="Transação não encontrada",
    ):
        cancel_transaction(
            999999,
            "Teste.",
        )


def test_nao_permitir_cancelamento_sem_motivo(test_db):
    initialize_database()

    transaction_id = create_expense(
        "Compra",
        5000,
        "2026-09-08",
    )

    from app.services.transactions import cancel_transaction

    with pytest.raises(
        ValueError,
        match="motivo do cancelamento",
    ):
        cancel_transaction(
            transaction_id,
            "",
        )


def test_cancelamento_gera_log(test_db):
    initialize_database()

    transaction_id = create_expense(
        "Compra de material",
        4050,
        "2026-09-08",
    )

    from app.services.transactions import (
        cancel_transaction,
        get_logs,
    )

    cancel_transaction(
        transaction_id,
        "Compra cancelada pelo cliente.",
    )

    logs = get_logs(transaction_id)

    assert len(logs) == 2

    cancellation_log = next(
        log for log in logs
        if log["acao"] == "CANCELAMENTO"
    )

    assert cancellation_log["transacao_id"] == transaction_id
    assert cancellation_log["tipo"] == "GASTO"
    assert cancellation_log["descricao"] == "Compra de material"
    assert cancellation_log["valor_centavos"] == 4050
    assert cancellation_log["detalhes"] == "Compra cancelada pelo cliente."

def test_filtrar_por_tipo(test_db):
    initialize_database()

    create_income(
        "Venda de camiseta",
        15000,
        "2026-09-08",
    )

    create_expense(
        "Compra de material",
        4050,
        "2026-09-08",
    )

    from app.services.transactions import get_transactions

    ganhos = get_transactions(transaction_type="GANHO")
    gastos = get_transactions(transaction_type="GASTO")

    assert len(ganhos) == 1
    assert ganhos[0]["descricao"] == "Venda de camiseta"

    assert len(gastos) == 1
    assert gastos[0]["descricao"] == "Compra de material"


def test_filtrar_por_periodo(test_db):
    initialize_database()

    create_income(
        "Venda 1",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda 2",
        20000,
        "2026-09-05",
    )

    create_income(
        "Venda 3",
        30000,
        "2026-09-08",
    )

    from app.services.transactions import get_transactions

    transactions = get_transactions(
        start_date="2026-09-03",
        end_date="2026-09-07",
    )

    assert len(transactions) == 1
    assert transactions[0]["descricao"] == "Venda 2"


def test_filtrar_por_data_inicial(test_db):
    initialize_database()

    create_income(
        "Venda antiga",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda recente",
        20000,
        "2026-09-08",
    )

    from app.services.transactions import get_transactions

    transactions = get_transactions(
        start_date="2026-09-05",
    )

    assert len(transactions) == 1
    assert transactions[0]["descricao"] == "Venda recente"


def test_filtrar_por_data_final(test_db):
    initialize_database()

    create_income(
        "Venda antiga",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda recente",
        20000,
        "2026-09-08",
    )

    from app.services.transactions import get_transactions

    transactions = get_transactions(
        end_date="2026-09-05",
    )

    assert len(transactions) == 1
    assert transactions[0]["descricao"] == "Venda antiga"


def test_canceladas_nao_aparecem_por_padrao(test_db):
    initialize_database()

    transaction_id = create_expense(
        "Despesa cancelada",
        5000,
        "2026-09-08",
    )

    create_expense(
        "Despesa ativa",
        7000,
        "2026-09-08",
    )

    from app.services.transactions import cancel_transaction, get_transactions

    cancel_transaction(
        transaction_id,
        "Teste de filtro.",
    )

    transactions = get_transactions()

    assert len(transactions) == 1
    assert transactions[0]["descricao"] == "Despesa ativa"


def test_incluir_canceladas_no_historico(test_db):
    initialize_database()

    transaction_id = create_expense(
        "Despesa cancelada",
        5000,
        "2026-09-08",
    )

    create_expense(
        "Despesa ativa",
        7000,
        "2026-09-08",
    )

    from app.services.transactions import cancel_transaction, get_transactions

    cancel_transaction(
        transaction_id,
        "Teste de filtro.",
    )

    transactions = get_transactions(
        include_cancelled=True,
    )

    assert len(transactions) == 2

    statuses = {transaction["status"] for transaction in transactions}

    assert statuses == {"ATIVA", "CANCELADA"}


def test_ordenar_transacoes_por_data_e_id(test_db):
    initialize_database()

    create_income(
        "Venda antiga",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda recente",
        20000,
        "2026-09-08",
    )

    create_income(
        "Outra venda recente",
        30000,
        "2026-09-08",
    )

    from app.services.transactions import get_transactions

    transactions = get_transactions()

    assert transactions[0]["descricao"] == "Outra venda recente"
    assert transactions[1]["descricao"] == "Venda recente"
    assert transactions[2]["descricao"] == "Venda antiga"

def test_filtrar_por_descricao(test_db):
    create_income(
        "Venda de camiseta",
        15000,
        "2026-09-01",
    )

    create_income(
        "Venda de calca",
        20000,
        "2026-09-02",
    )

    create_expense(
        "Compra de material",
        5000,
        "2026-09-03",
    )

    resultados = get_transactions(
        description="camiseta"
    )

    assert len(resultados) == 1
    assert resultados[0]["descricao"] == "Venda de camiseta"


def test_filtrar_por_descricao_parcial(test_db):
    create_income(
        "Venda de camiseta azul",
        15000,
        "2026-09-01",
    )

    resultados = get_transactions(
        description="camiseta"
    )

    assert len(resultados) == 1
    assert resultados[0]["descricao"] == "Venda de camiseta azul"


def test_filtrar_por_valor_minimo(test_db):
    create_income(
        "Venda 1",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda 2",
        20000,
        "2026-09-02",
    )

    create_income(
        "Venda 3",
        30000,
        "2026-09-03",
    )

    resultados = get_transactions(
        min_value_centavos=20000
    )

    assert len(resultados) == 2
    assert resultados[0]["descricao"] == "Venda 3"
    assert resultados[1]["descricao"] == "Venda 2"


def test_filtrar_por_valor_maximo(test_db):
    create_income(
        "Venda 1",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda 2",
        20000,
        "2026-09-02",
    )

    create_income(
        "Venda 3",
        30000,
        "2026-09-03",
    )

    resultados = get_transactions(
        max_value_centavos=20000
    )

    assert len(resultados) == 2
    assert resultados[0]["descricao"] == "Venda 2"
    assert resultados[1]["descricao"] == "Venda 1"


def test_filtrar_por_faixa_de_valor(test_db):
    create_income(
        "Venda 1",
        10000,
        "2026-09-01",
    )

    create_income(
        "Venda 2",
        20000,
        "2026-09-02",
    )

    create_income(
        "Venda 3",
        30000,
        "2026-09-03",
    )

    resultados = get_transactions(
        min_value_centavos=15000,
        max_value_centavos=25000,
    )

    assert len(resultados) == 1
    assert resultados[0]["descricao"] == "Venda 2"


def test_filtro_valor_minimo_maior_que_maximo(test_db):
    with pytest.raises(ValueError):
        get_transactions(
            min_value_centavos=30000,
            max_value_centavos=20000,
        )


def test_criacao_gera_log(test_db):
    initialize_database()

    transaction_id = create_income(
        "Venda de camiseta",
        15000,
        "2026-09-08",
    )

    from app.services.transactions import get_logs

    logs = get_logs(transaction_id)

    assert len(logs) == 1

    log = logs[0]

    assert log["acao"] == "CRIACAO"
    assert log["transacao_id"] == transaction_id
    assert log["tipo"] == "GANHO"
    assert log["descricao"] == "Venda de camiseta"
    assert log["valor_centavos"] == 15000
    assert log["detalhes"] == "Transação criada com sucesso."
    

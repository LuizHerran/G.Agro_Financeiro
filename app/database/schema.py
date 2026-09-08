from app.database.connection import get_connection


def initialize_database() -> None:
    """
    Cria todas as tabelas necessárias para a aplicação.
    """

    with get_connection() as connection:

        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                tipo TEXT NOT NULL
                    CHECK (tipo IN ('GANHO', 'GASTO')),

                descricao TEXT NOT NULL,

                valor_centavos INTEGER NOT NULL
                    CHECK (valor_centavos > 0),

                data_transacao TEXT NOT NULL,

                data_criacao TEXT NOT NULL,

                status TEXT NOT NULL DEFAULT 'ATIVA'
                    CHECK (status IN ('ATIVA', 'CANCELADA'))
            );


            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                data_hora TEXT NOT NULL,

                acao TEXT NOT NULL,

                transacao_id INTEGER,

                tipo TEXT,

                descricao TEXT,

                valor_centavos INTEGER,

                detalhes TEXT,

                FOREIGN KEY (transacao_id)
                    REFERENCES transacoes(id)
            );


            CREATE INDEX IF NOT EXISTS idx_transacoes_data
                ON transacoes(data_transacao);


            CREATE INDEX IF NOT EXISTS idx_transacoes_tipo
                ON transacoes(tipo);


            CREATE INDEX IF NOT EXISTS idx_logs_transacao
                ON logs(transacao_id);


            CREATE INDEX IF NOT EXISTS idx_logs_data
                ON logs(data_hora);
            """
        )
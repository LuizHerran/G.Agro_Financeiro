from datetime import date, datetime

DATE_FORMAT = "%Y-%m-%d"
BRAZIL_DATE_FORMAT = "%d/%m/%Y"

def today() -> str:
    return date.today().strftime(DATE_FORMAT)


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")

def today_brazil() -> str:
    return date.today().strftime(BRAZIL_DATE_FORMAT)

def validate_date(value: str) -> bool:
    try:
        datetime.strptime(value, DATE_FORMAT)
        return True
    except ValueError:
        return False


def validate_transaction_date(value: str) -> bool:
    """
    Valida se a data da transação existe e não é futura.
    """
    try:
        transaction_date = datetime.strptime(
            value,
            DATE_FORMAT,
        ).date()
    except ValueError:
        return False

    return transaction_date <= date.today()


def brazil_date_to_database(value: str) -> str:
    """
    Converte DD/MM/YYYY para YYYY-MM-DD.
    """
    try:
        parsed_date = datetime.strptime(
            value,
            BRAZIL_DATE_FORMAT,
        )
    except ValueError:
        raise ValueError(
            "Data inválida. Use o formato DD/MM/AAAA."
        )

    return parsed_date.strftime(DATE_FORMAT)


def database_date_to_brazil(value: str) -> str:    
    """
    Converte YYYY-MM-DD para DD/MM/YYYY.
    """
    try:
        parsed_date = datetime.strptime(
            value,
            DATE_FORMAT,
        )
    except ValueError:
        raise ValueError(
            "Data inválida."
        )

    BRAZIL_DATE_FORMAT = "%d/%m/%Y"
    
    
    def brazil_date_to_database(value: str) -> str:
        """
        Converte DD/MM/YYYY para YYYY-MM-DD.
        """
        try:
            parsed_date = datetime.strptime(
                value,
                BRAZIL_DATE_FORMAT,
            )
        except ValueError:
            raise ValueError(
                "Data inválida. Use o formato DD/MM/AAAA."
            )

        return parsed_date.strftime(DATE_FORMAT)


    def database_date_to_brazil(value: str) -> str:
        """
        Converte YYYY-MM-DD para DD/MM/YYYY.
        """
        try:
            parsed_date = datetime.strptime(
                value,
                DATE_FORMAT,
            )
        except ValueError:
            raise ValueError("Data inválida.")

        return parsed_date.strftime(BRAZIL_DATE_FORMAT)


    def today_brazil() -> str:
        """
        Retorna a data atual no formato brasileiro.
        """
        return date.today().strftime(BRAZIL_DATE_FORMAT)

    return parsed_date.strftime(BRAZIL_DATE_FORMAT)
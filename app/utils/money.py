from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def parse_money(value: str) -> int:
    """
    Converte um valor monetário para centavos.

    Exemplos:
        "10"      -> 1000
        "10,50"   -> 1050
        "10.50"   -> 1050
        "R$ 10,50" -> 1050
    """

    if not isinstance(value, str):
        raise ValueError("O valor precisa ser informado como texto.")

    value = value.strip()

    if not value:
        raise ValueError("O valor não pode estar vazio.")

    value = (
        value
        .replace("R$", "")
        .replace(" ", "")
    )

    # Aceita formato brasileiro: 1.234,56
    if "," in value:
        value = value.replace(".", "")
        value = value.replace(",", ".")

    try:
        amount = Decimal(value)
    except InvalidOperation:
        raise ValueError("Valor monetário inválido.")

    if amount <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    amount = amount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    return int(amount * 100)


def cents_to_money(value_centavos: int) -> str:
    """
    Converte centavos para uma representação monetária brasileira.
    """

    reais = value_centavos // 100
    centavos = value_centavos % 100

    return f"R$ {reais:,}.{centavos:02d}".replace(",", "X").replace(".", ",").replace("X", ".")
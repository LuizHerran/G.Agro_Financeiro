from datetime import date, timedelta


DATE_FORMAT = "%Y-%m-%d"


def get_weekly_period(reference_date: date | None = None):
    """
    Retorna o período da semana que contém a data informada.

    A semana começa na segunda-feira e termina no domingo.
    """

    if reference_date is None:
        reference_date = date.today()

    monday = reference_date - timedelta(
        days=reference_date.weekday()
    )

    sunday = monday + timedelta(days=6)

    return (
        monday.strftime(DATE_FORMAT),
        sunday.strftime(DATE_FORMAT),
    )


def get_previous_month_period(
    reference_date: date | None = None,
):
    """
    Retorna o primeiro e o último dia do mês anterior.
    """

    if reference_date is None:
        reference_date = date.today()

    first_day_current_month = reference_date.replace(
        day=1
    )

    last_day_previous_month = (
        first_day_current_month
        - timedelta(days=1)
    )

    first_day_previous_month = (
        last_day_previous_month.replace(day=1)
    )

    return (
        first_day_previous_month.strftime(DATE_FORMAT),
        last_day_previous_month.strftime(DATE_FORMAT),
    )
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
    
def get_current_month_period(
    reference_date: date | None = None,
):
    if reference_date is None:
        reference_date = date.today()

    first_day = reference_date.replace(day=1)

    if reference_date.month == 12:
        next_month = reference_date.replace(
            year=reference_date.year + 1,
            month=1,
            day=1,
        )
    else:
        next_month = reference_date.replace(
            month=reference_date.month + 1,
            day=1,
        )

    last_day = next_month - timedelta(days=1)

    return (
        first_day.strftime(DATE_FORMAT),
        last_day.strftime(DATE_FORMAT),
    )
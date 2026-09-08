from datetime import date

from app.reports.periods import (
    get_weekly_period,
    get_previous_month_period,
)


def test_periodo_semanal():

    inicio, fim = get_weekly_period(
        date(2026, 9, 8)
    )

    assert inicio == "2026-09-07"
    assert fim == "2026-09-13"


def test_periodo_semanal_quando_data_e_domingo():

    inicio, fim = get_weekly_period(
        date(2026, 9, 13)
    )

    assert inicio == "2026-09-07"
    assert fim == "2026-09-13"


def test_periodo_semanal_quando_data_e_segunda():

    inicio, fim = get_weekly_period(
        date(2026, 9, 7)
    )

    assert inicio == "2026-09-07"
    assert fim == "2026-09-13"


def test_periodo_mes_anterior():

    inicio, fim = get_previous_month_period(
        date(2026, 9, 8)
    )

    assert inicio == "2026-08-01"
    assert fim == "2026-08-31"


def test_periodo_mes_anterior_em_janeiro():

    inicio, fim = get_previous_month_period(
        date(2026, 1, 15)
    )

    assert inicio == "2025-12-01"
    assert fim == "2025-12-31"


def test_periodo_mes_anterior_com_fevereiro():

    inicio, fim = get_previous_month_period(
        date(2026, 3, 10)
    )

    assert inicio == "2026-02-01"
    assert fim == "2026-02-28"
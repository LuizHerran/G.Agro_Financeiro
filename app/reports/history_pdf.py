from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

from app.utils.dates import database_date_to_brazil
from app.utils.money import cents_to_money


def generate_history_pdf(
    transactions,
    summary,
    output_path,
    filters,
):
    output_path = Path(output_path)

    # =========================================================
    # CONFIGURAÇÃO DA PÁGINA
    # =========================================================

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.white,
        alignment=TA_CENTER,
    )

    period_style = ParagraphStyle(
        "PeriodCustom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=TA_CENTER,
    )

    section_style = ParagraphStyle(
        "SectionCustom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
    )

    center_style = ParagraphStyle(
        "CenterCustom",
        parent=normal_style,
        alignment=TA_CENTER,
    )

    right_style = ParagraphStyle(
        "RightCustom",
        parent=normal_style,
        alignment=TA_RIGHT,
    )

    bold_style = ParagraphStyle(
        "BoldCustom",
        parent=normal_style,
        fontName="Helvetica-Bold",
    )

    # =========================================================
    # CORES
    # =========================================================

    title_color = colors.HexColor("#1F4E78")
    section_color = colors.HexColor("#D9EAF7")
    header_color = colors.HexColor("#5B9BD5")
    total_color = colors.HexColor("#E2F0D9")
    cancelled_color = colors.HexColor("#FCE4D6")
    border_color = colors.HexColor("#D9E1F2")

    # =========================================================
    # PERÍODO
    # =========================================================

    period_text = "Período: "

    if filters.get("start_date"):
        period_text += database_date_to_brazil(
            filters["start_date"]
        )
    else:
        period_text += "Início"

    period_text += " até "

    if filters.get("end_date"):
        period_text += database_date_to_brazil(
            filters["end_date"]
        )
    else:
        period_text += "Fim"

    # =========================================================
    # ELEMENTOS DO PDF
    # =========================================================

    elements = []

    # =========================================================
    # TÍTULO
    # =========================================================

    title_table = Table(
        [[Paragraph("CONTROLE FINANCEIRO", title_style)]],
        colWidths=[273 * mm],
        rowHeights=[12 * mm],
    )

    title_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    title_color,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    elements.append(title_table)

    # =========================================================
    # PERÍODO
    # =========================================================

    period_table = Table(
        [[Paragraph(period_text, period_style)]],
        colWidths=[273 * mm],
        rowHeights=[8 * mm],
    )

    period_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    title_color,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    elements.append(period_table)

    # =========================================================
    # TRANSAÇÕES
    # =========================================================

    section_table = Table(
        [[Paragraph("TRANSAÇÕES", section_style)]],
        colWidths=[273 * mm],
        rowHeights=[8 * mm],
    )

    section_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    section_color,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    elements.append(section_table)

    # =========================================================
    # CABEÇALHO
    # =========================================================

    headers = [
        "ID",
        "Tipo",
        "Data",
        "Descrição",
        "Valor",
        "% do total",
        "Status",
    ]

    table_data = [
        [
            Paragraph(header, center_style)
            for header in headers
        ]
    ]

    # =========================================================
    # VALORES DO RESUMO
    # =========================================================

    total_ganhos = summary["total_ganhos"]
    total_gastos = summary["total_gastos"]

    fluxo_total = total_ganhos + total_gastos

    # =========================================================
    # TRANSAÇÕES
    # =========================================================

    for transaction in transactions:
        transaction_type = transaction["tipo"]
        status = transaction["status"]
        value_centavos = transaction["valor_centavos"]

        # Percentual
        if status == "CANCELADA":
            percentage = "—"

        elif transaction_type == "GANHO":
            if total_ganhos > 0:
                percentage = (
                    f"{value_centavos / total_ganhos * 100:.2f}%"
                )
            else:
                percentage = "0.00%"

        else:
            if total_gastos > 0:
                percentage = (
                    f"{value_centavos / total_gastos * 100:.2f}%"
                )
            else:
                percentage = "0.00%"

        table_data.append(
            [
                Paragraph(
                    str(transaction["id"]),
                    center_style,
                ),
                Paragraph(
                    transaction_type,
                    center_style,
                ),
                Paragraph(
                    database_date_to_brazil(
                        transaction["data_transacao"]
                    ),
                    center_style,
                ),
                Paragraph(
                    str(transaction["descricao"]),
                    normal_style,
                ),
                Paragraph(
                    cents_to_money(value_centavos),
                    right_style,
                ),
                Paragraph(
                    percentage,
                    right_style,
                ),
                Paragraph(
                    status,
                    center_style,
                ),
            ]
        )

    # =========================================================
    # TABELA DE TRANSAÇÕES
    # =========================================================

    transaction_table = Table(
        table_data,
        colWidths=[
            15 * mm,
            25 * mm,
            25 * mm,
            91 * mm,
            30 * mm,
            30 * mm,
            35 * mm,
        ],
        repeatRows=1,
    )

    transaction_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    header_color,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    border_color,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (2, -1),
                    "CENTER",
                ),
                (
                    "ALIGN",
                    (4, 1),
                    (5, -1),
                    "RIGHT",
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F8FBFD"),
                    ],
                ),
            ]
        )
    )

    # =========================================================
    # DESTACAR CANCELADAS
    # =========================================================

    for index, transaction in enumerate(
        transactions,
        start=1,
    ):
        if transaction["status"] == "CANCELADA":
            transaction_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, index),
                            (-1, index),
                            cancelled_color,
                        ),
                    ]
                )
            )

    elements.append(transaction_table)

    # =========================================================
    # RESUMO
    # =========================================================

    elements.append(Spacer(1, 4 * mm))

    resumo_table = Table(
        [[Paragraph("RESUMO", section_style)]],
        colWidths=[273 * mm],
        rowHeights=[8 * mm],
    )

    resumo_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    section_color,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    elements.append(resumo_table)

    # =========================================================
    # RESUMO FINANCEIRO
    # =========================================================

    ganhos_row = [
        Paragraph("Ganhos", bold_style),
        Paragraph(
            cents_to_money(total_ganhos),
            right_style,
        ),
        "",
        Paragraph("FLUXO TOTAL", bold_style),
        Paragraph(
            cents_to_money(fluxo_total),
            right_style,
        ),
    ]

    gastos_row = [
        Paragraph("Gastos", bold_style),
        Paragraph(
            cents_to_money(total_gastos),
            right_style,
        ),
        "",
        "",
        "",
    ]

    lucro_row = [
        Paragraph("Lucro real", bold_style),
        Paragraph(
            cents_to_money(summary["lucro_real"]),
            right_style,
        ),
        "",
        "",
        "",
    ]

    summary_table = Table(
        [
            ganhos_row,
            gastos_row,
            lucro_row,
        ],
        colWidths=[
            35 * mm,
            35 * mm,
            35 * mm,
            65 * mm,
            50 * mm,
        ],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (1, -1),
                    0.5,
                    border_color,
                ),
                (
                    "GRID",
                    (3, 0),
                    (4, 0),
                    0.5,
                    border_color,
                ),
                (
                    "BACKGROUND",
                    (3, 0),
                    (4, 0),
                    total_color,
                ),
                (
                    "BACKGROUND",
                    (0, 2),
                    (1, 2),
                    total_color,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "ALIGN",
                    (4, 0),
                    (4, 0),
                    "RIGHT",
                ),
            ]
        )
    )

    elements.append(summary_table)

    # =========================================================
    # GERAR PDF
    # =========================================================

    document.build(elements)
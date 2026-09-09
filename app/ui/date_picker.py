import calendar
from datetime import date

import customtkinter as ctk

MONTHS = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]

WEEKDAYS = [
    "Seg",
    "Ter",
    "Qua",
    "Qui",
    "Sex",
    "Sáb",
    "Dom",
]

class DatePicker(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        initial_date=None,
        on_select=None,
    ):
        super().__init__(
            parent,
            width=360,
            height=380,
            corner_radius=12,
            border_width=1,
        )

        self.on_select = on_select

        if initial_date is None:
            self.selected_date = date.today()
        else:
            self.selected_date = initial_date

        self.current_year = self.selected_date.year
        self.current_month = self.selected_date.month

        self._create_widgets()
        self._draw_calendar()

    def _create_widgets(self):

        # =========================
        # Cabeçalho
        # =========================

        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        header.pack(
            fill="x",
            padx=15,
            pady=(15, 10),
        )

        header.grid_columnconfigure(
            1,
            weight=1,
        )

        previous_button = ctk.CTkButton(
            header,
            text="‹",
            width=40,
            command=self._previous_month,
        )

        previous_button.grid(
            row=0,
            column=0,
            padx=5,
        )

        self.month_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        self.month_label.grid(
            row=0,
            column=1,
            padx=5,
        )

        next_button = ctk.CTkButton(
            header,
            text="›",
            width=40,
            command=self._next_month,
        )

        next_button.grid(
            row=0,
            column=2,
            padx=5,
        )

        # =========================
        # Calendário
        # =========================

        self.calendar_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.calendar_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5,
        )

        for column, weekday in enumerate(WEEKDAYS):

            self.calendar_frame.grid_columnconfigure(
                column,
                weight=1,
            )

            label = ctk.CTkLabel(
                self.calendar_frame,
                text=weekday,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold",
                ),
            )

            label.grid(
                row=0,
                column=column,
                padx=2,
                pady=(5, 8),
            )

        # =========================
        # Rodapé
        # =========================

        footer = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        footer.pack(
            fill="x",
            padx=15,
            pady=(5, 15),
        )

        today_button = ctk.CTkButton(
            footer,
            text="Hoje",
            width=90,
            command=self._select_today,
        )

        today_button.pack(
            side="left",
        )

        close_button = ctk.CTkButton(
            footer,
            text="Fechar",
            width=90,
            fg_color="transparent",
            border_width=1,
            command=self._close,
        )

        close_button.pack(
            side="right",
        )

    def _draw_calendar(self):

        # Remove somente os dias.
        for widget in self.calendar_frame.winfo_children():

            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        self.month_label.configure(
            text=(
                f"{MONTHS[self.current_month - 1]} "
                f"{self.current_year}"
            )
        )

        month_calendar = calendar.monthcalendar(
            self.current_year,
            self.current_month,
        )

        for row_index, week in enumerate(
            month_calendar,
            start=1,
        ):

            for column_index, day in enumerate(week):

                if day == 0:
                    continue

                current_day = date(
                    self.current_year,
                    self.current_month,
                    day,
                )

                is_selected = (
                    current_day == self.selected_date
                )

                if is_selected:
                    fg_color = (
                        "#3B8ED0",
                        "#1F6AA5",
                    )
                else:
                    fg_color = "transparent"

                is_future = current_day > date.today()

                button = ctk.CTkButton(
                    self.calendar_frame,
                    text=str(day),
                    width=38,
                    height=35,
                    fg_color=fg_color,
                    state="disabled" if is_future else "normal",
                    command=lambda d=current_day: (
                        self._select_date(d)
                    ),
                )

                button.grid(
                    row=row_index,
                    column=column_index,
                    padx=2,
                    pady=2,
                    sticky="nsew",
                )

    def _previous_month(self):

        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

        self._draw_calendar()

    def _next_month(self):

        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

        self._draw_calendar()

    def _select_date(self, selected_date):

        self.selected_date = selected_date

        if self.on_select:
            self.on_select(selected_date)

        self._close()

    def _select_today(self):

        today = date.today()

        self.selected_date = today

        if self.on_select:
            self.on_select(today)

        self._close()

    def _close(self):
        self.destroy()
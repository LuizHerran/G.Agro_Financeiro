from datetime import date
from pathlib import Path

import customtkinter as ctk
from PIL import Image

from app.services.transactions import ( create_expense, create_income,)
from app.ui.date_picker import DatePicker
from app.utils.dates import ( brazil_date_to_database, today_brazil,)
from app.utils.money import parse_money


class TransactionForm(ctk.CTkFrame):
    def __init__( self, parent, transaction_type: str, on_back,):
        self.transaction_type = transaction_type
        self.on_back = on_back

        assets_dir = Path(__file__).resolve().parent / "assets"

        self.calendar_icon = ctk.CTkImage(
            light_image=Image.open(
                assets_dir / "calendar.png"
            ),
            dark_image=Image.open(
                assets_dir / "calendar.png"
            ),
            size=(20, 20),
        )

        super().__init__(parent)

        if transaction_type not in ("GANHO", "GASTO"):
            raise ValueError("Tipo de transação inválido.")

        self.transaction_type = transaction_type
        self.on_back = on_back

        if transaction_type == "GANHO":
            title = "Registrar Ganho"
        else:
            title = "Registrar Gasto"

        self._create_widgets(title)

    def _open_date_picker(self):

        initial_date = date.today()

        value = self.date_entry.get().strip()

        if value:
            try:
                initial_date = date.fromisoformat(
                    brazil_date_to_database(value)
                )
            except ValueError:
                initial_date = date.today()

        picker = DatePicker(
            self,
            initial_date=initial_date,
            on_select=self._set_date,
        )

        picker.place(
            relx=0.5,
            rely=0.55,
            anchor="center",
        )

        self._date_picker = picker

    def _set_date(self, selected_date):

        if selected_date > date.today():
            self._show_message(
                "A data não pode ser futura."
            )
            return

        self.date_entry.delete(
            0,
            "end",
        )

        self.date_entry.insert(
            0,
            selected_date.strftime("%d/%m/%Y"),
        )

    def _create_widgets(self, title: str):
        self.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )
        title_label.grid(
            row=0,
            column=0,
            padx=30,
            pady=(30, 20),
        )

        description_label = ctk.CTkLabel(
            self,
            text="Descrição",
        )
        description_label.grid(
            row=1,
            column=0,
            padx=30,
            pady=(5, 5),
            sticky="w",
        )

        self.description_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ex.: Venda de produto",
            height=40,
        )
        self.description_entry.grid(
            row=2,
            column=0,
            padx=30,
            pady=(0, 15),
            sticky="ew",
        )

        value_label = ctk.CTkLabel(
            self,
            text="Valor",
        )
        value_label.grid(
            row=3,
            column=0,
            padx=30,
            pady=(5, 5),
            sticky="w",
        )

        self.value_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ex.: 150,00",
            height=40,
        )
        self.value_entry.grid(
            row=4,
            column=0,
            padx=30,
            pady=(0, 15),
            sticky="ew",
        )

        date_label = ctk.CTkLabel(
            self,
            text="Data",
        )
        date_label.grid(
            row=5,
            column=0,
            padx=30,
            pady=(5, 5),
            sticky="w",
        )

        date_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        date_frame.grid(
            row=6,
            column=0,
            padx=30,
            pady=(0, 15),
            sticky="ew",
        )

        date_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        self.date_entry = ctk.CTkEntry(
            date_frame,
            height=40,
        )

        self.date_entry.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        calendar_button = ctk.CTkButton(
            date_frame,
            text="",
            image=self.calendar_icon,
            width=45,
            height=40,
            command=self._open_date_picker,
        )

        calendar_button.grid(
            row=0,
            column=1,
            padx=(8, 0),
        )

        self.date_entry.insert(
            0,
            today_brazil(),
        )

        self.message_label = ctk.CTkLabel(
            self,
            text="",
        )
        self.message_label.grid(
            row=7,
            column=0,
            padx=30,
            pady=(5, 10),
        )

        self.add_button = ctk.CTkButton(
            self,
            text="Adicionar",
            height=45,
            command=self._add_transaction,
        )
        self.add_button.grid(
            row=8,
            column=0,
            padx=30,
            pady=(5, 10),
            sticky="ew",
        )

        self.back_button = ctk.CTkButton(
            self,
            text="← Voltar",
            height=40,
            fg_color="transparent",
            border_width=1,
            command=self.on_back,
        )
        self.back_button.grid(
            row=9,
            column=0,
            padx=30,
            pady=(5, 30),
            sticky="ew",
        )

        self.description_entry.focus()

    def _add_transaction(self):
        description = self.description_entry.get().strip()
        value = self.value_entry.get().strip()
        transaction_date = self.date_entry.get().strip()

        try:
            transaction_date = brazil_date_to_database(
                transaction_date
            )
        except ValueError as error:
            self._show_message(str(error))
            return

        try:
            value_centavos = parse_money(value)

            if self.transaction_type == "GANHO":
                create_income(
                    description=description,
                    value_centavos=value_centavos,
                    transaction_date=transaction_date,
                )
            else:
                create_expense(
                    description=description,
                    value_centavos=value_centavos,
                    transaction_date=transaction_date,
                )

        except ValueError as error:
            self._show_message(str(error))
            return

        except Exception:
            self._show_message(
                "Não foi possível registrar a transação."
            )
            return

        self._show_message(
            f"{description} registrada com sucesso."
        )

        self.description_entry.delete(0, "end")
        self.value_entry.delete(0, "end")

        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, today_brazil())

        self.description_entry.focus()

    def _show_message(self, message: str):
        self.message_label.configure(
            text=message,
        )
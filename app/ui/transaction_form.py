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
        # Cores da identidade visual G.Agro
        background = "#F4F1E8"
        dark_green = "#173A24"
        green = "#3F7D3A"
        light_green = "#6FAF45"
        yellow = "#D9A441"
        text_color = "#1E241F"

        card_background = "#E8E5DA"
        input_background = "#FFFFFF"
        border_color = "#C8C5BA"

        self.configure(
            fg_color=background,
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Área central do formulário
        form_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        form_container.grid(
            row=0,
            column=0,
            padx=40,
            pady=30,
            sticky="nsew",
        )

        form_container.grid_columnconfigure(0, weight=1)

        # Título
        title_label = ctk.CTkLabel(
            form_container,
            text=title,
            text_color=dark_green,
            font=ctk.CTkFont(
                size=30,
                weight="bold",
            ),
        )

        title_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(10, 5),
        )

        # Subtítulo
        subtitle = (
            "Informe os dados abaixo para registrar a movimentação."
        )

        subtitle_label = ctk.CTkLabel(
            form_container,
            text=subtitle,
            text_color=text_color,
            font=ctk.CTkFont(
                size=14,
            ),
        )

        subtitle_label.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
        )

        # Cartão do formulário
        form_card = ctk.CTkFrame(
            form_container,
            fg_color=card_background,
            corner_radius=15,
            border_width=1,
            border_color=border_color,
        )

        form_card.grid(
            row=2,
            column=0,
            padx=20,
            pady=5,
            sticky="ew",
        )

        form_card.grid_columnconfigure(0, weight=1)

        # -------------------------
        # DESCRIÇÃO
        # -------------------------

        description_label = ctk.CTkLabel(
            form_card,
            text="Descrição",
            text_color=text_color,
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
        )

        description_label.grid(
            row=0,
            column=0,
            padx=25,
            pady=(25, 6),
            sticky="w",
        )

        self.description_entry = ctk.CTkEntry(
            form_card,
            placeholder_text="Ex.: Venda de produto",
            height=45,
            corner_radius=8,
            border_width=1,
            border_color=border_color,
            fg_color=input_background,
            text_color=text_color,
            font=ctk.CTkFont(
                size=14,
            ),
        )

        self.description_entry.grid(
            row=1,
            column=0,
            padx=25,
            pady=(0, 15),
            sticky="ew",
        )

        # -------------------------
        # VALOR
        # -------------------------

        value_label = ctk.CTkLabel(
            form_card,
            text="Valor",
            text_color=text_color,
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
        )

        value_label.grid(
            row=2,
            column=0,
            padx=25,
            pady=(5, 6),
            sticky="w",
        )

        self.value_entry = ctk.CTkEntry(
            form_card,
            placeholder_text="Ex.: 150,00",
            height=45,
            corner_radius=8,
            border_width=1,
            border_color=border_color,
            fg_color=input_background,
            text_color=text_color,
            font=ctk.CTkFont(
                size=14,
            ),
        )

        self.value_entry.grid(
            row=3,
            column=0,
            padx=25,
            pady=(0, 15),
            sticky="ew",
        )

        # -------------------------
        # DATA
        # -------------------------

        date_label = ctk.CTkLabel(
            form_card,
            text="Data",
            text_color=text_color,
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
        )

        date_label.grid(
            row=4,
            column=0,
            padx=25,
            pady=(5, 6),
            sticky="w",
        )

        date_frame = ctk.CTkFrame(
            form_card,
            fg_color="transparent",
        )

        date_frame.grid(
            row=5,
            column=0,
            padx=25,
            pady=(0, 20),
            sticky="ew",
        )

        date_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        self.date_entry = ctk.CTkEntry(
            date_frame,
            height=45,
            corner_radius=8,
            border_width=1,
            border_color=border_color,
            fg_color=input_background,
            text_color=text_color,
            font=ctk.CTkFont(
                size=14,
            ),
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
            width=48,
            height=45,
            corner_radius=8,
            fg_color="#3F7D3A",
            hover_color="#6FAF45",
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

        # -------------------------
        # MENSAGEM
        # -------------------------

        self.message_label = ctk.CTkLabel(
            form_card,
            text="",
            text_color=green,
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
        )

        self.message_label.grid(
            row=6,
            column=0,
            padx=25,
            pady=(0, 5),
        )

        # -------------------------
        # ADICIONAR
        # -------------------------

        self.add_button = ctk.CTkButton(
            form_card,
            text="Adicionar",
            height=48,
            corner_radius=8,
            fg_color="#3F7D3A",
            hover_color="#6FAF45",
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
            command=self._add_transaction,
        )

        self.add_button.grid(
            row=7,
            column=0,
            padx=25,
            pady=(5, 10),
            sticky="ew",
        )

        # -------------------------
        # VOLTAR
        # -------------------------

        self.back_button = ctk.CTkButton(
            form_card,
            text="← Voltar",
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#E8E5DA",
            border_width=1,
            border_color="#C8C5BA",
            text_color=dark_green,
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            command=self.on_back,
        )

        self.back_button.grid(
            row=8,
            column=0,
            padx=25,
            pady=(0, 25),
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
import customtkinter as ctk

from app.utils.dates import ( brazil_date_to_database, database_date_to_brazil,)

from app.services.transactions import ( calculate_summary, cancel_transaction, get_transactions,)
from app.utils.money import ( cents_to_money, parse_money,)

class HistoryView(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent)

        self.on_back = on_back

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._create_header()
        self._create_filters()
        self._create_summary()
        self._create_transactions()

        self._load_data()

    def _create_header(self):
        header = ctk.CTkFrame(self)
        header.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="ew",
        )

        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Histórico",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )
        title.grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="w",
        )

        back_button = ctk.CTkButton(
            header,
            text="← Voltar",
            command=self.on_back,
        )
        back_button.grid(
            row=0,
            column=1,
            padx=15,
            pady=15,
        )

    def _create_filters(self):
        filters = ctk.CTkFrame(self)
        filters.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="ew",
        )

        filters.grid_columnconfigure(1, weight=1)
        filters.grid_columnconfigure(3, weight=1)
        filters.grid_columnconfigure(5, weight=1)

        # Data inicial
        start_label = ctk.CTkLabel(
            filters,
            text="Data inicial",
        )
        start_label.grid(
            row=0,
            column=0,
            padx=(10, 5),
            pady=(10, 5),
            sticky="w",
        )

        self.start_date_entry = ctk.CTkEntry(
            filters,
            placeholder_text="DD/MM/AAAA",
        )
        self.start_date_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=(10, 5),
            sticky="ew",
        )

        # Data final
        end_label = ctk.CTkLabel(
            filters,
            text="Data final",
        )
        end_label.grid(
            row=0,
            column=2,
            padx=(10, 5),
            pady=(10, 5),
            sticky="w",
        )

        self.end_date_entry = ctk.CTkEntry(
            filters,
            placeholder_text="DD/MM/AAAA",
        )
        self.end_date_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=(10, 5),
            sticky="ew",
        )

        # Tipo
        type_label = ctk.CTkLabel(
            filters,
            text="Tipo",
        )
        type_label.grid(
            row=0,
            column=4,
            padx=(10, 5),
            pady=(10, 5),
            sticky="w",
        )

        self.type_combobox = ctk.CTkComboBox(
            filters,
            values=[
                "Todos",
                "GANHO",
                "GASTO",
            ],
        )
        self.type_combobox.grid(
            row=0,
            column=5,
            padx=(5, 10),
            pady=(10, 5),
            sticky="ew",
        )
        self.type_combobox.set("Todos")

        # Descrição
        description_label = ctk.CTkLabel(
            filters,
            text="Descrição",
        )
        description_label.grid(
            row=1,
            column=0,
            padx=(10, 5),
            pady=5,
            sticky="w",
        )

        self.description_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Pesquisar descrição",
        )
        self.description_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew",
        )

        # Valor mínimo
        min_value_label = ctk.CTkLabel(
            filters,
            text="Valor mínimo",
        )
        min_value_label.grid(
            row=1,
            column=2,
            padx=(10, 5),
            pady=5,
            sticky="w",
        )

        self.min_value_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Ex.: 50,00",
        )
        self.min_value_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
            sticky="ew",
        )

        # Valor máximo
        max_value_label = ctk.CTkLabel(
            filters,
            text="Valor máximo",
        )
        max_value_label.grid(
            row=1,
            column=4,
            padx=(10, 5),
            pady=5,
            sticky="w",
        )

        self.max_value_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Ex.: 500,00",
        )
        self.max_value_entry.grid(
            row=1,
            column=5,
            padx=(5, 10),
            pady=5,
            sticky="ew",
        )

        # Botões
        buttons_frame = ctk.CTkFrame(
            filters,
            fg_color="transparent",
        )
        buttons_frame.grid(
            row=2,
            column=0,
            columnspan=6,
            padx=10,
            pady=(5, 10),
            sticky="e",
        )

        filter_button = ctk.CTkButton(
            buttons_frame,
            text="Filtrar",
            width=120,
            command=self._apply_filters,
        )
        filter_button.pack(
            side="left",
            padx=5,
        )

        clear_button = ctk.CTkButton(
            buttons_frame,
            text="Limpar filtros",
            width=120,
            command=self._clear_filters,
        )
        clear_button.pack(
            side="left",
            padx=5,
        )

    def _create_summary(self):
        self.summary_frame = ctk.CTkFrame(self)
        self.summary_frame.grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.summary_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1,
        )

        self.gains_label = ctk.CTkLabel(
            self.summary_frame,
            text="Ganhos: R$ 0,00",
        )
        self.gains_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=15,
        )

        self.expenses_label = ctk.CTkLabel(
            self.summary_frame,
            text="Gastos: R$ 0,00",
        )
        self.expenses_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=15,
        )

        self.profit_label = ctk.CTkLabel(
            self.summary_frame,
            text="Lucro real: R$ 0,00",
            font=ctk.CTkFont(
                weight="bold",
            ),
        )
        self.profit_label.grid(
            row=0,
            column=2,
            padx=10,
            pady=15,
        )

    def _create_transactions(self):
        self.transactions_frame = ctk.CTkScrollableFrame(
            self,
            label_text="Transações",
        )
        self.transactions_frame.grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew",
        )

    def _load_data(
        self,
        start_date=None,
        end_date=None,
        transaction_type=None,
        description=None,
        min_value_centavos=None,
        max_value_centavos=None,
    ):
        self._clear_transactions()

        transactions = get_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=transaction_type,
            description=description,
            min_value_centavos=min_value_centavos,
            max_value_centavos=max_value_centavos,
        )

        summary = calculate_summary(
            start_date=start_date,
            end_date=end_date,
        )

        self.gains_label.configure(
            text=(
                f"Ganhos: "
                f"{cents_to_money(summary['total_ganhos'])}"
            ),
        )

        self.expenses_label.configure(
            text=(
                f"Gastos: "
                f"{cents_to_money(summary['total_gastos'])}"
            ),
        )

        self.profit_label.configure(
            text=(
                f"Lucro real: "
                f"{cents_to_money(summary['lucro_real'])}"
            ),
        )

        if not transactions:
            empty_label = ctk.CTkLabel(
                self.transactions_frame,
                text="Nenhuma transação encontrada.",
            )
            empty_label.pack(
                padx=20,
                pady=20,
            )
            return

        for transaction in transactions:
            self._create_transaction_row(transaction)

    def _apply_filters(self):
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        transaction_type = self.type_combobox.get()

        if transaction_type == "Todos":
            transaction_type = None

        description = self.description_entry.get().strip()

        if not description:
            description = None

        min_value = self.min_value_entry.get().strip()
        max_value = self.max_value_entry.get().strip()

        try:
            if start_date:
                start_date = brazil_date_to_database(
                    start_date
                )

            if end_date:
                end_date = brazil_date_to_database(
                    end_date
                )

            min_value_centavos = (
                parse_money(min_value)
                if min_value
                else None
            )

            max_value_centavos = (
                parse_money(max_value)
                if max_value
                else None
            )

            self._load_data(
                start_date=start_date or None,
                end_date=end_date or None,
                transaction_type=transaction_type,
                description=description,
                min_value_centavos=min_value_centavos,
                max_value_centavos=max_value_centavos,
            )

        except ValueError as error:
            self._show_message(str(error))

    def _clear_filters(self):
        self.start_date_entry.delete(0, "end")
        self.end_date_entry.delete(0, "end")

        self.type_combobox.set("Todos")

        self.description_entry.delete(0, "end")
        self.min_value_entry.delete(0, "end")
        self.max_value_entry.delete(0, "end")

        self._load_data()

    def _create_transaction_row(self, transaction):
        row = ctk.CTkFrame(
            self.transactions_frame,
        )
        row.pack(
            fill="x",
            padx=5,
            pady=5,
        )

        row.grid_columnconfigure(
            0,
            weight=1,
        )

        transaction_id = transaction["id"]
        transaction_type = transaction["tipo"]
        description = transaction["descricao"]
        value = transaction["valor_centavos"]
        transaction_date = database_date_to_brazil(transaction["data_transacao"])
        status = transaction["status"]

        info = (
            f"#{transaction_id} | "
            f"{transaction_type} | "
            f"{transaction_date} | "
            f"{description} | "
            f"{cents_to_money(value)} | "
            f"{status}"
        )

        label = ctk.CTkLabel(
            row,
            text=info,
            anchor="w",
        )
        label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w",
        )

        if status == "ATIVA":
            cancel_button = ctk.CTkButton(
                row,
                text="Cancelar",
                width=100,
                command=lambda tid=transaction_id: (
                    self._cancel_transaction(tid)
                ),
            )
            cancel_button.grid(
                row=0,
                column=1,
                padx=10,
                pady=5,
                sticky="e",
            )

    def _cancel_transaction(self, transaction_id):
        dialog = ctk.CTkInputDialog(
            text="Informe o motivo do cancelamento:",
            title="Cancelar transação",
        )

        reason = dialog.get_input()

        if reason is None:
            return

        reason = reason.strip()

        if not reason:
            return

        try:
            cancel_transaction(
                transaction_id,
                reason,
            )
        except ValueError as error:
            self._show_message(str(error))
            return

        self._apply_filters()

    def _clear_transactions(self):
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()

    def _show_message(self, message):
        dialog = ctk.CTkInputDialog(
            text=message,
            title="Controle Financeiro",
        )
        dialog.get_input()

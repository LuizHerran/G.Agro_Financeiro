import customtkinter as ctk

from app.reports.periods import get_current_month_period
from app.utils.dates import ( brazil_date_to_database, database_date_to_brazil, today_brazil,)
from app.ui.date_picker import DatePicker
from tkinter import filedialog
from app.services.transactions import ( calculate_summary, cancel_transaction, get_transactions,)
from app.utils.money import ( cents_to_money, parse_money,)
from app.reports.history_csv import generate_history_csv
from app.reports.history_excel import generate_history_excel
from tkinter import filedialog, messagebox
from datetime import date
from app.reports.history_pdf import generate_history_pdf

from PIL import Image

class HistoryView(ctk.CTkFrame):
    
    def __init__(self, parent, on_back):
        super().__init__(parent)

        self.on_back = on_back

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.calendar_icon = ctk.CTkImage(
            light_image=Image.open("app/ui/assets/calendar.png"),
            dark_image=Image.open("app/ui/assets/calendar.png"),
            size=(22, 22),
        )

        self._create_header()
        self._create_filters()

        start_date, end_date = self._set_current_month_filter()

        self._create_summary()
        self._create_transactions()
        self._create_export_buttons()

        self._load_data(
            start_date=start_date,
            end_date=end_date,
        )

    def _set_current_month_filter(self):
        start_date, end_date = get_current_month_period()

        self.start_date_entry.insert(
            0,
            database_date_to_brazil(start_date),
        )

        self.end_date_entry.insert(
            0,
            database_date_to_brazil(end_date),
        )

        return start_date, end_date

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

        start_date_frame = ctk.CTkFrame(
            filters,
            fg_color="transparent",
        )

        start_date_frame.grid(
            row=0,
            column=1,
            padx=5,
            pady=(10, 5),
            sticky="ew",
        )

        start_date_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        self.start_date_entry = ctk.CTkEntry(
            start_date_frame,
            placeholder_text="DD/MM/AAAA",
        )

        self.start_date_entry.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        start_calendar_button = ctk.CTkButton(
            start_date_frame,
            text="",
            image=self.calendar_icon,
            width=40,
            height=32,
            command=self._open_start_date_picker,
        )

        start_calendar_button.grid(
            row=0,
            column=1,
            padx=(5, 0),
        )

        start_date_frame.grid_columnconfigure(0, weight=1)

        end_date_frame = ctk.CTkFrame(
            filters,
            fg_color="transparent",
        )

        end_date_frame.grid(
            row=0,
            column=3,
            padx=5,
            pady=(10, 5),
            sticky="ew",
        )

        end_date_frame.grid_columnconfigure(0, weight=1)

        self.end_date_entry = ctk.CTkEntry(
            end_date_frame,
            placeholder_text="DD/MM/AAAA",
        )

        self.end_date_entry.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        end_calendar_button = ctk.CTkButton(
            end_date_frame,
            text="",
            image=self.calendar_icon,
            width=40,
            height=32,
            command=self._open_end_date_picker,
        )

        end_calendar_button.grid(
            row=0,
            column=1,
            padx=(5, 0),
        )

        start_calendar_button = ctk.CTkButton(
            start_date_frame,
            text="",
            image=self.calendar_icon,
            width=40,
            height=32,
            command=self._open_start_date_picker,
        )

        start_calendar_button.grid(
            row=0,
            column=1,
            padx=(5, 0),
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

        end_date_frame = ctk.CTkFrame(
            filters,
            fg_color="transparent",
        )

        end_date_frame.grid(
            row=0,
            column=3,
            padx=5,
            pady=(10, 5),
            sticky="ew",
        )

        end_date_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        self.end_date_entry = ctk.CTkEntry(
            end_date_frame,
            placeholder_text="DD/MM/AAAA",
        )

        self.end_date_entry.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        end_calendar_button = ctk.CTkButton(
            end_date_frame,
            text="",
            image=self.calendar_icon,
            width=40,
            height=32,
            command=self._open_end_date_picker,
        )

        end_calendar_button.grid(
            row=0,
            column=1,
            padx=(5, 0),
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

        # =========================================================
        # BOTÕES DOS FILTROS
        # =========================================================

        filter_buttons_frame = ctk.CTkFrame(
            filters,
            fg_color="transparent",
        )

        filter_buttons_frame.grid(
            row=2,
            column=0,
            columnspan=6,
            sticky="w",
            padx=10,
            pady=(5, 10),
        )

        filter_button = ctk.CTkButton(
            filter_buttons_frame,
            text="Filtrar",
            width=120,
            command=self._apply_filters,
        )

        filter_button.pack(
            side="left",
            padx=(0, 5),
        )

        clear_button = ctk.CTkButton(
            filter_buttons_frame,
            text="Limpar filtros",
            width=120,
            fg_color="transparent",
            border_width=1,
            command=self._clear_filters,
        )

        clear_button.pack(
            side="left",
            padx=5,
        )

    def _create_export_buttons(self):
        export_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        export_frame.grid(
            row=4,
            column=0,
            padx=10,
            pady=(0, 15),
            sticky="e",
        )

        export_excel_button = ctk.CTkButton(
            export_frame,
            text="Exportar para Excel",
            width=150,
            command=self._export_excel,
        )

        export_excel_button.pack(
            side="left",
            padx=5,
        )

        export_pdf_button = ctk.CTkButton(
            export_frame,
            text="Exportar para PDF",
            width=150,
            command=self._export_pdf,
        )

        export_pdf_button.pack(
            side="left",
            padx=(5, 0),
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
        self.tabview = ctk.CTkTabview(self)

        self.tabview.grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew",
        )

        self.tabview.add("Ativas")
        self.tabview.add("Canceladas")

        self.active_transactions_frame = ctk.CTkScrollableFrame(
            self.tabview.tab("Ativas"),
            label_text="Transações ativas",
        )

        self.active_transactions_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5,
        )

        self.cancelled_transactions_frame = ctk.CTkScrollableFrame(
            self.tabview.tab("Canceladas"),
            label_text="Transações canceladas",
        )

        self.cancelled_transactions_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5,
        )

    def _load_data( self, start_date=None, end_date=None, transaction_type=None, description=None, min_value_centavos=None, max_value_centavos=None, ):
        self._clear_transactions()

        active_transactions = get_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=transaction_type,
            description=description,
            min_value_centavos=min_value_centavos,
            max_value_centavos=max_value_centavos,
            include_cancelled=False,
        )

        cancelled_transactions = get_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=transaction_type,
            description=description,
            min_value_centavos=min_value_centavos,
            max_value_centavos=max_value_centavos,
            include_cancelled=True,
        )

        cancelled_transactions = [
            transaction
            for transaction in cancelled_transactions
            if transaction["status"] == "CANCELADA"
        ]

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

        if not active_transactions:
            empty_label = ctk.CTkLabel(
                self.active_transactions_frame,
                text="Nenhuma transação ativa encontrada.",
            )
            empty_label.pack(
                padx=20,
                pady=20,
            )
        else:
            for transaction in active_transactions:
                self._create_transaction_row(
                    transaction,
                    self.active_transactions_frame,
                )

        if not cancelled_transactions:
            empty_label = ctk.CTkLabel(
                self.cancelled_transactions_frame,
                text="Nenhuma transação cancelada encontrada.",
            )
            empty_label.pack(
                padx=20,
                pady=20,
            )
        else:
            for transaction in cancelled_transactions:
                self._create_transaction_row(
                    transaction,
                    self.cancelled_transactions_frame,
                )

    def _clear_filters(self):
        self.start_date_entry.delete(0, "end")
        self.end_date_entry.delete(0, "end")

        self.type_combobox.set("Todos")

        self.description_entry.delete(0, "end")
        self.min_value_entry.delete(0, "end")
        self.max_value_entry.delete(0, "end")

        self._load_data()

    def _apply_filters(self):
        try:
            filters = self._get_current_filters()

            self._load_data(
                **filters,
            )

        except ValueError as error:
            self._show_message(str(error))

    def _open_start_date_picker(self):

        initial_date = None

        value = self.start_date_entry.get().strip()

        if value:
            try:
                initial_date = date.fromisoformat(
                    brazil_date_to_database(value)
                )
            except ValueError:
                initial_date = None

        picker = DatePicker(
            self,
            initial_date=initial_date,
            on_select=self._set_start_date,
        )

        picker.place(
            relx=0.5,
            rely=0.35,
            anchor="center",
        )

    def _open_end_date_picker(self):

        initial_date = None

        value = self.end_date_entry.get().strip()

        if value:
            try:
                initial_date = date.fromisoformat(
                    brazil_date_to_database(value)
                )
            except ValueError:
                initial_date = None

        picker = DatePicker(
            self,
            initial_date=initial_date,
            on_select=self._set_end_date,
        )

        picker.place(
            relx=0.5,
            rely=0.35,
            anchor="center",
        )

    def _set_start_date(self, selected_date):
        self.start_date_entry.delete(0, "end")
        self.start_date_entry.insert(
            0,
            selected_date.strftime("%d/%m/%Y"),
        )


    def _set_end_date(self, selected_date):
        self.end_date_entry.delete(0, "end")
        self.end_date_entry.insert(
            0,
            selected_date.strftime("%d/%m/%Y"),
        )
        
        def _clear_filters(self):
            self.start_date_entry.delete(0, "end")
            self.end_date_entry.delete(0, "end")

            self.type_combobox.set("Todos")

            self.description_entry.delete(0, "end")
            self.min_value_entry.delete(0, "end")
            self.max_value_entry.delete(0, "end")

            self._load_data()

    def _create_transaction_row(self, transaction, parent_frame,):
        row = ctk.CTkFrame(
            parent_frame,
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
            f"{cents_to_money(value)}"
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
        for widget in self.active_transactions_frame.winfo_children():
            widget.destroy()

        for widget in self.cancelled_transactions_frame.winfo_children():
            widget.destroy()

    def _show_message(self, message):
        messagebox.showinfo(
            "Controle Financeiro",
            message,
        )

    def _export_excel(self):
        try:
            filters = self._get_current_filters()

            transactions = get_transactions(
                **filters,
                include_cancelled=True,
            )

            summary = calculate_summary(
                start_date=filters["start_date"],
                end_date=filters["end_date"],
            )

        except ValueError as error:
            self._show_message(str(error))
            return

        if not transactions:
            self._show_message(
                "Não existem transações para exportar."
            )
            return

        output_path = filedialog.asksaveasfilename(
            title="Salvar relatório Excel",
            defaultextension=".xlsx",
            filetypes=[
                ("Arquivo Excel", "*.xlsx"),
                ("Todos os arquivos", "*.*"),
            ],
            initialfile="Relatorio_Financeiro.xlsx",
        )

        if not output_path:
            return

        try:
            generate_history_excel(
                transactions=transactions,
                summary=summary,
                output_path=output_path,
                filters=filters,
            )

        except Exception as error:
            self._show_message(
                f"Erro ao gerar relatório Excel:\n\n{type(error).__name__}: {error}"
            )
            return

        self._show_message(
            f"Relatório exportado com sucesso para:\n{output_path}"
        ) 

    def _export_pdf(self):
        try:
            filters = self._get_current_filters()

            transactions = get_transactions(
                **filters,
                include_cancelled=True,
            )

            summary = calculate_summary(
                start_date=filters["start_date"],
                end_date=filters["end_date"],
            )

        except ValueError as error:
            self._show_message(str(error))
            return

        if not transactions:
            self._show_message(
                "Não existem transações para exportar."
            )
            return

        output_path = filedialog.asksaveasfilename(
            title="Salvar relatório PDF",
            defaultextension=".pdf",
            filetypes=[
                ("Arquivo PDF", "*.pdf"),
                ("Todos os arquivos", "*.*"),
            ],
            initialfile="Relatorio_Financeiro.pdf",
        )

        if not output_path:
            return

        try:
            generate_history_pdf(
                transactions=transactions,
                summary=summary,
                output_path=output_path,
                filters=filters,
            )

        except Exception as error:
            self._show_message(
                "Erro ao gerar relatório PDF:\n\n"
                f"{type(error).__name__}: {error}"
            )
            return

        self._show_message(
            f"Relatório PDF exportado com sucesso:\n{output_path}"
        )

    def _get_current_filters(self):
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

        if start_date:
            start_date = brazil_date_to_database(start_date)

        if end_date:
            end_date = brazil_date_to_database(end_date)

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

        return {
            "start_date": start_date or None,
            "end_date": end_date or None,
            "transaction_type": transaction_type,
            "description": description,
            "min_value_centavos": min_value_centavos,
            "max_value_centavos": max_value_centavos,
        }

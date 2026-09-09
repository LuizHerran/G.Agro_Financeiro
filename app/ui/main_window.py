import customtkinter as ctk
from app.ui.history_view import HistoryView
from app.ui.transaction_form import TransactionForm
from pathlib import Path

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("G.Agro")
        
        icon_path = Path(__file__).parent / "assets" / "logo.ico"
        self.iconbitmap(icon_path)
        
        self.geometry("900x600")
        self.minsize(800, 650)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header()

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.content.grid(
            row=1,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew",
        )

        self.content.grid_columnconfigure(
            0,
            weight=1,
        )
        self.content.grid_columnconfigure(
            1,
            weight=1,
        )
        self.content.grid_rowconfigure(
            0,
            weight=1,
        )
        self.content.grid_rowconfigure(
            1,
            weight=1,
        )

        self.show_home()

    def _create_header(self):
        self.header = ctk.CTkFrame(
            self,
            corner_radius=0,
        )
        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        self.header.grid_columnconfigure(
            0,
            weight=1,
        )

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Controle Financeiro",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )
        self.title_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky="w",
        )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()

        self.content.grid_columnconfigure(
            0,
            weight=1,
        )
        self.content.grid_columnconfigure(
            1,
            weight=1,
        )

        gain_button = ctk.CTkButton(
            self.content,
            text="Registrar Ganho",
            height=80,
            command=self.show_gain_form,
        )
        gain_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="ew",
        )

        expense_button = ctk.CTkButton(
            self.content,
            text="Registrar Gasto",
            height=80,
            command=self.show_expense_form,
        )
        expense_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="ew",
        )

        history_button = ctk.CTkButton(
            self.content,
            text="Histórico",
            height=80,
            command=self.show_history,
        )
        history_button.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew",
        )

    def show_gain_form(self):
        self.clear_content()

        form = TransactionForm(
            self.content,
            "GANHO",
            self.show_home,
        )

        form.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
        )

    def show_expense_form(self):
        self.clear_content()

        form = TransactionForm(
            self.content,
            "GASTO",
            self.show_home,
        )

        form.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
        )
        
    def show_history(self):
        self.clear_content()

        history = HistoryView(
            self.content,
            self.show_home,
        )

        history.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
        )
import customtkinter as ctk

from PIL import Image, ImageOps
from app.utils.resources import resource_path
from app.ui.history_view import HistoryView
from app.ui.transaction_form import TransactionForm
from pathlib import Path
from app.utils.resources import resource_path
from app.utils.version import APP_VERSION

BACKGROUND = "#F4F1E8"
DARK_GREEN = "#173A24"
GREEN = "#3F7D3A"
LIGHT_GREEN = "#6FAF45"
AGRO_YELLOW = "#D9A441"
TEXT = "#1E241F"
WHITE = "#FFFFFF"

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("G.Agro")

        icon_path = resource_path("app/ui/assets/logo.ico")
        self.iconbitmap(str(icon_path))

        self.configure(
            fg_color=BACKGROUND,
        )

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.after(100, lambda: self.state("zoomed"))

        self._create_header()
        self._create_sidebar()

        self.content = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND,
            corner_radius=0,
        )
#---------------------------------------------------------------------
        self.content.grid(
            row=1,
            column=1,
            padx=0,
            pady=0,
            sticky="nsew",
        )

        self.content.grid_columnconfigure(
            0,
            weight=1,
        )

        self.content.grid_rowconfigure(
            0,
            weight=1,
        )

        self.show_home()

    def _create_header(self):
        self.header = ctk.CTkFrame(
            self,
            fg_color=DARK_GREEN,
            corner_radius=0,
            height=60,
        )

        self.header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
        )

        self.header.grid_columnconfigure(
            0,
            weight=1,
        )

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Controle Financeiro",
            text_color=WHITE,
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )

        self.title_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=15,
            sticky="w",
        )

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            fg_color=DARK_GREEN,
            corner_radius=0,
        )

        self.sidebar.grid(
            row=1,
            column=0,
            padx=0,
            pady=0,
            sticky="nsew",
        )

        self.sidebar.grid_propagate(False)

        self.sidebar.grid_columnconfigure(
            0,
            weight=1,
        )

        self.sidebar.grid_rowconfigure(
            0,
            weight=0,
        )

        self.sidebar.grid_rowconfigure(
            1,
            weight=1,
        )
        
        self.sidebar.grid_rowconfigure(
            2,
            weight=0,
        )

        menu_title = ctk.CTkLabel(
            self.sidebar,
            text="Menu",
            text_color=WHITE,
            font=ctk.CTkFont(
                size=22,
                weight="bold",
            ),
        )

        menu_title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(25, 30),
        )

        menu_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
        )

        menu_frame.grid(
            row=1,
            column=0,
            padx=15,
            pady=0,
            sticky="n",
        )

        self.gain_menu_button = ctk.CTkButton(
            menu_frame,
            text="Registrar Ganho",
            width=190,
            height=50,
            fg_color=GREEN,
            hover_color=LIGHT_GREEN,
            text_color=WHITE,
            command=self.show_gain_form,
        )

        self.gain_menu_button.pack(
            pady=6,
        )

        self.expense_menu_button = ctk.CTkButton(
            menu_frame,
            text="Registrar Gasto",
            width=190,
            height=50,
            fg_color=DARK_GREEN,
            hover_color=GREEN,
            text_color=WHITE,
            command=self.show_expense_form,
        )

        self.expense_menu_button.pack(
            pady=6,
        )

        self.history_menu_button = ctk.CTkButton(
            menu_frame,
            text="Histórico",
            width=190,
            height=50,
            fg_color=DARK_GREEN,
            hover_color=GREEN,
            text_color=WHITE,
            command=self.show_history,
        )

        self.history_menu_button.pack(
            pady=6,
        )
        
        version_label = ctk.CTkLabel(
            self.sidebar,
            text=f"v{APP_VERSION}",
            text_color="#B8C9BC",
            font=ctk.CTkFont(
                size=12,
            ),
        )

        version_label.grid(
            row=2,
            column=0,
            padx=15,
            pady=10,
            sticky="sw",
        )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()

        welcome_frame = self.content

        welcome_image_path = resource_path(
            "app/ui/assets/welcome.png"
        )

        original_image = Image.open(welcome_image_path)


        def update_welcome_image(event=None):
            width = welcome_frame.winfo_width()
            height = welcome_frame.winfo_height()

            if width <= 1 or height <= 1:
                return

            resized_image = ImageOps.fit(
                original_image,
                (width, height),
                method=Image.Resampling.LANCZOS,
            )

            welcome_image = ctk.CTkImage(
                light_image=resized_image,
                dark_image=resized_image,
                size=(width, height),
            )

            welcome_image_label.configure(
                image=welcome_image,
            )

            welcome_image_label.image = welcome_image


        welcome_image_label = ctk.CTkLabel(
            welcome_frame,
            text="",
        )

        welcome_image_label.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1,
        )

        welcome_frame.bind(
            "<Configure>",
            update_welcome_image,
        )
        
        welcome_frame.after(
            100,
            update_welcome_image,
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
            sticky="nsew",
        )
        
from app.database.schema import initialize_database
from app.ui.main_window import MainWindow


def run_app():
    initialize_database()

    app = MainWindow()
    app.mainloop()
import os
import subprocess
import sys
import threading
from pathlib import Path
from tkinter import messagebox

from app.database.schema import initialize_database
from app.services.update_checker import check_for_update
from app.services.updater import download_installer
from app.ui.main_window import MainWindow
from app.utils.version import APP_VERSION


def _check_update_in_background(app):
    update_info = check_for_update()

    if update_info is None:
        return

    app.after(
        0,
        lambda: _show_update_message(app, update_info),
    )


def _show_update_message(app, update_info):
    version = update_info["version"]

    should_update = messagebox.askyesno(
        "Atualização disponível",
        (
            "Uma nova versão do G.Agro Financeiro "
            "está disponível!\n\n"
            f"Versão atual: {APP_VERSION}\n"
            f"Nova versão: {version}\n\n"
            "Deseja atualizar agora?\n\n"
            "O sistema será fechado durante a atualização "
            "e será aberto novamente ao finalizar."
        ),
        parent=app,
    )

    if not should_update:
        return

    try:
        messagebox.showinfo(
            "Atualização",
            (
                "A atualização será baixada agora.\n\n"
                "O sistema será fechado automaticamente "
                "quando o download terminar."
            ),
            parent=app,
        )

        installer_path = download_installer(
            url=update_info["installer_url"],
            version=update_info["version"],
        )

        updater_path = _get_updater_path()
        application_path = Path(sys.executable).resolve()

        subprocess.Popen(
            [
                str(updater_path),
                str(os.getpid()),
                str(installer_path),
                str(application_path),
            ],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        app.destroy()

    except Exception as error:
        messagebox.showerror(
            "Erro na atualização",
            (
                "Não foi possível iniciar a atualização.\n\n"
                f"Detalhes: {error}"
            ),
            parent=app,
        )


def _get_updater_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "Updater.exe"

    return Path(__file__).resolve().parents[2] / "dist" / "Updater.exe"


def start_update_check(app):
    thread = threading.Thread(
        target=_check_update_in_background,
        args=(app,),
        daemon=True,
    )

    thread.start()


def run_app():
    initialize_database()

    app = MainWindow()

    start_update_check(app)

    app.mainloop()


if __name__ == "__main__":
    run_app()
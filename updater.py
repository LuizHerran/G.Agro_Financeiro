import subprocess
import sys
import time
from pathlib import Path


def process_exists(pid: int) -> bool:
    try:
        result = subprocess.run(
            [
                "tasklist",
                "/FI",
                f"PID eq {pid}",
                "/NH",
            ],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
            check=False,
        )

        return str(pid) in result.stdout

    except Exception:
        return False


def main() -> None:
    if len(sys.argv) < 4:
        return

    try:
        application_pid = int(sys.argv[1])
    except ValueError:
        return

    installer_path = Path(sys.argv[2])
    application_path = Path(sys.argv[3])

    if not installer_path.exists():
        return

    if not application_path.exists():
        return

    # Aguarda o Controle Financeiro fechar.
    while process_exists(application_pid):
        time.sleep(1)

    # Executa o instalador.
    installer_process = subprocess.run(
    [
        str(installer_path),
        "/SILENT",
    ],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    check=False,
    )

    # Se a instalação terminou, abre a nova versão.
    if installer_process.returncode == 0:
        subprocess.Popen(
            [str(application_path)],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )


if __name__ == "__main__":
    main()
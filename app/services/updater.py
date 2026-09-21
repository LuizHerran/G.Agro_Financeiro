import tempfile
from pathlib import Path
from urllib.request import Request, urlopen


def download_installer(url: str, version: str) -> Path:
    temp_dir = Path(tempfile.gettempdir()) / "ControleFinanceiro"

    temp_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    installer_path = (
        temp_dir
        / f"ControleFinanceiro-Setup-{version}.exe"
    )

    request = Request(
        url,
        headers={
            "User-Agent": "ControleFinanceiro-Updater",
        },
    )

    with urlopen(request, timeout=60) as response:
        with open(installer_path, "wb") as file:
            while True:
                chunk = response.read(1024 * 1024)

                if not chunk:
                    break

                file.write(chunk)

    if not installer_path.exists():
        raise RuntimeError(
            "O instalador não foi baixado."
        )

    if installer_path.stat().st_size == 0:
        raise RuntimeError(
            "O instalador baixado está vazio."
        )

    return installer_path
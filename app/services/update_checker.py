import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.utils.version import APP_VERSION


UPDATE_URL = (
    "https://api.github.com/repos/"
    "LuizHerran/G.Agro_Financeiro/releases/latest"
)


def _normalize_version(version: str) -> tuple[int, ...]:
    version = version.strip().lower()

    if version.startswith("v"):
        version = version[1:]

    parts = version.split(".")

    try:
        return tuple(int(part) for part in parts)
    except ValueError:
        return ()


def check_for_update():
    request = Request(
        UPDATE_URL,
        headers={
            "User-Agent": "ControleFinanceiro-Updater",
            "Accept": "application/vnd.github+json",
        },
    )

    try:
        with urlopen(request, timeout=5) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

    except (
        HTTPError,
        URLError,
        TimeoutError,
        json.JSONDecodeError,
    ):
        return None

    latest_version = data.get(
        "tag_name",
        "",
    ).strip()

    if not latest_version:
        return None

    current = _normalize_version(APP_VERSION)
    latest = _normalize_version(latest_version)

    if not current or not latest:
        return None

    if latest <= current:
        return None

    installer_url = None

    for asset in data.get("assets", []):
        asset_name = asset.get(
            "name",
            "",
        ).lower()

        if (
            asset_name.endswith(".exe")
            and "setup" in asset_name
        ):
            installer_url = asset.get(
                "browser_download_url"
            )
            break

    if not installer_url:
        return None

    return {
        "version": latest_version.lstrip("v"),
        "url": data.get("html_url"),
        "installer_url": installer_url,
        "name": data.get("name", ""),
    }
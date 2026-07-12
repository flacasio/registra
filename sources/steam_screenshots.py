"""
Monitor de capturas de tela da Steam.
"""

from config import STEAM_USER

from core.console import header, info, warning
from core.list_notifier import notify_new_items
from core.steam import screenshots

from parsers.steam_screenshots import parse
from templates.steam_screenshots import make_card


MODULE = "steam_screenshots"


def run():
    header("Steam • Screenshots")

    if not STEAM_USER:
        warning("STEAM_USER nao configurado.")
        return

    info("Baixando capturas...")

    html = screenshots()

    info("Interpretando capturas...")

    activities = parse(html)

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhuma captura encontrada.",
    )

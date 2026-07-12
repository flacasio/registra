"""
Monitor de insignias da Steam.
"""

from config import STEAM_USER

from core.console import header, info, warning
from core.list_notifier import notify_new_items
from core.steam import badges

from parsers.steam_badges import parse
from templates.steam_badges import make_card


MODULE = "steam_badges"


def run():
    header("Steam • Badges")

    if not STEAM_USER:
        warning("STEAM_USER nao configurado.")
        return

    info("Baixando insignias...")

    html = badges()

    info("Interpretando insignias...")

    activities = parse(html)

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhuma insignia encontrada.",
    )

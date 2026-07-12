"""
Monitor de amizades da Steam.
"""

from config import STEAM_USER

from core.console import header, info, warning
from core.list_notifier import notify_new_items
from core.steam import friends

from parsers.steam_friends import parse
from templates.steam_friends import make_card


MODULE = "steam_friends"


def run():
    header("Steam • Friends")

    if not STEAM_USER:
        warning("STEAM_USER nao configurado.")
        return

    info("Baixando amigos...")

    html = friends()

    info("Interpretando amigos...")

    activities = parse(html)

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum amigo encontrado.",
    )

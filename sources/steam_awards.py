"""
Monitor de premios recebidos na Steam.
"""

from config import STEAM_USER

from core.console import header, info, warning
from core.list_notifier import notify_new_items
from core.steam import awards

from parsers.steam_awards import parse
from templates.steam_awards import make_card


MODULE = "steam_awards"


def run():
    header("Steam • Awards")

    if not STEAM_USER:
        warning("STEAM_USER nao configurado.")
        return

    info("Baixando premios...")

    html = awards()

    info("Interpretando premios...")

    activities = parse(html)

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum premio encontrado.",
    )

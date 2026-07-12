"""
Monitor de novos jogos na biblioteca da Steam.
"""

from config import STEAM_USER

from core.console import header, info, warning
from core.list_notifier import notify_new_items
from core.steam import owned_games

from parsers.steam_games import parse_owned
from templates.steam_games import make_card


MODULE = "steam_new"


def run():
    header("Steam • Novos Jogos")

    if not STEAM_USER:
        warning("STEAM_USER nao configurado.")
        return

    info("Baixando biblioteca...")

    data = owned_games()

    info("Interpretando jogos...")

    activities = parse_owned(data, "STEAM_NEW")

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum jogo encontrado.",
    )

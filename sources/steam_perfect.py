"""
Monitor de jogos platinados na Steam.
"""

from config import STEAM_USER

from core.console import header, info, warning
from core.list_notifier import notify_new_items
from core.steam import games_perfect

from parsers.steam_games import parse
from templates.steam_games import make_card


MODULE = "steam_perfect"


def run():
    header("Steam • Jogos Platinados")

    if not STEAM_USER:
        warning("STEAM_USER nao configurado.")
        return

    info("Baixando jogos platinados...")

    html = games_perfect()

    info("Interpretando jogos...")

    activities = parse(html, "STEAM_PERFECT")

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum jogo platinado encontrado.",
    )

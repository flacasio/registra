"""
Monitor de reviews da Steam.
"""

from core.cache import cache_diff
from core.console import header, info, success, warning
from core.steam import game_details, reviews
from core.telegram import send

from parsers.steam_reviews import parse_all
from templates.steam_reviews import make_card


MODULE = "steam_reviews"


def run():
    header("Steam • Reviews")

    info("Baixando reviews...")

    html = reviews()

    info("Interpretando reviews...")

    activities = parse_all(html)

    if not activities:
        warning("Usuario ainda nao possui reviews.")
        success(f"{MODULE} finalizado.")
        return

    ids = [activity["id"] for activity in activities]
    novos = set(cache_diff(MODULE, ids))

    if not novos:
        warning("Nenhuma review nova.")
        success(f"{MODULE} finalizado.")
        return

    enviados = 0

    for activity in reversed(activities):
        if activity["id"] not in novos:
            continue

        info("Obtendo detalhes do jogo...")

        game = game_details(activity["appid"])
        activity["game"] = game["name"]

        info("Montando card...")

        card = make_card(activity)

        info("Enviando Telegram...")

        send(card)
        enviados += 1

    success(f"{enviados} card(s) enviado(s).")
    success(f"{MODULE} finalizado.")

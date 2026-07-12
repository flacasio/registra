"""
Monitor de comentarios no perfil da Steam.
"""

from core.cache import cache_diff
from core.console import header, info, success, warning
from core.steam import comments
from core.telegram import send

from parsers.steam_comments import parse_all
from templates.steam_comments import make_card


MODULE = "steam_comments"


def run():
    header("Steam • Comments")

    info("Baixando comentarios...")

    data = comments()

    info("Interpretando comentarios...")

    activities = parse_all(data)

    if not activities:
        warning("Nenhum comentario encontrado.")
        return

    ids = [activity["id"] for activity in activities]
    novos = set(cache_diff(MODULE, ids))

    if not novos:
        warning("Nenhum comentario novo.")
        return

    enviados = 0

    for activity in reversed(activities):
        if activity["id"] not in novos:
            continue

        info("Montando card...")

        card = make_card(activity)

        info("Enviando Telegram...")

        send(card)
        enviados += 1

    success(f"{enviados} card(s) enviado(s).")

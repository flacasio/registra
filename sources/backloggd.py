"""
Monitor do Backloggd.
"""

from config import BACKLOGGD_USER

from core.backloggd import activity as download_activity
from core.cache import cache_diff
from core.console import header, info, success, warning
from core.telegram import send

from parsers.backloggd import parse
from templates.backloggd import make_card


MODULE = "backloggd"


def run():
    header("Backloggd")

    if not BACKLOGGD_USER:
        warning("BACKLOGGD_USER não configurado.")
        return

    info("Baixando atividades...")

    html = download_activity()

    info("Interpretando atividades...")

    activities = parse(html)

    if not activities:
        warning("Nenhuma atividade encontrada.")
        return

    ids = [activity["id"] for activity in activities]
    novos = set(cache_diff(MODULE, ids))

    if not novos:
        warning("Nenhuma novidade.")
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

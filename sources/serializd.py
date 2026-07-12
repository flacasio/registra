"""
Monitor do Serializd.
"""

from config import SERIALIZD_USER

from core.cache import cache_diff
from core.console import header, info, success, warning
from core.serializd import activity as download_activity
from core.telegram import send

from parsers.serializd import parse
from templates.serializd import make_card


MODULE = "serializd"
MAX_ACTIVITIES = 5


def run():
    header("Serializd")

    if not SERIALIZD_USER:
        warning("SERIALIZD_USER não configurado.")
        return

    info("Baixando atividades...")

    payload = download_activity()

    info("Interpretando atividades...")

    activities = parse(payload)[:MAX_ACTIVITIES]

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

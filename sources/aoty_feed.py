"""
Monitor de avaliacoes recentes no Album of the Year.
"""

from config import AOTY_USER

from core.aoty import AotyRateLimitedError, profile
from core.cache import cache_diff
from core.console import header, info, success, warning
from core.telegram import send

from parsers.aoty import parse
from templates.aoty import make_card


MODULE = "aoty_feed"


def run():
    header("AOTY")

    if not AOTY_USER:
        warning("AOTY_USER não configurado.")
        return

    info("Baixando perfil...")

    try:
        html = profile()
    except AotyRateLimitedError:
        warning("AOTY limitou as requisicoes. Vou tentar de novo depois.")
        return

    info("Interpretando avaliações...")

    activities = parse(html)

    if not activities:
        warning("Nenhuma avaliação encontrada.")
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

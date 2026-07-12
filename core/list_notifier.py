"""
Fluxo comum para listas que so devem avisar novidades.
"""

from core.cache import cache_current, cache_diff
from core.console import info, success, warning
from core.telegram import send


def notify_new_items(module, activities, make_card, empty_message):
    if not activities:
        warning(empty_message)
        return 0

    ids = [activity["id"] for activity in activities]

    if not cache_current(module):
        cache_diff(module, ids)
        warning(
            f"Base inicial salva com {len(ids)} item(ns). "
            "As proximas novidades serao notificadas."
        )
        return 0

    novos = set(cache_diff(module, ids))

    if not novos:
        warning("Nenhuma novidade.")
        return 0

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
    return enviados

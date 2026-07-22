"""
Monitor de avaliacoes recentes no Album of the Year.
"""

import json

from config import AOTY_USER

from core.aoty import AotyRateLimitedError, profile
from core.cache import cache_current, cache_diff, cache_save
from core.console import header, info, success, warning
from core.telegram import send

from parsers.aoty import parse
from templates.aoty import make_card


MODULE = "aoty_feed"


def _migrate_legacy_ids(ids):
    """Converte silenciosamente IDs antigos que continham tempo relativo."""
    raw = cache_current(MODULE)

    if not raw:
        return

    try:
        antigos = json.loads(raw)
    except json.JSONDecodeError:
        antigos = [raw]

    if not isinstance(antigos, list):
        antigos = [str(antigos)]

    antigos = [str(value) for value in antigos]
    migrados = list(antigos)
    mudou = False

    for stable_id in ids:
        if stable_id in antigos:
            continue

        prefix = f"{stable_id}|"

        if any(old_id.startswith(prefix) for old_id in antigos):
            migrados.insert(0, stable_id)
            mudou = True

    if mudou:
        cache_save(
            MODULE,
            json.dumps(
                list(dict.fromkeys(migrados))[:500],
                ensure_ascii=False,
                indent=4,
            ),
        )


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
    _migrate_legacy_ids(ids)
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

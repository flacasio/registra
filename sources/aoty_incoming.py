"""
Monitor de lancamentos no radar do AOTY.
"""

import os

from config import AOTY_USER

from core.aoty import AotyRateLimitedError, incoming_list
from core.console import header, info, success, warning
from core.list_notifier import notify_new_items
from core.telegram import send

from parsers.aoty_incoming import parse
from templates.aoty_incoming import make_card


MODULE = "aoty_incoming"


def _force_enabled():
    return os.getenv("REZISTRO_FORCE_AOTY_INCOMING", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "sim",
    }


def _force_limit():
    raw = os.getenv("AOTY_INCOMING_FORCE_LIMIT", "3").strip()

    try:
        return max(1, int(raw))
    except ValueError:
        return 3


def _send_force_preview(activities):
    if not activities:
        warning("Nenhum lancamento encontrado.")
        return

    limit = _force_limit()
    selecionadas = activities[:limit]
    enviados = 0

    warning(
        f"Modo teste ativado: reenviando {len(selecionadas)} item(ns) recente(s)."
    )

    for activity in reversed(selecionadas):
        info("Montando card...")
        card = make_card(activity)

        info("Enviando Telegram...")
        send(card)
        enviados += 1

    success(f"{enviados} card(s) enviado(s).")


def run():
    header("AOTY • Incoming")

    if not AOTY_USER:
        warning("AOTY_USER nao configurado.")
        return

    info("Baixando lista de lancamentos...")

    try:
        html = incoming_list()
    except AotyRateLimitedError:
        warning("AOTY limitou as requisicoes. Vou tentar de novo depois.")
        return

    info("Interpretando lista...")

    activities = parse(html)

    if _force_enabled():
        _send_force_preview(activities)
        return

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum lancamento encontrado.",
    )
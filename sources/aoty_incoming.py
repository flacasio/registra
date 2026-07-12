"""
Monitor de lancamentos no radar do AOTY.
"""

from config import AOTY_USER

from core.aoty import AotyRateLimitedError, incoming_list
from core.console import header, info, warning
from core.list_notifier import notify_new_items

from parsers.aoty_incoming import parse
from templates.aoty_incoming import make_card


MODULE = "aoty_incoming"


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

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum lancamento encontrado.",
    )

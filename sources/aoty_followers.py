"""
Monitor de novos seguidores no AOTY.
"""

from config import AOTY_USER

from core.aoty import AotyRateLimitedError, followers
from core.console import header, info, warning
from core.list_notifier import notify_new_items

from parsers.aoty_people import parse_followers
from templates.aoty_people import make_card


MODULE = "aoty_followers"


def run():
    header("AOTY • Followers")

    if not AOTY_USER:
        warning("AOTY_USER nao configurado.")
        return

    info("Baixando seguidores...")

    try:
        html = followers()
    except AotyRateLimitedError:
        warning("AOTY limitou as requisicoes. Vou tentar de novo depois.")
        return

    info("Interpretando seguidores...")

    activities = parse_followers(html)

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum seguidor encontrado.",
    )

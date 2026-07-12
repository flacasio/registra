"""
Monitor de wishlist da Steam.
"""

from config import STEAM_USER

from core.console import header, info, warning
from core.list_notifier import notify_new_items
from core.steam import wishlist, wishlist_json

from parsers.steam_wishlist import parse_all, parse_json
from templates.steam_wishlist import make_card


MODULE = "steam_wishlist"


def run():
    header("Steam • Wishlist")

    if not STEAM_USER:
        warning("STEAM_USER nao configurado.")
        return

    info("Baixando wishlist...")

    try:
        data = wishlist_json()
        info("Interpretando wishlist...")
        activities = parse_json(data)
    except Exception as json_error:
        warning(
            "Wishlist JSON indisponivel agora. "
            "Tentando pagina publica..."
        )

        try:
            html = wishlist()
            info("Interpretando wishlist...")
            activities = parse_all(html)
        except Exception as html_error:
            warning(
                "Steam bloqueou ou nao entregou a wishlist agora. "
                "O modulo sera ignorado nesta rodada."
            )
            warning(f"JSON: {json_error}")
            warning(f"Pagina: {html_error}")
            return

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum jogo encontrado na wishlist.",
    )

"""
Monitor de novos jogos na biblioteca da Steam.
"""

from config import STEAM_USER

from core.console import header, info, warning
from core.list_notifier import notify_new_items
from core.steam import games_all, owned_games

from parsers.steam_games import parse, parse_owned
from templates.steam_games import make_card


MODULE = "steam_new"


def run():
    header("Steam • Novos Jogos")

    if not STEAM_USER:
        warning("STEAM_USER nao configurado.")
        return

    info("Baixando biblioteca...")

    try:
        data = owned_games()
        info("Interpretando jogos...")
        activities = parse_owned(data, "STEAM_NEW")

        if not activities:
            raise RuntimeError("API de jogos retornou uma biblioteca vazia.")

    except Exception as api_error:
        warning(
            "Biblioteca pela API indisponivel ou vazia. "
            "Tentando pagina publica..."
        )

        try:
            html = games_all()
            info("Interpretando jogos...")
            activities = parse(html, "STEAM_NEW")
        except Exception as page_error:
            warning(
                "Steam bloqueou ou nao entregou a biblioteca agora. "
                "O modulo sera ignorado nesta rodada."
            )
            warning(f"API: {api_error}")
            warning(f"Pagina: {page_error}")
            return

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum jogo encontrado.",
    )

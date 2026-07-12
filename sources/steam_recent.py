"""
============================================================
Rezistro
Arquivo: sources/steam_recent.py
Versão: 2.0
============================================================

Responsabilidade:
Monitorar os jogos recentemente
jogados na Steam.
"""

from core.cache import cache_diff
from core.console import (
    header,
    info,
    success,
    warning,
)
from core.steam import recent_games
from core.telegram import send

from parsers.steam_recent import parse_all
from templates.steam_recent import make_card


MODULE = "steam_recent"


def run():

    header(
        "Steam • Jogos Recentes"
    )

    info(
        "Baixando jogos recentes..."
    )

    dados = recent_games()

    info(
        "Interpretando atividade..."
    )

    activities = parse_all(dados)

    if not activities:
        warning("Nenhum jogo recente encontrado.")
        return

    ids = [activity["id"] for activity in activities]
    novos = set(cache_diff(MODULE, ids))

    if not novos:

        warning(
            "Nenhuma novidade."
        )

        return

    enviados = 0

    for activity in reversed(activities):
        if activity["id"] not in novos:
            continue

        info(
            "Montando card..."
        )

        card = make_card(activity)

        info(
            "Enviando Telegram..."
        )

        send(card)
        enviados += 1

    success(
        f"{enviados} card(s) enviado(s)."
    )

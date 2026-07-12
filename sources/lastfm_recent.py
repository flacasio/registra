"""
Monitor de musicas recentemente escutadas no Last.fm.
"""

from core.cache import cache_diff
from core.console import header, info, success, warning
from core.lastfm import recent_tracks
from core.telegram import send

from parsers.lastfm_recent import parse
from templates.lastfm_recent import make_card


MODULE = "lastfm_recent"


def run():
    header("Last.fm • Recent Tracks")

    info("Baixando musicas recentes...")

    tracks = recent_tracks()

    if not tracks:
        warning("Nenhuma musica encontrada.")
        return

    info("Interpretando atividades...")

    activities = [parse(track) for track in tracks]
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

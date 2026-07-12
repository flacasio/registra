"""
Monitor de musicas favoritadas no Last.fm.
"""

from core.cache import cache_diff
from core.console import header, info, success, warning
from core.lastfm import loved_tracks
from core.telegram import send

from parsers.lastfm_loved import parse
from templates.lastfm_loved import make_card


MODULE = "lastfm_loved"


def run():
    header("Last.fm • Loved Tracks")

    info("Baixando musicas favoritadas...")

    tracks = loved_tracks()

    if not tracks:
        warning("Nenhuma musica favoritada.")
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

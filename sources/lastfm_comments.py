"""
Monitor de comentarios no perfil do Last.fm.
"""

from core.cache import cache_diff
from core.console import header, info, success, warning
from core.lastfm import comments
from core.telegram import send

from parsers.lastfm_comments import parse
from templates.lastfm_comments import make_card


MODULE = "lastfm_comments"


def _id(activity):
    return "|".join(
        str(part)
        for part in (
            activity.get("user"),
            activity.get("date"),
            activity.get("text"),
        )
        if part
    )


def run():
    header("Last.fm • Comments")

    info("Baixando comentarios...")

    html = comments()

    info("Interpretando comentarios...")

    activities = parse(html)

    if not activities:
        warning("Nenhum comentario encontrado.")
        return

    for activity in activities:
        activity["id"] = _id(activity)

    ids = [activity["id"] for activity in activities]
    novos = set(cache_diff(MODULE, ids))

    if not novos:
        warning("Nenhum comentario novo.")
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

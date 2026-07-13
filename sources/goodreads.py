"""
Monitor do Goodreads.
"""

import os

from bs4 import BeautifulSoup
from urllib.parse import urlencode

from config import GOODREADS_USER_ID

from core.cache import cache_diff
from core.console import header, info, success, warning
from core.downloader import download_text
from core.telegram import send

from parsers.goodreads import parse_rss_items
from templates.goodreads import make_card


SHELVES = [
    ("currently-reading", "CURRENTLY_READING"),
    ("to-read", "WANT_TO_READ"),
    ("read", "READ"),
]


def _rss_url(shelf):
    query = urlencode({
        "shelf": shelf,
        "sort": "date_updated",
        "per_page": 100,
    })

    return (
        "https://www.goodreads.com/review/list_rss/"
        f"{GOODREADS_USER_ID}?{query}"
    )


def _cache_module(tipo):
    return f"goodreads_{tipo.lower()}"


def _download_activities(shelf, tipo):
    xml = download_text(_rss_url(shelf))
    soup = BeautifulSoup(xml, "xml")
    return parse_rss_items(soup, tipo)


def _force_enabled():
    return os.getenv("REZISTRO_FORCE_GOODREADS", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "sim",
    }


def _force_limit():
    raw = os.getenv("GOODREADS_FORCE_LIMIT_PER_SHELF", "3").strip()

    try:
        return max(1, int(raw))
    except ValueError:
        return 3


def run():
    header("Goodreads")

    if not GOODREADS_USER_ID:
        warning("GOODREADS_USER_ID não configurado.")
        return

    enviados = 0
    force = _force_enabled()
    force_limit = _force_limit()

    if force:
        warning(
            "Modo resgate ativado: enviando itens recentes mesmo se o cache ja conhece."
        )

    for shelf, tipo in SHELVES:
        info(f"Baixando feed: {shelf}")

        activities = _download_activities(shelf, tipo)
        info(f"{len(activities)} item(ns) encontrado(s) em {shelf}.")

        if not activities:
            warning(f"Nenhuma atividade em {shelf}.")
            continue

        module = _cache_module(tipo)
        ids = [activity["id"] for activity in activities]

        if force:
            selecionadas = activities[:force_limit]
            novos = {activity["id"] for activity in selecionadas}
        else:
            novos = set(cache_diff(module, ids))

        if not novos:
            warning(f"Nenhuma novidade em {shelf}.")
            continue

        for activity in reversed(activities):
            if activity["id"] not in novos:
                continue

            info("Montando card...")

            card = make_card(activity)

            info("Enviando Telegram...")

            send(card)
            enviados += 1

    if enviados:
        success(f"{enviados} card(s) enviado(s).")
    else:
        warning("Nenhuma novidade.")
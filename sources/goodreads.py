"""
Monitor do Goodreads.
"""

from bs4 import BeautifulSoup

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
    return (
        "https://www.goodreads.com/review/list_rss/"
        f"{GOODREADS_USER_ID}?shelf={shelf}"
    )


def _cache_module(tipo):
    return f"goodreads_{tipo.lower()}"


def _download_activities(shelf, tipo):
    xml = download_text(_rss_url(shelf))
    soup = BeautifulSoup(xml, "xml")
    return parse_rss_items(soup, tipo)


def run():
    header("Goodreads")

    if not GOODREADS_USER_ID:
        warning("GOODREADS_USER_ID não configurado.")
        return

    enviados = 0

    for shelf, tipo in SHELVES:
        info(f"Baixando feed: {shelf}")

        activities = _download_activities(shelf, tipo)

        if not activities:
            warning(f"Nenhuma atividade em {shelf}.")
            continue

        module = _cache_module(tipo)
        ids = [activity["id"] for activity in activities]
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

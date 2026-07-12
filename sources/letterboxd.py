
"""
============================================================
Rezistro
Arquivo: sources/letterboxd.py
Versão: 1.0
============================================================
"""

from bs4 import BeautifulSoup

from config import LETTERBOXD_USER

from core.cache import cache_diff
from core.console import header, info, success, warning
from core.downloader import download_text
from core.telegram import send

from parsers.letterboxd import parse_all
from templates.letterboxd import make_card


MODULE = "letterboxd"

URL = (
    f"https://letterboxd.com/"
    f"{LETTERBOXD_USER}/rss/"
)


def run():

    header("Letterboxd")

    if not LETTERBOXD_USER:

        warning("LETTERBOXD_USER não configurado.")

        return

    info("Baixando feed RSS...")

    xml = download_text(URL)

    soup = BeautifulSoup(
        xml,
        "xml"
    )

    info("Interpretando atividade...")

    activities = parse_all(soup)

    if not activities:
        warning("Nenhuma atividade encontrada.")
        return

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

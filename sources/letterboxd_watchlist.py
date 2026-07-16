"""
Monitor da watchlist do Letterboxd.
"""

from config import LETTERBOXD_USER

from core.console import header, info, warning
from core.downloader import download_html
from core.list_notifier import notify_new_items

from parsers.letterboxd_watchlist import parse
from templates.letterboxd import make_card


MODULE = "letterboxd_watchlist"


def _url():
    return f"https://letterboxd.com/{LETTERBOXD_USER}/activity/"


def run():
    header("Letterboxd • Watchlist")

    if not LETTERBOXD_USER:
        warning("LETTERBOXD_USER não configurado.")
        return

    info("Baixando atividade...")

    soup = download_html(_url())

    info("Interpretando watchlist...")

    activities = parse(soup)

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhuma atividade de watchlist encontrada.",
    )

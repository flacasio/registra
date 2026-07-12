"""
Monitor de usuarios seguidos no Goodreads.
"""

from config import GOODREADS_USER_ID

from core.console import header, info, warning
from core.goodreads import following_page
from core.list_notifier import notify_new_items

from parsers.goodreads_people import parse
from templates.goodreads_people import make_card


MODULE = "goodreads_following"


def run():
    header("Goodreads • Following")

    if not GOODREADS_USER_ID:
        warning("GOODREADS_USER_ID nao configurado.")
        return

    info("Baixando usuarios seguidos...")

    html = following_page()

    info("Interpretando usuarios...")

    activities = parse(html, "following")

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhum usuario seguido encontrado.",
    )

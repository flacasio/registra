"""
Monitor do Banco de Series.
"""

from config import BDS_UID

from core.cache import cache_diff
from core.console import header, info, success, warning
from core.downloader import download_html
from core.telegram import send

from parsers.bds import parse_all
from templates.bds import make_card


MODULE = "bds"

URL = (
    f"https://bancodeseries.com.br/"
    f"index.php?action=userPage&uid={BDS_UID}"
)


def run():
    header("Banco de Series")

    info("Baixando perfil...")

    soup = download_html(URL)

    info("Interpretando atividades...")

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

"""
Monitor do Futez.
"""

from config import FUTEZ_PROFILE_URL, FUTEZ_USER_ID

from core.console import header, info, warning
from core.futez import profile_page
from core.list_notifier import notify_new_items

from parsers.futez import parse
from templates.futez import make_card


MODULE = "futez"
MAX_ACTIVITIES = 10


def run():
    header("Futez")

    if not (FUTEZ_PROFILE_URL or FUTEZ_USER_ID):
        warning("FUTEZ_PROFILE_URL ou FUTEZ_USER_ID nao configurado.")
        return

    info("Baixando perfil...")

    html = profile_page()

    info("Interpretando atividades...")

    activities = parse(html)[:MAX_ACTIVITIES]

    notify_new_items(
        MODULE,
        activities,
        make_card,
        "Nenhuma atividade do Futez encontrada.",
    )

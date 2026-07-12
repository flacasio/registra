"""
Monitor de conquistas da Steam.
"""

from config import STEAM_ACHIEVEMENTS_APPIDS, STEAM_API_KEY, STEAM_USER

from core.cache import cache_current, cache_diff
from core.console import header, info, success, warning
from core.steam import achievement_schema, player_achievements
from core.telegram import send

from parsers.steam_achievements import parse
from templates.steam_achievements import make_card


MODULE = "steam_achievements"


def _appids():
    return [
        appid.strip()
        for appid in STEAM_ACHIEVEMENTS_APPIDS.split(",")
        if appid.strip()
    ]


def run():
    header("Steam • Achievements")

    if not STEAM_USER:
        warning("STEAM_USER nao configurado.")
        return

    if not STEAM_API_KEY:
        warning("STEAM_API_KEY nao configurado.")
        return

    appids = _appids()

    if not appids:
        warning("STEAM_ACHIEVEMENTS_APPIDS nao configurado.")
        return

    enviados = 0

    for appid in appids:
        info(f"Baixando conquistas do jogo {appid}...")

        payload = player_achievements(appid)
        schema = achievement_schema(appid)

        info("Interpretando conquistas...")

        activities = parse(payload, schema, appid)

        if not activities:
            warning(f"Nenhuma conquista encontrada para {appid}.")
            continue

        module = f"{MODULE}_{appid}"
        ids = [activity["id"] for activity in activities]

        if not cache_current(module):
            cache_diff(module, ids)
            warning(
                f"Base inicial de conquistas salva para {appid}. "
                "As proximas conquistas serao notificadas."
            )
            continue

        novos = set(cache_diff(module, ids))

        if not novos:
            warning(f"Nenhuma conquista nova para {appid}.")
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

"""
Monitor de conquistas da Steam.
"""

from time import time

from config import STEAM_ACHIEVEMENTS_APPIDS, STEAM_API_KEY, STEAM_USER

from core.cache import cache_current, cache_diff
from core.console import header, info, success, warning
from core.steam import achievement_schema, player_achievements, recent_games
from core.telegram import send

from parsers.steam_achievements import parse
from templates.steam_achievements import make_card


MODULE = "steam_achievements"
RECOVERY_WINDOW_HOURS = 72


def _configured_appids():
    return [
        appid.strip()
        for appid in STEAM_ACHIEVEMENTS_APPIDS.split(",")
        if appid.strip()
    ]


def _recent_appids():
    try:
        payload = recent_games()
    except Exception as exc:
        warning(f"Nao foi possivel detectar jogos recentes: {exc}")
        return []

    games = payload.get("response", {}).get("games", [])

    appids = [
        str(game.get("appid", "")).strip()
        for game in games
        if game.get("appid")
    ]

    if appids:
        info(f"{len(appids)} jogo(s) recente(s) detectado(s) automaticamente.")

    return appids


def _appids():
    # Jogos recentes sao a fonte principal. A configuracao manual continua
    # funcionando como complemento para jogos que o usuario queira vigiar
    # mesmo sem terem sido jogados recentemente.
    return list(dict.fromkeys(_recent_appids() + _configured_appids()))


def _recover_recent_achievements(activities):
    cutoff = int(time()) - (RECOVERY_WINDOW_HOURS * 60 * 60)

    return [
        activity
        for activity in activities
        if int(activity.get("unlocktime", 0) or 0) >= cutoff
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
        warning(
            "Nenhum jogo recente detectado e "
            "STEAM_ACHIEVEMENTS_APPIDS nao configurado."
        )
        return

    enviados = 0

    for appid in appids:
        info(f"Baixando conquistas do jogo {appid}...")

        try:
            payload = player_achievements(appid)
            schema = achievement_schema(appid)
        except Exception as exc:
            warning(f"Nao foi possivel consultar conquistas de {appid}: {exc}")
            continue

        info("Interpretando conquistas...")

        activities = parse(payload, schema, appid)

        if not activities:
            warning(f"Nenhuma conquista encontrada para {appid}.")
            continue

        module = f"{MODULE}_{appid}"
        ids = [activity["id"] for activity in activities]

        if not cache_current(module):
            cache_diff(module, ids)

            recentes = _recover_recent_achievements(activities)

            if not recentes:
                warning(
                    f"Base inicial de conquistas salva para {appid}. "
                    "As proximas conquistas serao notificadas."
                )
                continue

            warning(
                f"Base inicial salva para {appid}; recuperando "
                f"{len(recentes)} conquista(s) das ultimas "
                f"{RECOVERY_WINDOW_HOURS}h."
            )

            for activity in reversed(recentes):
                info("Montando card de recuperacao...")
                card = make_card(activity)

                info("Enviando Telegram...")
                send(card)
                enviados += 1

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

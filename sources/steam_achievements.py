"""
Monitor de conquistas da Steam.
"""

import json
from time import time

from config import STEAM_ACHIEVEMENTS_APPIDS, STEAM_API_KEY, STEAM_USER

from core.cache import cache_current, cache_save
from core.console import header, info, success, warning
from core.steam import achievement_schema, player_achievements, recent_games
from core.telegram import send

from parsers.steam_achievements import parse
from templates.steam_achievements import make_card


MODULE = "steam_achievements"
RECOVERY_WINDOW_HOURS = 72

# Resgate unico do lote que foi detectado em 08/08/2026, mas nao chegou ao
# Telegram por causa de uma imagem quebrada da Steam CDN. A janela reproduz
# exatamente as 72h que o modulo usou naquela execucao.
RESCUE_APPID = "2142790"
RESCUE_START_UTC = 1785962831  # 2026-08-05 20:47:11 UTC
RESCUE_END_UTC = 1786222031    # 2026-08-08 20:47:11 UTC
RESCUE_MODULE = f"{MODULE}_{RESCUE_APPID}_lost_20260808"


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
    return list(dict.fromkeys(_recent_appids() + _configured_appids()))


def _recover_recent_achievements(activities):
    cutoff = int(time()) - (RECOVERY_WINDOW_HOURS * 60 * 60)

    return [
        activity
        for activity in activities
        if int(activity.get("unlocktime", 0) or 0) >= cutoff
    ]


def _known_ids(module):
    raw = cache_current(module)

    if not raw:
        return []

    try:
        values = json.loads(raw)
    except json.JSONDecodeError:
        values = [raw]

    if not isinstance(values, list):
        values = [values]

    return [str(value) for value in values]


def _save_ids(module, values):
    unique = list(dict.fromkeys(str(value) for value in values))
    cache_save(
        module,
        json.dumps(unique[:500], ensure_ascii=False, indent=4),
    )


def _remember(module, achievement_id):
    known = _known_ids(module)
    achievement_id = str(achievement_id)

    if achievement_id in known:
        return

    _save_ids(module, [achievement_id] + known)


def _unseen(module, activities):
    known = set(_known_ids(module))
    return [
        activity
        for activity in activities
        if str(activity["id"]) not in known
    ]


def _deliver(module, activity, recovery=False):
    if recovery:
        info("Montando card de recuperacao...")
    else:
        info("Montando card...")

    card = make_card(activity)

    info("Enviando Telegram...")
    send(card)

    # A conquista so passa a ser conhecida depois que o Telegram confirmou
    # o envio. Se qualquer etapa acima falhar, ela continua pendente para a
    # proxima execucao.
    _remember(module, activity["id"])


def _rescue_lost_batch(appid, activities):
    if appid != RESCUE_APPID:
        return 0

    delivered = set(_known_ids(RESCUE_MODULE))
    rescue = [
        activity
        for activity in activities
        if RESCUE_START_UTC <= int(activity.get("unlocktime", 0) or 0) <= RESCUE_END_UTC
        and str(activity["id"]) not in delivered
    ]

    if not rescue:
        return 0

    warning(
        f"Resgatando {len(rescue)} conquista(s) perdidas do lote de 08/08/2026."
    )

    enviados = 0

    for activity in reversed(rescue):
        info("Montando card de resgate historico...")
        card = make_card(activity)

        info("Enviando Telegram...")
        send(card)

        # Marcador separado do cache normal. Assim este resgate e idempotente:
        # cada conquista do lote e enviada no maximo uma vez.
        _remember(RESCUE_MODULE, activity["id"])
        enviados += 1

    return enviados


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

        # O lote perdido e tratado por um marcador proprio, independente do
        # cache normal que ja havia considerado essas conquistas como vistas.
        enviados += _rescue_lost_batch(appid, activities)

        module = f"{MODULE}_{appid}"

        if not cache_current(module):
            recentes = _recover_recent_achievements(activities)
            recent_ids = {activity["id"] for activity in recentes}

            # Na primeira observacao, conquistas antigas entram como base sem
            # gerar notificacao. As recentes ficam fora do cache ate serem
            # efetivamente entregues.
            antigos = [
                activity["id"]
                for activity in activities
                if activity["id"] not in recent_ids
            ]
            _save_ids(module, antigos)

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
                _deliver(module, activity, recovery=True)
                enviados += 1

            continue

        novas = _unseen(module, activities)

        if not novas:
            warning(f"Nenhuma conquista nova para {appid}.")
            continue

        for activity in reversed(novas):
            _deliver(module, activity)
            enviados += 1

    if enviados:
        success(f"{enviados} card(s) enviado(s).")
    else:
        warning("Nenhuma novidade.")

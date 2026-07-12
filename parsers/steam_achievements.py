"""
Interpretar conquistas da Steam.
"""

from config import STEAM_USER


def _schema_map(schema):
    game = schema.get("game", {})
    stats = game.get("availableGameStats", {})
    achievements = stats.get("achievements", [])

    return {
        achievement.get("name"): achievement
        for achievement in achievements
    }, game.get("gameName", "Jogo da Steam")


def parse(payload, schema, appid):
    playerstats = payload.get("playerstats", {})
    achievements = playerstats.get("achievements", [])
    details, schema_game_name = _schema_map(schema)
    game_name = playerstats.get("gameName") or schema_game_name
    activities = []

    for item in achievements:
        if not item.get("achieved"):
            continue

        apiname = item.get("apiname") or item.get("name")
        detail = details.get(apiname, {})
        unlocktime = item.get("unlocktime", 0)
        name = (
            detail.get("displayName")
            or item.get("name")
            or apiname
            or "Conquista"
        )

        activities.append({
            "id": f"{appid}_{apiname}_{unlocktime}",
            "tipo": "ACHIEVEMENT",
            "appid": str(appid),
            "apiname": apiname,
            "game": game_name,
            "name": name,
            "description": detail.get("description", ""),
            "icon": detail.get("icon", ""),
            "game_cover": "",
            "unlocktime": int(unlocktime or 0),
            "url": (
                f"https://steamcommunity.com/id/{STEAM_USER}/"
                f"stats/{appid}/achievements/"
            ),
        })

    return sorted(
        activities,
        key=lambda activity: activity["unlocktime"],
        reverse=True,
    )

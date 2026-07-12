"""
Interpretar listas de jogos da Steam.
"""

import json
import re

from bs4 import BeautifulSoup


def _clean(text):
    return " ".join(str(text or "").split())


def _game_url(appid):
    return f"https://store.steampowered.com/app/{appid}/"


def _from_json(html, tipo):
    match = re.search(r"rgGames\s*=\s*(\[[\s\S]*?\]);", html)

    if not match:
        return []

    try:
        games = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []

    activities = []

    for game in games:
        appid = str(game.get("appid") or game.get("app_id") or "")
        name = _clean(game.get("name") or game.get("title"))

        if not appid or not name:
            continue

        hours = (
            game.get("hours_forever")
            or game.get("hours")
            or game.get("playtime_forever")
            or ""
        )

        activities.append({
            "id": f"{tipo}_{appid}",
            "tipo": tipo,
            "appid": appid,
            "title": name,
            "hours": str(hours),
            "url": _game_url(appid),
        })

    return activities


def _from_html(html, tipo):
    soup = BeautifulSoup(html, "html.parser")
    activities = []

    for row in soup.select("[data-appid], [data-app-id], .gameListRow, .gameListRowItem"):
        appid = (
            row.get("data-appid")
            or row.get("data-app-id")
            or ""
        )

        if not appid:
            link = row.select_one("a[href*='/app/']")
            href = link.get("href", "") if link else ""
            match = re.search(r"/app/(\d+)", href)
            appid = match.group(1) if match else ""

        title_node = (
            row.select_one(".gameListRowItemName")
            or row.select_one(".gameListRowLogo + div")
            or row.select_one("a[href*='/app/']")
        )
        title = _clean(title_node.get_text(" ", strip=True) if title_node else "")

        if not appid or not title:
            continue

        hours_node = row.select_one(".hours_played, .gameListRowHours")
        hours = _clean(hours_node.get_text(" ", strip=True) if hours_node else "")

        activities.append({
            "id": f"{tipo}_{appid}",
            "tipo": tipo,
            "appid": appid,
            "title": title,
            "hours": hours,
            "url": _game_url(appid),
        })

    seen = set()
    unique = []

    for activity in activities:
        if activity["id"] in seen:
            continue

        seen.add(activity["id"])
        unique.append(activity)

    return unique


def parse(html, tipo):
    return _from_json(html, tipo) or _from_html(html, tipo)


def parse_owned(data, tipo="STEAM_NEW"):
    games = data.get("response", {}).get("games", [])
    activities = []

    for game in games:
        appid = str(game.get("appid") or "")
        title = _clean(game.get("name"))

        if not appid or not title:
            continue

        minutes = int(game.get("playtime_forever", 0) or 0)

        if minutes:
            hours = f"{minutes // 60}h {minutes % 60}min"
        else:
            hours = "Sem tempo registrado"

        activities.append({
            "id": f"{tipo}_{appid}",
            "tipo": tipo,
            "appid": appid,
            "title": title,
            "hours": hours,
            "url": _game_url(appid),
        })

    return activities

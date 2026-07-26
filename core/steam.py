"""
============================================================
Rezistro
Arquivo: core/steam.py
Versão: 2.0
============================================================

Responsabilidade:
Centralizar toda a comunicação com a Steam.

Este módulo deve conhecer apenas
como conversar com a plataforma.

Os parsers, templates e sources
não devem conhecer URLs da Steam.
"""

import requests

from config import (
    STEAM_API_KEY,
    STEAM_USER,
)


# ==========================================================
# RESOLVE STEAM ID
# ==========================================================

def resolve_steamid():
    """
    Resolve um SteamID64.

    STEAM_USER pode ser:
    - Vanity URL
    - SteamID64
    """

    if STEAM_USER.isdigit():
        return STEAM_USER

    response = requests.get(

        "https://api.steampowered.com/"
        "ISteamUser/"
        "ResolveVanityURL/v0001/",

        params={

            "key": STEAM_API_KEY,

            "vanityurl": STEAM_USER

        },

        timeout=30

    )

    response.raise_for_status()

    data = response.json()["response"]

    if data.get("success") != 1:

        raise RuntimeError(
            "Não foi possível resolver o SteamID."
        )

    return data["steamid"]


# ==========================================================
# RECENT GAMES
# ==========================================================

def recent_games():

    steamid = resolve_steamid()

    response = requests.get(

        "https://api.steampowered.com/"
        "IPlayerService/"
        "GetRecentlyPlayedGames/"
        "v0001/",

        params={

            "key": STEAM_API_KEY,

            "steamid": steamid,

            "format": "json"

        },

        timeout=30

    )

    response.raise_for_status()

    return response.json()


def owned_games():

    steamid = resolve_steamid()

    response = requests.get(

        "https://api.steampowered.com/"
        "IPlayerService/"
        "GetOwnedGames/"
        "v0001/",

        params={

            "key": STEAM_API_KEY,

            "steamid": steamid,

            "format": "json",

            "include_appinfo": 1,

            "include_played_free_games": 1,

        },

        timeout=30

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# ACHIEVEMENTS
# ==========================================================

def player_achievements(appid):

    steamid = resolve_steamid()

    response = requests.get(

        "https://api.steampowered.com/"
        "ISteamUserStats/"
        "GetPlayerAchievements/"
        "v0001/",

        params={

            "key": STEAM_API_KEY,

            "steamid": steamid,

            "appid": appid,

            "l": "brazilian",

            "format": "json"

        },

        timeout=30

    )

    response.raise_for_status()

    return response.json()


def achievement_schema(appid):

    response = requests.get(

        "https://api.steampowered.com/"
        "ISteamUserStats/"
        "GetSchemaForGame/"
        "v2/",

        params={

            "key": STEAM_API_KEY,

            "appid": appid,

            "l": "brazilian",

            "format": "json"

        },

        timeout=30

    )

    response.raise_for_status()

    return response.json()


def achievements_page(appid):

    return (
        f"https://steamcommunity.com/id/{STEAM_USER}/"
        f"stats/{appid}/achievements/"
    )


# ==========================================================
# GAME DETAILS
# ==========================================================

def game_details(appid):

    response = requests.get(

        "https://store.steampowered.com/api/appdetails",

        params={

            "appids": appid,

            "cc": "br",

            "l": "brazilian"

        },

        timeout=30

    )

    response.raise_for_status()

    payload = response.json()

    game = payload.get(str(appid))

    if not game:

        raise RuntimeError(
            "Jogo não encontrado."
        )

    if not game.get("success"):

        raise RuntimeError(
            "Steam não retornou dados."
        )

    data = game["data"]

    price = {

        "original": None,

        "current": None,

        "discount": 0

    }

    overview = data.get("price_overview")

    if overview:

        price = {

            "original":
                overview.get("initial", 0) / 100,

            "current":
                overview.get("final", 0) / 100,

            "discount":
                overview.get(
                    "discount_percent",
                    0
                )

        }

    return {

        "appid": appid,

        "name":
            data.get(
                "name",
                "Jogo desconhecido"
            ),

        "url":
            f"https://store.steampowered.com/app/{appid}/",

        "price":
            price

    }


# ==========================================================
# WISHLIST
# ==========================================================

STORE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,application/json;q=0.8,*/*;q=0.7"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}


def wishlist():

    response = requests.get(

        f"https://store.steampowered.com/wishlist/id/{STEAM_USER}",

        params={

            "sort": "dateadded"

        },

        timeout=30,

        headers=STORE_HEADERS

    )

    response.raise_for_status()

    return response.text


def wishlist_json():
    urls = [
        f"https://store.steampowered.com/wishlist/id/{STEAM_USER}/wishlistdata/",
    ]

    try:
        steamid = resolve_steamid()
        urls.append(
            f"https://store.steampowered.com/wishlist/profiles/{steamid}/wishlistdata/"
        )
    except Exception:
        pass

    last_error = None
    empty_payload = None

    for url in urls:
        response = requests.get(
            url,
            timeout=30,
            headers=STORE_HEADERS
        )

        try:
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            continue

        # A Steam pode responder {} no endpoint de vanity mesmo quando
        # o endpoint por SteamID64 contém a wishlist completa.
        if data:
            return data

        empty_payload = data

    # Se todos os endpoints responderem JSON vazio, preserva a possibilidade
    # de a wishlist estar realmente vazia. Erros só vencem quando nenhum
    # endpoint retornou sequer um JSON válido.
    if empty_payload is not None:
        return empty_payload

    if last_error:
        raise last_error

    raise RuntimeError("Wishlist da Steam não retornou dados.")


# ==========================================================
# COMMUNITY PAGES
# ==========================================================

COMMUNITY_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
    )
}


def community_page(path):

    response = requests.get(

        f"https://steamcommunity.com/id/{STEAM_USER}/{path}",

        timeout=30,

        headers=COMMUNITY_HEADERS

    )

    response.raise_for_status()

    return response.text


def games_all():

    return community_page("games/?tab=all")


def games_perfect():

    return community_page("games/?tab=perfect")


def awards():

    return community_page("awards/")


def badges():

    return community_page("badges/")


def screenshots():

    return community_page("screenshots/")


def friends():

    return community_page("friends/")

# ==========================================================
# REVIEWS
# ==========================================================

def reviews():

    response = requests.get(

        f"https://steamcommunity.com/id/{STEAM_USER}/recommended",

        timeout=30,

        headers={

            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )

        }

    )

    response.raise_for_status()

    return response.text


# ==========================================================
# COMMENTS
# ==========================================================

def comments(count=10):

    steamid = resolve_steamid()

    response = requests.get(

        f"https://steamcommunity.com/comment/Profile/render/{steamid}/-1/",

        params={

            "start": 0,

            "count": count,

            "sessionid": "",

            "feature2": -1

        },

        timeout=30,

        headers={

            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )

        }

    )

    response.raise_for_status()

    return response.json()

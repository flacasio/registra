"""
============================================================
Rezistro
Arquivo: parsers/steam.py
Versão: 1.0
============================================================

Responsabilidade:
Interpretar a resposta da API
GetRecentlyPlayedGames da Steam.

Recebe:
    dict (JSON)

Retorna:
    dict
"""


def _parse_game(jogo):
    appid = jogo["appid"]

    return {

        "id":
            f"{appid}_{jogo.get('playtime_forever', 0)}",

        "tipo":
            "RECENT_PLAY",

        "appid":
            appid,

        "titulo":
            jogo.get(
                "name",
                "Jogo desconhecido"
            ),

        "tempo_total":
            jogo.get(
                "playtime_forever",
                0
            ),

        "tempo_recente":
            jogo.get(
                "playtime_2weeks",
                0
            ),

        "url":
            (
                "https://store.steampowered.com/app/"
                f"{appid}/"
            )

    }


def parse_all(data):

    response = data.get("response", {})

    games = response.get("games", [])

    return [
        _parse_game(jogo)
        for jogo in games
    ]


def parse(data):
    activities = parse_all(data)

    if not activities:
        raise RuntimeError(
            "Nenhum jogo recente encontrado."
        )

    return activities[0]

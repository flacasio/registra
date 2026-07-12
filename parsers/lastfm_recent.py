"""
============================================================
Rezistro
Arquivo: parsers/lastfm_recent.py
Versão: 2.0
============================================================

Responsabilidade:
Interpretar uma música recentemente
escutada no Last.fm.
"""


def parse(track):

    if not track:

        raise RuntimeError(
            "Nenhuma música encontrada."
        )

    nowplaying = "@attr" in track

    if nowplaying:

        track_id = f"now_{track['name']}"

        timestamp = None

    else:

        timestamp = int(
            track["date"]["uts"]
        )

        track_id = str(timestamp)

    return {

        "id":
            track_id,

        "tipo":
            "RECENT",

        "titulo":
            track["name"],

        "artista":
            track["_artist"],

        "album":
            track["_album"],

        "capa":
            track["_cover"],

        "url":
            track["_url"],

        "timestamp":
            timestamp

    }
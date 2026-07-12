"""
============================================================
Rezistro
Arquivo: parsers/lastfm_loved.py
Versão: 2.0
============================================================

Responsabilidade:
Interpretar uma música favoritada
no Last.fm.
"""


def parse(track):

    if not track:

        raise RuntimeError(
            "Nenhuma música encontrada."
        )

    timestamp = int(
        track["date"]["uts"]
    )

    return {

        "id":
            str(timestamp),

        "tipo":
            "LOVED",

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
"""
============================================================
Rezistro
Arquivo: core/lastfm.py
Versão: 2.0
============================================================

Responsabilidade:
Centralizar toda comunicação com
a API do Last.fm.
"""

import requests

from config import (
    LASTFM_API_KEY,
    LASTFM_USER,
)


API = "https://ws.audioscrobbler.com/2.0/"


# ==========================================================
# REQUEST
# ==========================================================

def _request(method, **params):

    response = requests.get(

        API,

        params={

            "method": method,

            "api_key": LASTFM_API_KEY,

            "format": "json",

            **params

        },

        timeout=30

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# RECENT TRACK
# ==========================================================

def recent_tracks(limit=10):

    data = _request(

        "user.getrecenttracks",

        user=LASTFM_USER,

        limit=limit

    )

    tracks = (

        data

        .get("recenttracks", {})

        .get("track", [])

    )

    if isinstance(tracks, dict):
        tracks = [tracks]

    if not tracks:

        return []

    return [
        enrich_track(track)
        for track in tracks
    ]



def recent_track():
    tracks = recent_tracks(limit=1)
    return tracks[0] if tracks else None


# ==========================================================
# LOVED TRACK
# ==========================================================

def loved_tracks(limit=10):

    data = _request(

        "user.getlovedtracks",

        user=LASTFM_USER,

        limit=limit

    )

    tracks = (

        data

        .get("lovedtracks", {})

        .get("track", [])

    )

    if isinstance(tracks, dict):
        tracks = [tracks]

    if not tracks:

        return []

    return [
        enrich_track(track)
        for track in tracks
    ]



def loved_track():
    tracks = loved_tracks(limit=1)
    return tracks[0] if tracks else None


# ==========================================================
# TRACK INFO
# ==========================================================

def track_info(artist, track):

    data = _request(

        "track.getInfo",

        artist=artist,

        track=track

    )

    return data.get(

        "track",

        {}

    )


# ==========================================================
# ENRICH TRACK
# ==========================================================

def enrich_track(track):

    artist_data = track.get("artist", {})

    artist = (
        artist_data.get("#text")
        or artist_data.get("name")
        or "Artista desconhecido"
    )

    info = track_info(
        artist,
        track["name"]
    )

    album = info.get("album") or {}

    images = album.get("image")
    if not isinstance(images, list):
        images = []

    cover = ""
    if images:
        cover = images[-1].get("#text", "")

    if not cover:
        images = track.get("image", [])
        if images:
            cover = images[-1].get("#text", "")

    enriched = track.copy()

    enriched["_cover"] = cover
    enriched["_artist"] = artist
    enriched["_url"] = info.get("url", "")
    enriched["_album"] = album.get(
        "title",
        track.get("album", {}).get("#text", "")
    )

    return enriched

# ==========================================================
# COMMENTS
# ==========================================================

def comments():

    url = (
        f"https://www.last.fm/pt/user/"
        f"{LASTFM_USER}/partial/shoutbox?ajax=1"
    )

    session = requests.Session()

    session.headers.update({

        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) "
            "Gecko/20100101 Firefox/152.0"
        ),

        "Referer": (
            f"https://www.last.fm/pt/user/{LASTFM_USER}"
        ),

        "X-Requested-With": "XMLHttpRequest",

        "Accept": "*/*",
    })

    # visita primeiro a página do perfil
    session.get(
        f"https://www.last.fm/pt/user/{LASTFM_USER}",
        timeout=30
    )

    response = session.get(
        url,
        timeout=30
    )

    print(response.status_code)

    return response.text

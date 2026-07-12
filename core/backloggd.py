"""
============================================================
Rezistro
Arquivo: core/backloggd.py
============================================================
"""

import requests

from config import (
    BACKLOGGD_USER,
)


HEADERS = {

    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),

    "Referer": "https://www.backloggd.com/",
}


def activity():

    response = requests.get(

        f"https://www.backloggd.com/u/{BACKLOGGD_USER}/activity/",

        headers=HEADERS,

        timeout=30

    )

    response.raise_for_status()

    return response.text


def game_cover(game_url):
    if game_url.startswith("/"):
        game_url = f"https://www.backloggd.com{game_url}"

    response = requests.get(
        game_url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    image = soup.find(
        "img",
        class_="game-cover"
    )

    if image and image.get("src"):
        return image["src"]

    meta = soup.find(
        "meta",
        property="og:image"
    )

    if meta and meta.get("content"):
        return meta["content"]

    return None

"""
Interpretar paginas de notas do AOTY.
"""

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE_URL = "https://www.albumoftheyear.org"


def _text(node, selector):
    found = node.select_one(selector)
    return found.get_text(" ", strip=True) if found else ""


def _image_url(img):
    if not img:
        return ""

    # As paginas de notas do AOTY usam lazy-loading e podem deixar um
    # placeholder em src/srcset. Os atributos data-* guardam a capa real.
    for attribute in (
        "data-src",
        "data-lazy-src",
        "data-original",
        "data-srcset",
        "srcset",
        "src",
    ):
        value = img.get(attribute, "")

        if not value:
            continue

        for candidate in str(value).split(","):
            image_url = candidate.strip().split(" ")[0]

            if not image_url or image_url.startswith(("data:", "blob:")):
                continue

            return urljoin(BASE_URL, image_url)

    return ""


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    ratings = []

    for block in soup.find_all("div", class_=re.compile(r"\balbumBlock\b")):
        artist = _text(block, ".artistTitle")
        album = _text(block, ".albumTitle")
        rating = _text(block, ".rating")
        image = _image_url(block.find("img"))
        link = block.find("a", href=re.compile(r"^/album/"))
        album_url = urljoin(BASE_URL, link["href"]) if link else ""

        if not album or not rating or not album_url:
            continue

        ratings.append({
            "id": album_url,
            "artist": artist,
            "album": album,
            "rating": rating,
            "image": image,
            "url": album_url,
        })

    return ratings

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

    srcset = img.get("srcset", "")

    if srcset:
        first = srcset.split(",")[0].strip().split(" ")[0]

        if first:
            return urljoin(BASE_URL, first)

    return urljoin(
        BASE_URL,
        img.get("data-src") or img.get("src") or "",
    )


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

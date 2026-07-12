"""
Interpretar avaliacoes recentes do Album of the Year.
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


def _is_best_of_block(block):
    return block.find_parent("section") is not None


def parse(html):
    if isinstance(html, str):
        html = BeautifulSoup(html, "html.parser")

    activities = []

    for block in html.find_all("div", class_="albumBlock five"):
        if _is_best_of_block(block):
            continue

        artist = _text(block, ".artistTitle")
        album = _text(block, ".albumTitle")
        rating = _text(block, ".rating")
        relative_time = _text(block, ".ratingText")
        kind = _text(block, ".type")
        image = _image_url(block.find("img"))
        link = block.find("a", href=re.compile(r"^/album/"))
        album_url = urljoin(BASE_URL, link["href"]) if link else ""

        if not album or not rating:
            continue

        activity_id = "|".join(
            part for part in (album_url, rating, relative_time) if part
        )

        activities.append({
            "id": activity_id,
            "artist": artist,
            "album": album,
            "rating": rating,
            "relative_time": relative_time,
            "kind": kind,
            "image": image,
            "url": album_url,
        })

    return activities

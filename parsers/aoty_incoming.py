"""
Interpretar lista publica de lancamentos futuros no AOTY.
"""

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE_URL = "https://www.albumoftheyear.org"


def _clean(text):
    return " ".join(str(text or "").split())


def _text(node, selector):
    found = node.select_one(selector)
    return _clean(found.get_text(" ", strip=True)) if found else ""


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


def _extra_lines(block, artist, album):
    ignored = {
        artist,
        album,
    }
    lines = []

    selectors = [
        ".listComment",
        ".comment",
        ".description",
        ".notes",
        ".date",
        ".releaseDate",
        ".albumDate",
    ]

    for selector in selectors:
        for node in block.select(selector):
            text = _clean(node.get_text(" ", strip=True))

            if text and text not in ignored and text not in lines:
                lines.append(text)

    if lines:
        return lines

    raw_lines = [
        _clean(line)
        for line in block.get_text("\n", strip=True).splitlines()
    ]

    for line in raw_lines:
        if not line or line in ignored or line in lines:
            continue

        if line == "Upcoming" or line == "List":
            continue

        lines.append(line)

    return lines[:6]


def _parse_block(block):
    artist = _text(block, ".artistTitle")
    album = _text(block, ".albumTitle")
    link = block.find("a", href=re.compile(r"^/album/"))

    if not album and link:
        album = _clean(link.get_text(" ", strip=True))

    album_url = urljoin(BASE_URL, link["href"]) if link else ""

    if not artist:
        artist_link = block.find("a", href=re.compile(r"^/artist/"))
        artist = _clean(artist_link.get_text(" ", strip=True)) if artist_link else ""

    if not album or not album_url:
        return None

    return {
        "id": album_url,
        "artist": artist,
        "album": album,
        "image": _image_url(block.find("img")),
        "url": album_url,
        "extra_lines": _extra_lines(block, artist, album),
    }


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    activities = []
    seen = set()

    blocks = soup.find_all("div", class_=re.compile(r"\balbumBlock\b"))

    if not blocks:
        blocks = [
            link.find_parent(["div", "li", "tr"])
            for link in soup.find_all("a", href=re.compile(r"^/album/"))
        ]

    for block in blocks:
        if not block:
            continue

        activity = _parse_block(block)

        if not activity or activity["id"] in seen:
            continue

        seen.add(activity["id"])
        activities.append(activity)

    return activities

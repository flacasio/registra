"""
Interpretar lista publica de lancamentos futuros no AOTY.
"""

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE_URL = "https://www.albumoftheyear.org"


IMAGE_ATTRS = (
    "data-src",
    "data-original",
    "data-lazy-src",
    "data-img-url",
    "src",
)

SRCSET_ATTRS = (
    "data-srcset",
    "srcset",
)


def _clean(text):
    return " ".join(str(text or "").split())


def _text(node, selector):
    found = node.select_one(selector)
    return _clean(found.get_text(" ", strip=True)) if found else ""


def _absolute_image_url(value):
    value = str(value or "").strip()

    if not value or value.startswith("data:"):
        return ""

    return urljoin(BASE_URL, value)


def _srcset_url(value):
    value = str(value or "").strip()

    if not value:
        return ""

    candidates = []

    for part in value.split(","):
        url = part.strip().split(" ")[0]

        if url:
            candidates.append(url)

    # A ultima opcao costuma ser a maior imagem do srcset.
    for candidate in reversed(candidates):
        url = _absolute_image_url(candidate)

        if url:
            return url

    return ""


def _style_image_url(style):
    match = re.search(r"url\((['\"]?)(.*?)\1\)", str(style or ""))

    if not match:
        return ""

    return _absolute_image_url(match.group(2))


def _node_image_url(node):
    if not node:
        return ""

    for attr in SRCSET_ATTRS:
        url = _srcset_url(node.get(attr, ""))

        if url:
            return url

    for attr in IMAGE_ATTRS:
        url = _absolute_image_url(node.get(attr, ""))

        if url:
            return url

    return _style_image_url(node.get("style", ""))


def _image_url(block):
    selectors = [
        ".albumCover source",
        ".albumCover img",
        ".cover source",
        ".cover img",
        "picture source",
        "picture img",
        "img",
        "[style*=url]",
    ]

    for selector in selectors:
        for node in block.select(selector):
            url = _node_image_url(node)

            if url:
                return url

    return ""


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
        "image": _image_url(block),
        "url": album_url,
        "extra_lines": _extra_lines(block, artist, album),
    }


def _block_for_album_link(link):
    block = link

    for _ in range(8):
        block = block.find_parent(["div", "li", "tr"])

        if not block:
            return None

        if _image_url(block) or block.select_one(".artistTitle, .albumTitle"):
            return block

    return None


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    activities = []
    seen = set()

    blocks = soup.find_all("div", class_=re.compile(r"\balbumBlock\b"))

    if not blocks:
        blocks = [
            _block_for_album_link(link)
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
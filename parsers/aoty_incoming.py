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


def _release_date(block):
    selectors = (
        ".releaseDate",
        ".albumDate",
        ".date",
    )

    candidates = []

    for selector in selectors:
        for node in block.select(selector):
            text = _clean(node.get_text(" ", strip=True))

            if text and text not in candidates:
                candidates.append(text)

    if not candidates:
        candidates = [
            _clean(line)
            for line in block.get_text("\n", strip=True).splitlines()
        ]

    # O AOTY pode repetir a data em versoes visual e acessivel do mesmo bloco.
    # Mantemos somente a primeira data real encontrada, normalizada para dia/mes.
    for text in candidates:
        numeric = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/\d{2,4})?\b", text)

        if numeric:
            return f"{int(numeric.group(1)):02d}/{int(numeric.group(2)):02d}"

        named = re.search(
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+(\d{1,2})\b",
            text,
            re.IGNORECASE,
        )

        if named:
            month_match = re.search(
                r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)",
                text,
                re.IGNORECASE,
            )
            months = {
                "jan": 1,
                "feb": 2,
                "mar": 3,
                "apr": 4,
                "may": 5,
                "jun": 6,
                "jul": 7,
                "aug": 8,
                "sep": 9,
                "sept": 9,
                "oct": 10,
                "nov": 11,
                "dec": 12,
            }
            month = months[month_match.group(1).lower()]
            day = int(named.group(1))
            return f"{day:02d}/{month:02d}"

    return ""


def _parse_block(block):
    artist = _text(block, ".artistTitle")
    album = _text(block, ".albumTitle")
    link = block.find("a", href=re.compile(r"^/album/"))

    if not album and link:
        album = _clean(link.get_text(" ", strip=True))

    # Alguns cards do AOTY incluem o ano como sufixo do titulo.
    album = re.sub(r"\s+\d{4}$", "", album).strip()

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
        "release_date": _release_date(block),
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

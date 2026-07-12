"""
Interpretar atividades publicas do Futez.

Esta primeira versao usa um parser tolerante, porque o formato final da pagina
precisa ser calibrado com a URL real do perfil.
"""

import hashlib
import re
from urllib.parse import urljoin


BASE_URL = "https://futez.com.br"
MAX_TEXT_LENGTH = 280


def _normalize(text):
    return " ".join(str(text).split())


def _first_image(item):
    image = item.find("img")

    if not image:
        return ""

    return image.get("src") or image.get("data-src") or ""


def _first_link(item):
    link = item.find("a", href=True)

    if not link:
        return ""

    return urljoin(BASE_URL, link["href"])


def _title_from_text(text):
    if not text:
        return "Nova atividade"

    sentence = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0]
    return sentence[:MAX_TEXT_LENGTH].strip()


def _activity_id(text, url):
    seed = "|".join(part for part in (url, text[:MAX_TEXT_LENGTH]) if part)
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()


def _candidate_items(html):
    selectors = [
        "article",
        "li",
        "[class*=activity]",
        "[class*=post]",
        "[class*=feed]",
        "[class*=card]",
    ]

    seen = set()

    for selector in selectors:
        for item in html.select(selector):
            marker = id(item)

            if marker in seen:
                continue

            seen.add(marker)
            yield item


def parse(html):
    if html is None:
        return []

    activities = []
    seen_ids = set()

    for item in _candidate_items(html):
        text = _normalize(item.get_text(" ", strip=True))

        if len(text) < 8:
            continue

        url = _first_link(item)
        activity_id = _activity_id(text, url)

        if activity_id in seen_ids:
            continue

        seen_ids.add(activity_id)

        activities.append({
            "id": activity_id,
            "title": _title_from_text(text),
            "text": text[:MAX_TEXT_LENGTH],
            "url": url,
            "image": _first_image(item),
        })

    return activities

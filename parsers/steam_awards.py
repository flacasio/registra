"""
Interpretar premios recebidos na Steam.
"""

import re
import hashlib
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE_URL = "https://steamcommunity.com"

AWARD_TRANSLATIONS = {
    "Beautiful": "Bonito",
    "Clever": "Esperto",
    "Deep Thoughts": "Pensamentos profundos",
    "Fancy Pants": "Elegante",
    "Heartwarming": "Reconfortante",
    "Hilarious": "Hilario",
    "Jester": "Bobo da corte",
    "Michelangelo": "Michelangelo",
    "Mind Blown": "Mente explodida",
    "One Hundred": "Cem",
    "Poetry": "Poesia",
    "Saucy": "Atrevido",
    "Slow Clap": "Aplauso lento",
    "Super Star": "Superestrela",
    "Take My Points": "Leve meus pontos",
    "Treasure": "Tesouro",
    "Warm Blanket": "Cobertor quentinho",
    "Wholesome": "Fofo",
    "Wild": "Selvagem",
}


def _clean(text):
    return " ".join(str(text or "").split())


def _translate_award(title):
    return AWARD_TRANSLATIONS.get(title, title)


def _image_url(image):
    if not image:
        return ""

    url = (
        image.get("src")
        or image.get("data-src")
        or image.get("data-original")
        or ""
    )

    if not url and image.get("srcset"):
        url = image["srcset"].split()[0]

    return urljoin(BASE_URL, url)


def _award_count(text):
    match = re.search(r"\((x\d+)\)", text, flags=re.I)
    return match.group(1).lower() if match else ""


def _stable_id(title, text):
    seed = "|".join(
        part.lower()
        for part in (
            _clean(title),
            _award_count(text),
        )
        if part
    )
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    activities = []

    selectors = [
        ".profile_awards .profile_award",
        ".award_card",
        "[class*='award']",
    ]

    for selector in selectors:
        for item in soup.select(selector):
            text = _clean(item.get_text(" ", strip=True))
            image = item.select_one("img")
            title = image.get("alt", "") if image else ""
            title = _clean(title or text)
            title = _translate_award(title)

            if not title:
                continue

            image_url = _image_url(image)
            item_id = (
                item.get("id")
                or item.get("data-award-id")
                or _stable_id(title, text)
            )

            activities.append({
                "id": f"award_{item_id}",
                "title": title,
                "text": "",
                "image": image_url,
                "url": re.sub(r"\?.*$", "", "https://steamcommunity.com/"),
            })

        if activities:
            break

    return activities

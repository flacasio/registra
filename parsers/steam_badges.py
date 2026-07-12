"""
Interpretar insignias da Steam.
"""

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE_URL = "https://steamcommunity.com"

BADGE_TRANSLATIONS = {
    "Community Ambassador": "Embaixador da Comunidade",
    "Community Ambassador - Legacy": "Embaixador da Comunidade - Legado",
    "Community Contributor": "Colaborador da Comunidade",
    "Community Contributor - Legacy": "Colaborador da Comunidade - Legado",
    "Community Leader": "Lider da Comunidade",
    "Community Leader - Legacy": "Lider da Comunidade - Legado",
    "Community Patron": "Patrono da Comunidade",
    "Community Patron - Legacy": "Patrono da Comunidade - Legado",
    "Years of Service": "Anos de Servico",
}


def _clean(text):
    return " ".join(str(text or "").split())


def _image_from_srcset(value):
    if not value:
        return ""

    return value.split(",")[0].strip().split()[0]


def _image_from_style(value):
    if not value:
        return ""

    match = re.search(r"url\(['\"]?([^'\")]+)", value)
    return match.group(1) if match else ""


def _image_url(badge):
    image = badge.select_one("img")

    if image:
        url = (
            image.get("src")
            or image.get("data-src")
            or image.get("data-original")
            or _image_from_srcset(image.get("srcset"))
        )

        if url:
            return urljoin(BASE_URL, url)

    styled = badge.select_one("[style*='background']")

    if styled:
        url = _image_from_style(styled.get("style", ""))

        if url:
            return urljoin(BASE_URL, url)

    return ""


def _title(text):
    cleaned = _clean(text)
    cleaned = re.sub(r"\s*(View details|Ver detalhes)\s*$", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\bView details\b", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\bVer detalhes\b", "", cleaned, flags=re.I)
    cleaned = _clean(cleaned)
    return BADGE_TRANSLATIONS.get(cleaned, cleaned)


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    activities = []

    for badge in soup.select(".badge_row, .badge_card_set_card, [class*='badge_row']"):
        link = badge.select_one("a[href*='/badges/']")
        title_node = (
            badge.select_one(".badge_title")
            or badge.select_one(".badge_info_title")
            or link
        )
        title = _title(title_node.get_text(" ", strip=True) if title_node else "")

        if not title:
            continue

        url = link.get("href", "") if link else ""
        url = urljoin(BASE_URL, url)
        image_url = _image_url(badge)
        item_id = url or title

        activities.append({
            "id": f"badge_{item_id}",
            "title": title,
            "image": image_url,
            "url": url,
        })

    return activities

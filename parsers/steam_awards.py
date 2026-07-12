"""
Interpretar premios recebidos na Steam.
"""

import re

from bs4 import BeautifulSoup


def _clean(text):
    return " ".join(str(text or "").split())


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

            if not title:
                continue

            image_url = image.get("src", "") if image else ""
            item_id = item.get("id") or item.get("data-award-id") or f"{title}|{image_url}|{text}"

            activities.append({
                "id": f"award_{item_id}",
                "title": title,
                "text": text,
                "image": image_url,
                "url": re.sub(r"\?.*$", "", "https://steamcommunity.com/"),
            })

        if activities:
            break

    return activities

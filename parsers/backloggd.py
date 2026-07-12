"""
Interpretar atividades recentes do Backloggd.
"""

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE_URL = "https://www.backloggd.com"

ACTION_MAP = {
    "abandoned": "ABANDONED",
    "completed": "COMPLETED",
    "now playing": "PLAYING",
    "is now playing": "PLAYING",
}


def _normalize(text):
    return " ".join(str(text).split())


def _action_from_text(text):
    lower = text.lower()

    for marker, action in ACTION_MAP.items():
        if marker in lower:
            return action

    return "ACTIVITY"


def _game_link(item):
    return item.find(
        "a",
        href=re.compile(r"^/games/")
    )


def _review_link(item):
    links = item.find_all(
        "a",
        href=re.compile(r"^/u/.+/review/")
    )

    for link in links:
        if "Open review" in link.get_text(" ", strip=True):
            return link

    return links[0] if links else None


def _timestamp_text(text):
    match = re.search(
        r"(\d+\s+(?:min|mins|minute|minutes|hour|hours|hr|hrs|day|days)\s+ago)",
        text,
        flags=re.I,
    )

    return match.group(1) if match else ""


def _review_text(item):
    text = item.get_text(" ", strip=True)
    review_link = _review_link(item)

    if not review_link:
        return ""

    # Backloggd coloca o comentario antes de "0 Likes / Open review".
    match = re.search(
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\s+(.*?)\s+\d+\s+Likes?",
        text,
        flags=re.I,
    )

    if match:
        return _normalize(match.group(1))

    return ""


def parse(html):
    if isinstance(html, str):
        html = BeautifulSoup(html, "html.parser")

    activities = []

    for item in html.find_all("div", class_="activity"):
        text = _normalize(item.get_text(" ", strip=True))
        game = _game_link(item)

        if not game:
            continue

        game_title = _normalize(game.get_text(" ", strip=True))
        game_url = urljoin(BASE_URL, game.get("href", ""))
        review = _review_link(item)
        review_url = urljoin(BASE_URL, review.get("href", "")) if review else ""
        image = item.find("img")
        action = _action_from_text(text)

        activity_id = "|".join(
            part for part in (
                action,
                game.get("href", ""),
                review.get("href", "") if review else "",
                _timestamp_text(text),
                _review_text(item),
            ) if part
        )

        activities.append({
            "id": activity_id,
            "tipo": action,
            "raw_text": text,
            "game": game_title,
            "game_url": game_url,
            "review_url": review_url,
            "image": image.get("src") if image else "",
            "relative_time": _timestamp_text(text),
            "review": _review_text(item),
        })

    return activities

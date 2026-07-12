"""
Interpretar reviews da Steam.
"""

import re
from datetime import datetime

from bs4 import BeautifulSoup


MESES = {
    "January": "janeiro",
    "February": "fevereiro",
    "March": "março",
    "April": "abril",
    "May": "maio",
    "June": "junho",
    "July": "julho",
    "August": "agosto",
    "September": "setembro",
    "October": "outubro",
    "November": "novembro",
    "December": "dezembro",
}


def _text(node, selector):
    found = node.select_one(selector)
    return found.get_text(" ", strip=True) if found else ""


def _parse_posted(text):
    posted = (
        text
        .replace("Posted", "")
        .replace(".", "")
        .strip()
    )

    for ingles, portugues in MESES.items():
        posted = posted.replace(ingles, portugues)

    match = re.match(r"(\d+)\s+(.+)", posted)

    if match:
        return f"{match.group(1)} de {match.group(2)} de {datetime.now().year}"

    return posted


def _parse_review(review):
    link_tag = review.select_one(".title a")
    link = link_tag["href"] if link_tag else ""

    match = re.search(r"RecommendationVoteUpBtn(\d+)", str(review))
    review_id = match.group(1) if match else link

    match = re.search(r"/recommended/(\d+)/", link)
    appid = match.group(1) if match else ""

    cover_tag = review.select_one("img.game_capsule")
    cover = cover_tag["src"] if cover_tag else ""

    classes = review.get("class", [])

    if "thumbs_up" in classes:
        recommended = True
    elif "thumbs_down" in classes:
        recommended = False
    else:
        title = _text(review, ".title").lower()
        recommended = "recommend" in title or "recomend" in title

    hours = _text(review, ".hours")
    match = re.search(r"([\d.]+)", hours)

    if match:
        valor = match.group(1).replace(".", ",")
        hours = f"{valor} horas jogadas"

    return {
        "id": review_id,
        "appid": appid,
        "link": link,
        "cover": cover,
        "recommended": recommended,
        "hours": hours,
        "text": _text(review, ".content"),
        "posted": _parse_posted(_text(review, ".posted")),
    }


def parse_all(html):
    soup = BeautifulSoup(html, "html.parser")
    return [
        _parse_review(review)
        for review in soup.select(".review_box")
    ]


def parse(html):
    reviews = parse_all(html)
    return reviews[0] if reviews else None

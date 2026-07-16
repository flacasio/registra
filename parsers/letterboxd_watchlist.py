"""
Parser de atividades de watchlist do Letterboxd.
"""

from urllib.parse import urljoin


BASE_URL = "https://letterboxd.com"


def _clean(text):
    return " ".join(text.split())


def _text(element):
    return _clean(element.get_text(" ", strip=True))


def _is_watchlist_activity(element):
    text = _text(element).lower()
    return "watchlist" in text and "added" in text


def _poster(element):
    image = element.find("img")

    if not image:
        return None

    for attr in ("data-src", "data-original", "src"):
        value = image.get(attr)

        if value:
            return value

    return None


def _film_title(element, link):
    film = element.find(attrs={"data-film-name": True})

    if film:
        return _clean(film["data-film-name"])

    if link:
        for attr in ("title", "aria-label"):
            value = link.get(attr)

            if value:
                return _clean(value)

        text = _text(link)

        if text:
            return text

    return "Filme"


def _film_link(element):
    for link in element.find_all("a", href=True):
        href = link["href"]

        if "/film/" in href:
            return link

    return None


def _published(element):
    time = element.find("time")

    if not time:
        return ""

    return time.get("datetime") or _text(time)


def _parse_activity(element):
    link = _film_link(element)

    if not link:
        return None

    href = link["href"]
    url = urljoin(BASE_URL, href)
    title = _film_title(element, link)

    return {
        "id": f"letterboxd_watchlist:{url}",
        "tipo": "WATCHLIST",
        "titulo": title,
        "url": url,
        "published": _published(element),
        "poster": _poster(element),
    }


def parse(soup):
    activities = []
    seen = set()
    candidates = soup.select(
        "li, article, tr, div.activity, div.activity-row, div.activity-table-row"
    )

    for element in candidates:
        if not _is_watchlist_activity(element):
            continue

        activity = _parse_activity(element)

        if not activity or activity["id"] in seen:
            continue

        seen.add(activity["id"])
        activities.append(activity)

    return activities

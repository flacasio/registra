"""
Interpretar atividades do Goodreads a partir dos feeds RSS publicos.
"""

from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup


def _text(item, name):
    tag = item.find(name)
    return tag.get_text(" ", strip=True) if tag else ""


def _clean_url(url):
    if not url:
        return ""

    parts = urlsplit(url)
    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path,
            "",
            "",
        )
    )


def _book_url(item):
    description = item.find("description")

    if description:
        description_html = BeautifulSoup(
            description.get_text("", strip=True),
            "html.parser",
        )
        link = description_html.find("a")

        if link and link.get("href"):
            return _clean_url(link["href"])

    return _clean_url(_text(item, "link"))


def _parse_item(item, tipo):

    title = _text(item, "title")
    author = _text(item, "author_name")
    rating = _text(item, "user_rating")
    shelves = _text(item, "user_shelves")
    pub_date = _text(item, "pubDate")
    read_at = _text(item, "user_read_at")
    date_added = _text(item, "user_date_added")
    review = _text(item, "user_review")
    guid = _text(item, "guid") or _text(item, "link")
    book_id = _text(item, "book_id")

    if tipo == "CURRENTLY_READING":
        event_date = pub_date or date_added
    elif tipo == "WANT_TO_READ":
        event_date = date_added or pub_date
    else:
        event_date = pub_date or read_at or date_added

    activity_id = "|".join(
        part for part in (tipo, guid, event_date, rating, shelves) if part
    )

    return {
        "id": activity_id,
        "tipo": tipo,
        "titulo": title,
        "autor": author,
        "capa": (
            _text(item, "book_large_image_url")
            or _text(item, "book_medium_image_url")
            or _text(item, "book_image_url")
        ),
        "url": _book_url(item),
        "review_url": _clean_url(_text(item, "link")),
        "book_id": book_id,
        "rating": int(rating) if rating.isdigit() else 0,
        "shelves": shelves,
        "review": review,
        "event_date": event_date,
        "read_at": read_at,
        "date_added": date_added,
    }


def parse_rss_items(soup, tipo):
    return [
        _parse_item(item, tipo)
        for item in soup.find_all("item")
    ]


def parse_rss(soup, tipo):
    items = parse_rss_items(soup, tipo)
    return items[0] if items else None

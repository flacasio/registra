"""
Interpretar listas de pessoas do AOTY.
"""

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE_URL = "https://www.albumoftheyear.org"


def _clean(text):
    return " ".join(str(text or "").split())


def _image_url(img):
    if not img:
        return ""

    return urljoin(
        BASE_URL,
        img.get("data-src") or img.get("src") or "",
    )


def parse_followers(html):
    soup = BeautifulSoup(html, "html.parser")
    people = []
    seen = set()

    for link in soup.find_all("a", href=re.compile(r"^/user/[^/]+/?$")):
        href = link.get("href", "")
        url = urljoin(BASE_URL, href)
        username = href.strip("/").split("/")[-1]
        container = link.find_parent(["div", "li", "tr"])
        name = _clean(link.get_text(" ", strip=True)) or username
        image = ""

        if container:
            img = container.find("img")
            image = _image_url(img)

            if not name or name == username:
                candidate = (
                    container.select_one(".userName")
                    or container.select_one(".username")
                    or container.select_one(".name")
                )
                name = _clean(candidate.get_text(" ", strip=True) if candidate else name)

        item_id = f"aoty_follower_{username}"

        if not username or item_id in seen:
            continue

        seen.add(item_id)
        people.append({
            "id": item_id,
            "username": username,
            "name": name or username,
            "image": image,
            "url": url,
        })

    return people

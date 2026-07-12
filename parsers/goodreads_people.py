"""
Interpretar listas de pessoas do Goodreads.
"""

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE_URL = "https://www.goodreads.com"


def _clean(text):
    return " ".join(str(text or "").split())


def _person_from_link(link, kind):
    href = link.get("href", "")

    if "/user/show/" not in href and "/user/" not in href:
        return None

    url = urljoin(BASE_URL, href)
    name = _clean(link.get_text(" ", strip=True))

    image = ""
    container = link.find_parent(["div", "li", "tr"])

    if container:
        img = container.select_one("img")
        image = img.get("src", "") if img else ""

        if not name:
            name_node = (
                container.select_one(".userName")
                or container.select_one(".friendName")
                or container.select_one("a[href*='/user/']")
            )
            name = _clean(name_node.get_text(" ", strip=True) if name_node else "")

    if not name:
        return None

    match = re.search(r"/user/show/([^/?#]+)", url)
    person_id = match.group(1) if match else url

    return {
        "id": f"{kind}_{person_id}",
        "kind": kind,
        "name": name,
        "image": image,
        "url": url,
    }


def parse(html, kind):
    soup = BeautifulSoup(html, "html.parser")
    people = []
    seen = set()

    for link in soup.select("a[href*='/user/show/'], a[href^='/user/']"):
        person = _person_from_link(link, kind)

        if not person or person["id"] in seen:
            continue

        seen.add(person["id"])
        people.append(person)

    return people

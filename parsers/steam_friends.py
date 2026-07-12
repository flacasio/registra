"""
Interpretar amigos da Steam.
"""

from bs4 import BeautifulSoup


def _clean(text):
    return " ".join(str(text or "").split())


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    activities = []

    for friend in soup.select(".friend_block_v2, .selectable, [data-steamid]"):
        steamid = friend.get("data-steamid", "")
        link = friend.select_one("a[href*='steamcommunity.com']")
        image = friend.select_one("img")
        name_node = (
            friend.select_one(".friend_block_content")
            or friend.select_one(".friend_block_content_inner")
            or link
        )
        name = _clean(name_node.get_text(" ", strip=True) if name_node else "")

        if not name:
            continue

        url = link.get("href", "") if link else ""
        avatar = image.get("src", "") if image else ""
        item_id = steamid or url or name

        activities.append({
            "id": f"friend_{item_id}",
            "name": name,
            "avatar": avatar,
            "url": url,
        })

    return activities

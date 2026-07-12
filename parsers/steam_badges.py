"""
Interpretar insignias da Steam.
"""

from bs4 import BeautifulSoup


def _clean(text):
    return " ".join(str(text or "").split())


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    activities = []

    for badge in soup.select(".badge_row, .badge_card_set_card, [class*='badge_row']"):
        link = badge.select_one("a[href*='/badges/']")
        image = badge.select_one("img")
        title_node = (
            badge.select_one(".badge_title")
            or badge.select_one(".badge_info_title")
            or link
        )
        title = _clean(title_node.get_text(" ", strip=True) if title_node else "")

        if not title:
            continue

        url = link.get("href", "") if link else ""
        image_url = image.get("src", "") if image else ""
        item_id = url or image_url or title

        activities.append({
            "id": f"badge_{item_id}",
            "title": title,
            "image": image_url,
            "url": url,
        })

    return activities

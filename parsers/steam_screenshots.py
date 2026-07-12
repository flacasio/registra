"""
Interpretar capturas de tela da Steam.
"""

from bs4 import BeautifulSoup


def _clean(text):
    return " ".join(str(text or "").split())


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    activities = []

    for shot in soup.select(".profile_media_item, .imageWallRow a, a[href*='sharedfiles/filedetails']"):
        link = shot if shot.name == "a" else shot.select_one("a[href*='sharedfiles/filedetails']")
        image = shot.select_one("img") if shot.name != "img" else shot

        if image is None and link is not None:
            image = link.select_one("img")

        url = link.get("href", "") if link else ""
        image_url = image.get("src", "") if image else ""
        title = _clean(image.get("alt", "") if image else "")

        if not url and not image_url:
            continue

        activities.append({
            "id": f"screenshot_{url or image_url}",
            "title": title or "Nova captura de tela",
            "image": image_url,
            "url": url,
        })

    return activities

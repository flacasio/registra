"""
Interpretar wishlist da Steam.
"""

import json
import re

from bs4 import BeautifulSoup


def _clean(text):
    return " ".join(str(text or "").split())


def _price(value):
    if value in (None, "", 0):
        return ""

    if isinstance(value, int):
        return f"R$ {value / 100:.2f}"

    return str(value)


def _from_json(html):
    match = re.search(r"g_rgWishlistData\s*=\s*(\[[\s\S]*?\]);", html)

    if not match:
        return []

    try:
        items = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []

    activities = []

    for item in items:
        appid = str(item.get("appid") or "")
        title = _clean(item.get("name"))

        if not appid or not title:
            continue

        subs = item.get("subs") or []
        sub = subs[0] if subs else {}

        activities.append({
            "id": f"wishlist_{appid}",
            "tipo": "WISHLIST",
            "appid": appid,
            "title": title,
            "cover": item.get("capsule") or "",
            "discount": sub.get("discount_pct") or "",
            "price": _price(sub.get("price")),
            "original_price": _price(sub.get("original_price")),
            "added": item.get("date_added") or "",
            "url": f"https://store.steampowered.com/app/{appid}/",
        })

    return activities


def _from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    activities = []

    for row in soup.select(".wishlist_row, [data-app-id], [data-appid]"):
        appid = row.get("data-app-id") or row.get("data-appid") or ""
        link = row.select_one("a[href*='/app/']")

        if not appid and link:
            match = re.search(r"/app/(\d+)", link.get("href", ""))
            appid = match.group(1) if match else ""

        title = _clean(link.get_text(" ", strip=True) if link else "")

        if not appid or not title:
            continue

        image = row.select_one("img")
        discount = row.select_one(".discount_pct")
        price = row.select_one(".discount_final_price")
        original = row.select_one(".discount_original_price")

        activities.append({
            "id": f"wishlist_{appid}",
            "tipo": "WISHLIST",
            "appid": appid,
            "title": title,
            "cover": image.get("src", "") if image else "",
            "discount": _clean(discount.get_text(" ", strip=True) if discount else ""),
            "price": _clean(price.get_text(" ", strip=True) if price else ""),
            "original_price": _clean(original.get_text(" ", strip=True) if original else ""),
            "added": "",
            "url": link.get("href", "") if link else f"https://store.steampowered.com/app/{appid}/",
        })

    return activities


def parse_all(html):
    return _from_json(html) or _from_html(html)


def parse_json(data):
    activities = []

    if isinstance(data, dict):
        items = data.items()
    else:
        items = []

    for appid, item in items:
        title = _clean(item.get("name"))

        if not appid or not title:
            continue

        subs = item.get("subs") or []
        sub = subs[0] if subs else {}
        capsule = item.get("capsule") or item.get("capsule_header") or ""

        activities.append({
            "id": f"wishlist_{appid}",
            "tipo": "WISHLIST",
            "appid": str(appid),
            "title": title,
            "cover": capsule,
            "discount": sub.get("discount_pct") or "",
            "price": _price(sub.get("price")),
            "original_price": _price(sub.get("original_price")),
            "added": item.get("date_added") or "",
            "url": f"https://store.steampowered.com/app/{appid}/",
        })

    return activities


def parse(html):
    items = parse_all(html)

    if not items:
        raise RuntimeError("Nenhum jogo encontrado na wishlist.")

    return items[0]

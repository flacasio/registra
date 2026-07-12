"""
Downloads do Serializd.
"""

import requests

from config import SERIALIZD_USER


API_BASE_URL = "https://serializd.onrender.com"
SITE_BASE_URL = "https://www.serializd.com"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w780"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": SITE_BASE_URL,
    "Referer": f"{SITE_BASE_URL}/user/{SERIALIZD_USER}/activity",
    "X-Requested-With": "serializd_vercel",
}


def activity(cursor=None):
    params = {}

    if cursor:
        params["cursor"] = cursor

    response = requests.get(
        f"{API_BASE_URL}/api/user/{SERIALIZD_USER}/activity_v3",
        params=params,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def image_url(path):
    if not path:
        return ""

    if path.startswith("http://") or path.startswith("https://"):
        return path

    if not path.startswith("/"):
        path = f"/{path}"

    return f"{IMAGE_BASE_URL}{path}"


def review_url(review_id):
    if not review_id:
        return ""

    return f"{SITE_BASE_URL}/review/{review_id}"


def show_url(show_id):
    if not show_id:
        return ""

    return f"{SITE_BASE_URL}/show/{show_id}"

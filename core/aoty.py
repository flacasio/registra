"""
Downloads do Album of the Year.
"""

from urllib.parse import urljoin
import time

import requests

from config import AOTY_INCOMING_LIST_PATH, AOTY_REQUEST_DELAY_SECONDS, AOTY_USER


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.albumoftheyear.org/",
}


class AotyRateLimitedError(RuntimeError):
    pass


def _get(url):
    time.sleep(max(0, AOTY_REQUEST_DELAY_SECONDS))

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    if response.status_code == 429:
        raise AotyRateLimitedError("AOTY limitou as requisicoes.")

    response.raise_for_status()

    return response.text


def profile():
    return _get(
        f"https://www.albumoftheyear.org/user/{AOTY_USER}/",
    )


def followers():
    return _get(
        f"https://www.albumoftheyear.org/user/{AOTY_USER}/followers/",
    )


def ratings_page(page=1):
    suffix = "ratings/" if int(page) <= 1 else f"ratings/{page}/"

    return _get(
        f"https://www.albumoftheyear.org/user/{AOTY_USER}/{suffix}",
    )


def incoming_list():
    url = urljoin(
        f"https://www.albumoftheyear.org/user/{AOTY_USER}/",
        AOTY_INCOMING_LIST_PATH,
    )

    return _get(
        url,
    )

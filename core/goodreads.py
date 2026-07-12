"""
Downloads do Goodreads.
"""

from config import GOODREADS_USER_ID
from core.downloader import download_text


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def following_page():
    return download_text(
        f"https://www.goodreads.com/user/{GOODREADS_USER_ID}/following",
        headers=HEADERS,
    )

"""
Downloads do Futez.
"""

from config import FUTEZ_PROFILE_URL, FUTEZ_USER_ID
from core.downloader import download_html


def _profile_url():
    if FUTEZ_PROFILE_URL:
        return FUTEZ_PROFILE_URL

    if not FUTEZ_USER_ID:
        return ""

    return f"https://futez.com.br/{FUTEZ_USER_ID}"


def profile_page():
    url = _profile_url()

    if not url:
        return None

    return download_html(url)

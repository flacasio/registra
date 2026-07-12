"""
============================================================
Rezistro
Arquivo: core/downloader.py
Versão: 1.2
============================================================

Responsabilidade:
Centralizar todos os downloads realizados pelo Rezistro.
"""

from pathlib import Path
import time

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}


def _request(method, url, headers=None, retries=DEFAULT_RETRIES, **kwargs):
    if headers is None:
        headers = DEFAULT_HEADERS

    last_error = None

    for attempt in range(1, retries + 1):
        try:
            resposta = requests.request(
                method,
                url,
                headers=headers,
                timeout=DEFAULT_TIMEOUT,
                **kwargs,
            )

            if (
                resposta.status_code in RETRY_STATUS_CODES
                and attempt < retries
            ):
                time.sleep(attempt * 5)
                continue

            resposta.raise_for_status()
            return resposta

        except requests.RequestException as exc:
            last_error = exc

            if attempt >= retries:
                raise

            time.sleep(attempt * 5)

    raise last_error


# ==========================================================
# HTML
# ==========================================================

def download_html(url, headers=None):
    resposta = _request(
        "GET",
        url,
        headers=headers,
    )

    return BeautifulSoup(
        resposta.text,
        "html.parser"
    )


# ==========================================================
# TEXTO
# ==========================================================

def download_text(url, headers=None):
    resposta = _request(
        "GET",
        url,
        headers=headers,
    )

    return resposta.text


# ==========================================================
# JSON
# ==========================================================

def download_json(url, headers=None):
    resposta = _request(
        "GET",
        url,
        headers=headers,
    )

    return resposta.json()


# ==========================================================
# BYTES
# ==========================================================

def download_bytes(url, headers=None):
    text_url = str(url)

    if not text_url.startswith(("http://", "https://")):
        caminho = Path(text_url)

        if caminho.exists():
            return caminho.read_bytes()

    resposta = _request(
        "GET",
        url,
        headers=headers,
    )

    return resposta.content


# ==========================================================
# IMAGEM
# ==========================================================

def download_image(url, headers=None):

    return download_bytes(
        url,
        headers=headers
    )


# ==========================================================
# STATUS
# ==========================================================

def url_exists(url, headers=None):

    if headers is None:
        headers = DEFAULT_HEADERS

    try:

        resposta = _request(
            "HEAD",
            url,
            headers=headers,
            allow_redirects=True,
        )
        return resposta.ok

    except requests.RequestException:

        return False


# ==========================================================
# TESTE
# ==========================================================

if __name__ == "__main__":

    print("Downloader carregado com sucesso.")

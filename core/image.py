"""
============================================================
Rezistro
Arquivo: core/image.py
Versão: 2.0
============================================================

Responsabilidade:
Resolver a melhor imagem disponível
para cada serviço.
"""

import requests

from core.downloader import download_html


# ==========================================================
# GOODREADS
# ==========================================================

def goodreads_cover(book_url):

    soup = download_html(book_url)

    imagem = soup.select_one("img.ResponsiveImage")

    if imagem:

        src = imagem.get("src")

        if src:

            return src

    imagem = soup.select_one("#coverImage")

    if imagem:

        src = imagem.get("src")

        if src:

            return src

    return None


# ==========================================================
# STEAM
# ==========================================================

def steam_cover(appid):

    base = (
        "https://cdn.cloudflare.steamstatic.com/"
        f"steam/apps/{appid}"
    )

    candidatos = [

        f"{base}/library_600x900_2x.jpg",

        f"{base}/library_600x900.jpg",

        f"{base}/header.jpg"

    ]

    for url in candidatos:

        try:

            resposta = requests.head(
                url,
                timeout=10,
                allow_redirects=True
            )

            if resposta.status_code == 200:

                return url

        except Exception:

            pass

    return None


# ==========================================================
# LETTERBOXD
# ==========================================================

def letterboxd_cover(url):

    return url
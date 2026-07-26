"""
Configuracao central do Rezistro.

O codigo le as mesmas variaveis em dois lugares:

1. No seu computador, pelo arquivo local .env.
2. No GitHub Actions, pelos Repository Secrets.

Valores reais nao devem ficar escritos neste arquivo.
"""

import os
from pathlib import Path


def _carregar_env_local():
    caminho = Path(".env")

    if not caminho.exists():
        return

    for linha_original in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha_original.strip()

        if not linha or linha.startswith("#") or "=" not in linha:
            continue

        nome, valor = linha.split("=", 1)
        nome = nome.strip()
        valor = valor.strip().strip('"').strip("'")

        if nome:
            os.environ.setdefault(nome, valor)


def _valor(nome, padrao=""):
    return os.getenv(nome, padrao).strip()


_carregar_env_local()


# Telegram
TELEGRAM_TOKEN = _valor("TELEGRAM_TOKEN")
CHAT_ID = _valor("CHAT_ID")

# Nome exibido nos cards
DISPLAY_NAME = _valor("DISPLAY_NAME")
REAL_NAME = _valor("REAL_NAME")
DISPLAY_EMOJI = _valor("DISPLAY_EMOJI")

# Banco de Series
BDS_UID = _valor("BDS_UID")

# Goodreads
GOODREADS_USER_ID = _valor("GOODREADS_USER_ID")

# Steam
STEAM_USER = _valor("STEAM_USER")
STEAM_API_KEY = _valor("STEAM_API_KEY")
STEAM_ACHIEVEMENTS_APPIDS = _valor("STEAM_ACHIEVEMENTS_APPIDS")

# Letterboxd
LETTERBOXD_USER = _valor("LETTERBOXD_USER")

# Backloggd
BACKLOGGD_USER = _valor("BACKLOGGD_USER")

# Last.fm
LASTFM_USER = _valor("LASTFM_USER")
LASTFM_API_KEY = _valor("LASTFM_API_KEY")

# Album of the Year
AOTY_USER = _valor("AOTY_USER")
AOTY_COMPARE_MAX_PAGES = int(_valor("AOTY_COMPARE_MAX_PAGES", "80") or 80)
AOTY_COMPARE_PAGES_PER_RUN = int(_valor("AOTY_COMPARE_PAGES_PER_RUN", "2") or 2)
AOTY_REQUEST_DELAY_SECONDS = float(
    _valor("AOTY_REQUEST_DELAY_SECONDS", "4") or 4
)
AOTY_INCOMING_LIST_PATH = _valor("AOTY_INCOMING_LIST_PATH")

# Serializd
SERIALIZD_USER = _valor("SERIALIZD_USER")

# Futez
FUTEZ_USER_ID = _valor("FUTEZ_USER_ID")
FUTEZ_PROFILE_URL = _valor("FUTEZ_PROFILE_URL")
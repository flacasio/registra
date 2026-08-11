"""
Envio de cards para o Telegram.
"""

from io import BytesIO

import requests

from config import CHAT_ID, TELEGRAM_TOKEN
from core.card import Card
from core.downloader import download_bytes


def _api_url():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN nao configurado.")

    return f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def _validar_config():
    if not CHAT_ID:
        raise RuntimeError("CHAT_ID nao configurado.")


def _send_text(card: Card):
    resposta = requests.post(
        f"{_api_url()}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": card.to_caption(),
            "parse_mode": "HTML",
        },
        timeout=30,
    )

    resposta.raise_for_status()
    return resposta.json()


def send(card: Card):
    if not isinstance(card, Card):
        raise TypeError("send() aceita apenas objetos Card.")

    _validar_config()

    if not card.image:
        return _send_text(card)

    try:
        imagem = BytesIO(download_bytes(card.image))
    except requests.RequestException:
        return _send_text(card)

    imagem.name = "card.jpg"

    resposta = requests.post(
        f"{_api_url()}/sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "caption": card.to_caption(),
            "parse_mode": "HTML",
        },
        files={
            "photo": (
                "card.jpg",
                imagem,
                "image/jpeg",
            )
        },
        timeout=30,
    )

    resposta.raise_for_status()

    return resposta.json()


if __name__ == "__main__":
    card = Card()
    card.set_title("Teste")
    card.set_image("https://placehold.co/600x900")
    card.add_lines("Linha 1", "Linha 2")

    send(card)

    print("Teste enviado.")

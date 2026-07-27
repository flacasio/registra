import re

from core.card import Card
from core.card_style import set_network_title


RELATIVE_TIME = {
    "mins ago": "minutos atrás",
    "min ago": "minuto atrás",
    "minutes ago": "minutos atrás",
    "minute ago": "minuto atrás",
    "hrs ago": "horas atrás",
    "hr ago": "hora atrás",
    "hours ago": "horas atrás",
    "hour ago": "hora atrás",
    "days ago": "dias atrás",
    "day ago": "dia atrás",
}


def _relative_time(text):
    translated = text
    translated = re.sub(r"\b1h ago\b", "1 hora atrás", translated)
    translated = re.sub(r"\b(\d+)h ago\b", r"\1 horas atrás", translated)

    for original, replacement in RELATIVE_TIME.items():
        translated = translated.replace(original, replacement)

    return translated


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("image"):
        card.set_image(activity["image"])

    set_network_title(card, "📀", "AOTY", "avaliou")

    card.add_lines(
        f"💿 <b>{activity['album']}</b>",
        f"👤 {activity['artist']}",
        f"⭐ <b>Nota: {activity['rating']}/100</b>",
    )

    if activity.get("relative_time"):
        card.add_lines(
            "",
            f"🕒 {_relative_time(activity['relative_time'])}",
        )

    if activity.get("url"):
        card.add_lines(
            f'🔗 <a href="{activity["url"]}">Página</a>'
        )

    return card

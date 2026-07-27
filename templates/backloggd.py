from core.backloggd import game_cover
from core.card import Card
from core.card_style import set_network_title


ACTION_TEXT = {
    "ABANDONED": "abandonou",
    "COMPLETED": "concluiu",
    "PLAYING": "começou",
    "ACTIVITY": "atualizou",
}

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

    for original, replacement in RELATIVE_TIME.items():
        translated = translated.replace(original, replacement)

    return translated


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    image = activity.get("image") or game_cover(activity["game_url"])

    if image:
        card.set_image(image)

    action = ACTION_TEXT.get(activity["tipo"], "atualizou")

    set_network_title(card, "👾", "Backloggd", action)

    card.add_line(
        f"🎮 <b>{activity['game']}</b>"
    )

    if activity.get("review"):
        card.add_lines(
            "",
            f"“{activity['review']}”",
        )

    if activity.get("relative_time"):
        card.add_lines(
            "",
            f"🕒 {_relative_time(activity['relative_time'])}",
        )

    if activity.get("review_url"):
        card.add_lines(
            f'🔗 <a href="{activity["review_url"]}">Review</a>'
        )
    elif activity.get("game_url"):
        card.add_lines(
            f'🔗 <a href="{activity["game_url"]}">Página</a>'
        )

    return card

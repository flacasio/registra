from core.card import Card
from core.card_style import set_network_title
from core.text import clean_media_title


def _direction(old_rating, new_rating):
    try:
        old_value = float(str(old_rating).replace(",", "."))
        new_value = float(str(new_rating).replace(",", "."))
    except ValueError:
        return "🔁"

    if new_value > old_value:
        return "↗️"

    if new_value < old_value:
        return "↘️"

    return "🔁"


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("image"):
        card.set_image(activity["image"])

    emoji = _direction(
        activity["old_rating"],
        activity["new_rating"],
    )

    set_network_title(card, "📀", "AOTY", "reavaliou")

    card.add_lines(
        f"💿 <b>{clean_media_title(activity['album'])}</b>",
        f"👤 {activity['artist']}",
        f"{emoji} <b>{activity['old_rating']} → {activity['new_rating']}</b>",
    )

    if activity.get("url"):
        card.add_lines(
            "",
            f'🔗 <a href="{activity["url"]}">Página</a>',
        )

    return card

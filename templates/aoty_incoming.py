from core.card import Card
from core.card_style import set_network_title
from core.text import clean_media_title


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("image"):
        card.set_image(activity["image"])

    set_network_title(card, "📀", "AOTY", "está de olho")

    card.add_line(
        f"💿 <b>{clean_media_title(activity['album'])}</b>"
    )

    if activity.get("artist"):
        card.add_line(
            f"👤 {activity['artist']}"
        )

    if activity.get("release_date"):
        card.add_line(
            f"📅 {activity['release_date']}"
        )

    if activity.get("url"):
        card.add_lines(
            "",
            f'🔗 <a href="{activity["url"]}">Página</a>',
        )

    return card

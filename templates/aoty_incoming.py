from core.card import Card
from core.card_style import set_network_title


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("image"):
        card.set_image(activity["image"])

    set_network_title(card, "📀", "AOTY", "está de olho")

    card.add_line(
        f"💿 <b>{activity['album']}</b>"
    )

    if activity.get("artist"):
        card.add_line(
            f"👤 {activity['artist']}"
        )

    for line in activity.get("extra_lines", []):
        card.add_line(
            f"📝 {line}"
        )

    if activity.get("url"):
        card.add_lines(
            "",
            f'🔗 <a href="{activity["url"]}">Página</a>',
        )

    return card

from core.card import Card
from core.card_style import set_network_title


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("image"):
        card.set_image(activity["image"])

    set_network_title(card, "🎖", "Steam", "foi premiada")

    card.add_line(
        f"🏅 <b>{activity['title']}</b>"
    )

    return card

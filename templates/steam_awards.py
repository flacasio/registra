from core.card import Card
from core.card_style import set_network_title


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("image"):
        card.set_image(activity["image"])

    set_network_title(card, "🕹️", "Steam", "recebeu um prêmio")

    card.add_line(
        f"🎖️ <b>{activity['title']}</b>"
    )

    if activity.get("text") and activity["text"] != activity["title"]:
        card.add_line(
            activity["text"]
        )

    return card

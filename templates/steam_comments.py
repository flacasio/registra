from core.card import Card
from core.card_style import add_posted_at, set_network_title


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("avatar"):
        card.set_image(activity["avatar"])

    set_network_title(card, "🕹️", "Steam", "recebeu um comentário")

    card.add_lines(
        f"👤 <b>{activity['author']}</b>",
        "",
        f"💭 {activity['text']}",
    )

    add_posted_at(card, activity.get("timestamp"))

    return card

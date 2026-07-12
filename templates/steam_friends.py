from core.card import Card
from core.card_style import set_network_title


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("avatar"):
        card.set_image(activity["avatar"])

    set_network_title(card, "🕹️", "Steam", "fez uma nova amizade")

    card.add_line(
        f"👤 <b>{activity['name']}</b>"
    )

    if activity.get("url"):
        card.add_lines(
            "",
            f'🔗 <a href="{activity["url"]}">Perfil</a>',
        )

    return card

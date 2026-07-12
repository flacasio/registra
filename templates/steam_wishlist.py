from core.card import Card
from core.card_style import add_posted_at, set_network_title
from core.image import steam_cover


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    image = activity.get("cover") or steam_cover(activity["appid"])

    if image:
        card.set_image(image)

    set_network_title(card, "🕹️", "Steam", "colocou um jogo no radar")

    card.add_line(
        f"🎮 <b>{activity['title']}</b>"
    )

    if activity.get("discount"):
        card.add_line(
            f"🏷️ <b>{activity['discount']}</b>"
        )

    if activity.get("price"):
        card.add_line(
            f"💰 <b>{activity['price']}</b>"
        )

    add_posted_at(card, activity.get("added"))

    if activity.get("url"):
        card.add_lines(
            "",
            f'🔗 <a href="{activity["url"]}">Ver na Steam</a>',
        )

    return card

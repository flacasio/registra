from core.card import Card
from core.card_style import set_network_title
from core.image import steam_cover


def make_card(activity):
    card = Card()

    capa = steam_cover(activity["appid"]) or activity["cover"]

    if capa:
        card.set_image(capa)

    card.set_id(activity["id"])

    if activity["recommended"]:
        set_network_title(card, "🕹️", "Steam", "aprovou um jogo")
    else:
        set_network_title(card, "🕹️", "Steam", "reprovou um jogo")

    card.add_lines(
        f"🎮 <b>{activity['game']}</b>",
        f"⌛ {activity['hours']}",
        f"✍️ {activity['text']}",
        f"🕒 {activity['posted']}",
    )

    if activity.get("link"):
        card.add_line(
            f'🔗 <a href="{activity["link"]}">Review</a>'
        )

    return card

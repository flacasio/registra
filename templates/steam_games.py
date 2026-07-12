from core.card import Card
from core.card_style import set_network_title
from core.image import steam_cover


ACTION_BY_TYPE = {
    "STEAM_NEW": "adicionou um novo jogo",
    "STEAM_PERFECT": "platinou um jogo",
}


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    image = steam_cover(activity["appid"])

    if image:
        card.set_image(image)

    set_network_title(
        card,
        "🕹️",
        "Steam",
        ACTION_BY_TYPE.get(activity["tipo"], "teve uma nova atividade"),
    )

    card.add_line(
        f"🎮 <b>{activity['title']}</b>"
    )

    if activity.get("hours"):
        card.add_line(
            f"⏱️ {activity['hours']}"
        )

    if activity.get("url"):
        card.add_lines(
            "",
            f'🔗 <a href="{activity["url"]}">Ver na Steam</a>',
        )

    return card

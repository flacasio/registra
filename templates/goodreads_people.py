from core.card import Card
from core.card_style import set_network_title


ACTION_BY_KIND = {
    "following": "seguiu um novo usuário",
}


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("image"):
        card.set_image(activity["image"])

    set_network_title(
        card,
        "📚",
        "Goodreads",
        ACTION_BY_KIND.get(activity.get("kind"), "teve uma nova atividade"),
    )

    card.add_line(
        f"👤 <b>{activity['name']}</b>"
    )

    if activity.get("url"):
        card.add_lines(
            "",
            f'🔗 <a href="{activity["url"]}">Perfil</a>',
        )

    return card

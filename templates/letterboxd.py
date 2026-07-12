from core.card import Card
from core.card_style import add_posted_at, set_network_title


def make_card(activity):
    card = Card()
    card.set_image(activity["poster"])
    card.set_id(activity["id"])

    if activity["tipo"] == "WATCH":
        set_network_title(card, "🎬", "Letterboxd", "assistiu a um filme")
    else:
        set_network_title(card, "🎬", "Letterboxd", "teve uma nova atividade")

    card.add_line(
        f"🎞️ <b>{activity['titulo']}</b>"
    )

    add_posted_at(card, activity.get("published"))

    card.add_lines(
        "",
        f'🔗 <a href="{activity["url"]}">Página</a>',
    )

    return card

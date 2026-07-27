from core.card import Card
from core.card_style import add_posted_at, set_network_title


def _action(activity):
    if activity["tipo"] == "WATCH":
        return "assistiu"

    if activity["tipo"] == "WATCHLIST":
        return "quer ver"

    return "teve uma nova atividade"


def make_card(activity):
    card = Card()

    if activity.get("poster"):
        card.set_image(activity["poster"])

    card.set_id(activity["id"])
    set_network_title(card, "🎬", "Letterboxd", _action(activity))

    card.add_line(
        f"🎞️ <b>{activity['titulo']}</b>"
    )

    if activity.get("rating"):
        card.add_line(
            f"⭐️ {activity['rating']}"
        )

    add_posted_at(card, activity.get("published"))

    card.add_lines(
        "",
        f'🔗 <a href="{activity["url"]}">Página</a>',
    )

    return card

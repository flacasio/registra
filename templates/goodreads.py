from core.card import Card
from core.card_style import add_posted_at, set_network_title


def _stars(rating):
    if not rating:
        return ""

    return "★" * rating + "☆" * (5 - rating)


def _action(activity):
    tipo = activity["tipo"]

    if tipo == "CURRENTLY_READING":
        return "está lendo um livro"

    if tipo == "WANT_TO_READ":
        return "quer ler um livro"

    if activity.get("rating"):
        return "avaliou um livro"

    return "marcou um livro como lido"


def make_card(activity):
    card = Card()

    capa = activity.get("capa")

    if capa:
        card.set_image(capa)
    card.set_id(activity["id"])
    set_network_title(card, "📚", "Goodreads", _action(activity))

    card.add_lines(
        f"📖 <b>{activity['titulo']}</b>",
        f"👤 <b>{activity['autor']}</b>",
    )

    if activity.get("rating"):
        card.add_line(
            f"⭐ <b>{_stars(activity['rating'])}</b>"
        )

    if activity.get("review"):
        card.add_lines(
            "",
            f"✍️ {activity['review']}",
        )

    add_posted_at(card, activity.get("event_date"))

    card.add_lines(
        "",
        f'🔗 <a href="{activity["url"]}">Página</a>',
    )

    return card

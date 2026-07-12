from core.card import Card
from core.card_style import add_posted_at, set_network_title


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity["capa"]:
        card.set_image(activity["capa"])

    set_network_title(card, "💘", "Last.fm", "favoritou uma música")

    card.add_lines(
        f"🎵 <b>{activity['titulo']}</b>",
        f"🎤 {activity['artista']}",
    )

    if activity["album"]:
        card.add_line(
            f"💿 <i>{activity['album']}</i>"
        )

    add_posted_at(card, activity["timestamp"])

    return card

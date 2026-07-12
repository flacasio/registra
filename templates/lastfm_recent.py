from core.card import Card
from core.card_style import add_posted_at, set_network_title


def _format_date(timestamp):
    if not timestamp:
        return "Tocando agora"

    return timestamp


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity["capa"]:
        card.set_image(activity["capa"])

    set_network_title(card, "🎧", "Last.fm", "escutou uma música")

    card.add_lines(
        f"🎵 <b>{activity['titulo']}</b>",
        f"🎤 {activity['artista']}",
    )

    if activity["album"]:
        card.add_line(
            f"💿 <i>{activity['album']}</i>"
        )

    if activity["timestamp"]:
        add_posted_at(card, _format_date(activity["timestamp"]))
    else:
        card.add_lines(
            "",
            "🕒 Tocando agora",
        )

    return card

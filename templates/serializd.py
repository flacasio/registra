from core.card import Card
from core.card_style import add_posted_at, set_network_title


ACTION_BY_KIND = {
    "LOGGED": "registrou um episódio",
    "RATED": "avaliou uma série",
    "REVIEWED": "comentou uma série",
    "WATCHLIST": "adicionou uma série à lista",
    "CURRENTLY_WATCHING": "está assistindo uma série",
    "PAUSED": "pausou uma série",
    "DROPPED": "abandonou uma série",
    "ACTIVITY": "atualizou o perfil",
}


def _rating(value):
    if value is None or value == "":
        return ""

    return f"⭐ <b>Nota: {value}/10</b>"


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])

    if activity.get("image"):
        card.set_image(activity["image"])

    action = ACTION_BY_KIND.get(
        activity.get("kind"),
        ACTION_BY_KIND["ACTIVITY"],
    )

    set_network_title(card, "📼", "Serializd", action)

    card.add_line(
        f"🎞️ <b>{activity['show']}</b>"
    )

    if activity.get("season"):
        card.add_line(
            f"🎥 {activity['season']}"
        )

    if activity.get("episode"):
        card.add_line(
            f"📼 {activity['episode']}"
        )

    card.add_line(
        _rating(activity.get("rating"))
    )

    if activity.get("review"):
        card.add_lines(
            "",
            f"“{activity['review']}”",
        )

    add_posted_at(card, activity.get("backdate") or activity.get("date_added"))

    if activity.get("url"):
        card.add_line(
            f'🔗 <a href="{activity["url"]}">Página</a>'
        )

    return card

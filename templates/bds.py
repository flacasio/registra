from core.card import Card
from core.card_style import add_posted_at, set_network_title


def make_card(activity):
    card = Card()
    card.set_image(activity["poster"])
    card.set_id(activity["id"])

    if activity["tipo"] == "RATE":
        set_network_title(card, "🍿", "Banco de Séries", "avaliou um episódio")

        card.add_lines(
            f"⭐ <b>{activity['serie']}</b>",
            f"🎞️ {activity['episodio']}",
            f"➡️ <b>Nota: {activity['nota']}/10</b>",
        )

        add_posted_at(card, activity.get("posted_at"))
        return card

    set_network_title(card, "🍿", "Banco de Séries", "marcou um episódio")

    card.add_lines(
        f"🎞️ <b>{activity['serie']}</b>",
        f"📺 {activity['episodio']}",
        "✅ <b>Assistido</b>",
    )

    add_posted_at(card, activity.get("posted_at"))
    return card

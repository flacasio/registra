from core.achievement_image import achievement_card_image
from core.card import Card
from core.card_style import add_posted_at, set_network_title


def make_card(activity):
    card = Card()
    card.set_id(activity["id"])
    card.set_image(achievement_card_image(activity))

    set_network_title(card, "🕹️", "Steam", "conquistou novos troféus")

    card.add_lines(
        f"🎮 <b>{activity['game']}</b>",
        f"🏆 <b>{activity['name']}</b>",
    )

    if activity.get("description"):
        card.add_line(
            f"💬 {activity['description']}"
        )

    add_posted_at(card, activity.get("unlocktime"))

    if activity.get("url"):
        card.add_line(
            f'🔗 <a href="{activity["url"]}">Conquistas</a>'
        )

    return card

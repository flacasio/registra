from core.card import Card
from core.card_style import set_network_title
from core.image import steam_cover


def _format_minutes(minutes):
    horas = minutes // 60
    minutos = minutes % 60

    if horas:
        return f"{horas}h {minutos}min"

    return f"{minutos}min"


def make_card(activity):
    card = Card()
    card.set_image(steam_cover(activity["appid"]))
    card.set_id(activity["id"])

    if activity["tipo"] == "RECENT_PLAY":
        tempo_total = _format_minutes(activity["tempo_total"])
        tempo_recente = _format_minutes(activity["tempo_recente"])

        set_network_title(card, "🕹️", "Steam", "jogou")

        card.add_lines(
            f"🎮 <b>{activity['titulo']}</b>",
            f"⌚ <b>{tempo_recente}</b> recente",
            f"⏱️ <b>{tempo_total}</b> total",
            "",
            f'🔗 <a href="{activity["url"]}">Ver na Steam</a>',
        )

        return card

    set_network_title(card, "🕹️", "Steam", "teve uma nova atividade")

    card.add_lines(
        f"🎮 <b>{activity['titulo']}</b>",
        "",
        f'🔗 <a href="{activity["url"]}">Ver na Steam</a>',
    )

    return card

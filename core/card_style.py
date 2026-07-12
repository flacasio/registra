"""
Padroes visuais dos cards do Rezistro.
"""

from config import DISPLAY_EMOJI, DISPLAY_NAME
from core.text import format_datetime_sp


def set_network_title(card, icon, network, action):
    card.set_title(f"{icon} <b>{network}</b>")
    prefix = f"{DISPLAY_EMOJI} " if DISPLAY_EMOJI else ""
    card.add_line(f"{prefix}{DISPLAY_NAME} {action}")
    return card


def add_posted_at(card, value):
    if not value:
        return card

    card.add_lines(
        "",
        f"🕒 {format_datetime_sp(value)}",
    )
    return card

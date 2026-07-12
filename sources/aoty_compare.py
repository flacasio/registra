"""
Monitor de notas alteradas no AOTY.
"""

import json
from pathlib import Path

from config import (
    AOTY_COMPARE_MAX_PAGES,
    AOTY_COMPARE_PAGES_PER_RUN,
    AOTY_USER,
)

from core.aoty import AotyRateLimitedError, ratings_page
from core.cache import CACHE_DIR
from core.console import header, info, success, warning
from core.telegram import send

from parsers.aoty_ratings import parse
from templates.aoty_compare import make_card


MODULE = "aoty_compare"
STATE_FILE = CACHE_DIR / f"{MODULE}.json"


def _load_state():
    if not STATE_FILE.exists():
        return {
            "ratings": {},
            "next_page": 1,
            "initialized": False,
        }

    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        state = {}

    return {
        "ratings": state.get("ratings", {}),
        "next_page": int(state.get("next_page", 1) or 1),
        "initialized": bool(state.get("initialized")),
    }


def _save_state(state):
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )


def _page_window(start_page):
    max_pages = max(1, AOTY_COMPARE_MAX_PAGES)
    pages_per_run = max(1, AOTY_COMPARE_PAGES_PER_RUN)
    end_page = min(max_pages, start_page + pages_per_run - 1)
    return range(start_page, end_page + 1)


def _next_page_after(window):
    max_pages = max(1, AOTY_COMPARE_MAX_PAGES)
    last_page = list(window)[-1]

    if last_page >= max_pages:
        return 1

    return last_page + 1


def _scan_pages(pages):
    found = {}

    for page in pages:
        info(f"Baixando pagina de notas {page}...")

        html = ratings_page(page)
        ratings = parse(html)

        if not ratings:
            warning(f"Nenhuma nota encontrada na pagina {page}.")
            break

        for item in ratings:
            found[item["id"]] = item

    return found


def _initial_scan_step(state):
    pages = list(_page_window(state["next_page"]))
    found = _scan_pages(pages)

    if not found:
        state["next_page"] = 1
        state["initialized"] = True
        _save_state(state)
        return 0, True

    state["ratings"].update(found)

    last_page = pages[-1]

    if last_page >= max(1, AOTY_COMPARE_MAX_PAGES):
        state["next_page"] = 1
        state["initialized"] = True
        done = True
    else:
        state["next_page"] = _next_page_after(pages)
        done = False

    _save_state(state)
    return len(found), done


def _changed_items(old_ratings, current):
    changed = []

    for item_id, item in current.items():
        old = old_ratings.get(item_id)

        if not old:
            continue

        old_rating = old.get("rating")
        new_rating = item.get("rating")

        if str(old_rating) == str(new_rating):
            continue

        changed.append({
            "id": f"{item_id}|{old_rating}|{new_rating}",
            "artist": item.get("artist", ""),
            "album": item.get("album", ""),
            "image": item.get("image", ""),
            "url": item.get("url", item_id),
            "old_rating": old_rating,
            "new_rating": new_rating,
        })

    return changed


def run():
    header("AOTY • Compare")

    if not AOTY_USER:
        warning("AOTY_USER nao configurado.")
        return

    state = _load_state()

    try:
        if not state["initialized"]:
            total_before = len(state["ratings"])
            count, done = _initial_scan_step(state)
            total_after = total_before + count

            if done:
                warning(
                    f"Base inicial concluida com {len(state['ratings'])} nota(s). "
                    "Mudancas futuras serao notificadas."
                )
            else:
                warning(
                    f"Base inicial em andamento: {total_after} nota(s) salvas. "
                    "Continuo na proxima execucao."
                )

            return

        pages = list(_page_window(state["next_page"]))
        current = _scan_pages(pages)
    except AotyRateLimitedError:
        warning("AOTY limitou as requisicoes. Vou tentar de novo na proxima execucao.")
        return

    if not current:
        state["next_page"] = 1
        _save_state(state)
        warning("Nenhuma nota encontrada neste bloco.")
        return

    changed = _changed_items(state["ratings"], current)

    state["ratings"].update(current)
    state["next_page"] = _next_page_after(pages)
    _save_state(state)

    if not changed:
        warning("Nenhuma nota alterada neste bloco.")
        return

    enviados = 0

    for activity in changed:
        info("Montando card...")

        card = make_card(activity)

        info("Enviando Telegram...")

        send(card)
        enviados += 1

    success(f"{enviados} card(s) enviado(s).")

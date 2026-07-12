"""
Interpretar atividades do Serializd.
"""

from core.serializd import image_url, review_url, show_url


def _clean(value):
    if value is None:
        return ""

    return str(value).strip()


def _activity_id(item, data, review):
    parts = [
        item.get("type"),
        item.get("id"),
        data.get("reviewId"),
        review.get("id"),
        item.get("dateAdded"),
        item.get("text"),
    ]

    return "|".join(_clean(part) for part in parts if _clean(part))


def _kind(item_type, data, review):
    if item_type == "reviewItem":
        if data.get("reviewIsLog") or review.get("isLog"):
            return "LOGGED"

        if data.get("reviewRating") or review.get("rating"):
            return "RATED"

        return "REVIEWED"

    if item_type == "watchlistItem":
        return "WATCHLIST"

    if item_type == "currentlyWatchingItem":
        return "CURRENTLY_WATCHING"

    if item_type == "pausedItem":
        return "PAUSED"

    if item_type == "droppedItem":
        return "DROPPED"

    return "ACTIVITY"


def _episode_label(review):
    number = review.get("episodeNumber")
    name = _clean(review.get("episodeName"))

    if number and name:
        return f"Episódio {number}: {name}"

    if number:
        return f"Episódio {number}"

    return name


def _season_label(value):
    text = _clean(value)

    if text.lower().startswith("season "):
        return "Temporada " + text.split(" ", 1)[1].strip()

    return text


def parse(payload):
    items = payload.get("items", []) if isinstance(payload, dict) else []
    activities = []

    for item in items:
        data = item.get("data") or {}
        review = data.get("review") or {}
        item_type = item.get("type", "")

        show = _clean(
            data.get("showName")
            or review.get("showName")
            or data.get("name")
            or item.get("text")
        )

        if not show:
            continue

        review_id = data.get("reviewId") or review.get("id")
        show_id = data.get("showId") or review.get("showId")
        rating = data.get("reviewRating")

        if rating is None:
            rating = review.get("rating")

        image_path = (
            data.get("showImage")
            or review.get("showBannerImage")
            or data.get("image")
            or data.get("posterPath")
        )

        activities.append({
            "id": _activity_id(item, data, review),
            "kind": _kind(item_type, data, review),
            "type": item_type,
            "text": _clean(item.get("text")),
            "show": show,
            "season": _season_label(data.get("seasonName") or review.get("seasonName")),
            "episode": _episode_label(review),
            "rating": rating,
            "review": _clean(data.get("reviewText") or review.get("reviewText")),
            "date_added": item.get("dateAdded") or review.get("dateAdded"),
            "backdate": review.get("backdate"),
            "image": image_url(image_path),
            "url": review_url(review_id) or show_url(show_id),
        })

    return activities

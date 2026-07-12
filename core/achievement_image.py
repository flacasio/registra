"""
Montagem de imagem composta para conquistas.
"""

from io import BytesIO
from pathlib import Path
import re

from core.downloader import download_bytes
from core.image import steam_cover


OUT_DIR = Path("cache") / "images" / "achievements"


def _safe(value):
    text = str(value)
    text = re.sub(r"[^a-zA-Z0-9_.-]+", "_", text)
    return text.strip("_") or "achievement"


def _open_image(url, Image):
    data = download_bytes(url)
    return Image.open(BytesIO(data)).convert("RGB")


def _fit_cover(image, size, Image):
    image = image.copy()
    image.thumbnail(size)

    canvas = Image.new("RGB", size, (17, 24, 39))
    x = (size[0] - image.width) // 2
    y = (size[1] - image.height) // 2
    canvas.paste(image, (x, y))
    return canvas


def achievement_card_image(activity):
    icon = activity.get("icon")
    cover = activity.get("game_cover") or steam_cover(activity["appid"])

    if not icon:
        return cover

    if not cover:
        return icon

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return icon or cover

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUT_DIR / f"{_safe(activity['id'])}.jpg"

    if output.exists():
        return str(output)

    try:
        cover_img = _fit_cover(_open_image(cover, Image), (360, 520), Image)
        icon_img = _fit_cover(_open_image(icon, Image), (260, 260), Image)
    except Exception:
        return icon or cover

    canvas = Image.new("RGB", (900, 520), (10, 16, 26))
    canvas.paste(cover_img, (0, 0))

    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (430, 70, 830, 470),
        radius=24,
        fill=(25, 35, 54),
        outline=(64, 85, 120),
        width=3,
    )
    canvas.paste(icon_img, (500, 110))

    draw.text((500, 390), "Nova conquista", fill=(235, 241, 255))
    draw.text((500, 420), activity.get("game", "Steam"), fill=(154, 170, 196))

    canvas.save(output, "JPEG", quality=92)
    return str(output)

"""
Tratamento de texto exibido nos cards.
"""

import re
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from config import DISPLAY_NAME, REAL_NAME


try:
    SAO_PAULO = ZoneInfo("America/Sao_Paulo")
except ZoneInfoNotFoundError:
    SAO_PAULO = timezone(timedelta(hours=-3), name="America/Sao_Paulo")

MONTHS_PT = [
    "",
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
]

COMMON_TRANSLATIONS = {
    "Recommended": "Recomendado",
    "Not Recommended": "Não recomendado",
    "Posted": "Publicado",
    "played": "jogado",
    "hours played": "horas jogadas",
    "Currently reading": "Lendo agora",
    "Want to read": "Quero ler",
}

EDITION_KEYWORDS = (
    "anniversary",
    "aniversário",
    "bonus track",
    "bonus tracks",
    "collector's",
    "collectors",
    "deluxe",
    "edition",
    "edição",
    "expanded",
    "extended",
    "limited",
    "portuguese",
    "português",
    "reissue",
    "remaster",
    "remastered",
    "special",
    "version",
    "versão",
)

EDITION_SUFFIX = re.compile(
    r"(?:\s*[-–—:]\s*)?[\[(](?P<label>[^)\]]+)[)\]]\s*$",
    re.IGNORECASE,
)

DASH_EDITION_SUFFIX = re.compile(
    r"\s*[-–—:]\s*(?P<label>[^\-–—:]+)\s*$",
    re.IGNORECASE,
)


def translate_common_text(text):
    for original, translated in COMMON_TRANSLATIONS.items():
        text = text.replace(original, translated)

    return text


def display_text(value):
    if value is None:
        return ""

    text = str(value)

    if REAL_NAME and DISPLAY_NAME:
        text = text.replace(REAL_NAME, DISPLAY_NAME)

    return translate_common_text(text)


def clean_media_title(value):
    """Remove apenas sufixos finais que descrevem edição ou versão."""
    if value is None:
        return ""

    title = str(value).strip()

    while title:
        match = EDITION_SUFFIX.search(title) or DASH_EDITION_SUFFIX.search(title)

        if not match:
            break

        label = match.group("label").casefold()

        if not any(keyword.casefold() in label for keyword in EDITION_KEYWORDS):
            break

        title = title[:match.start()].rstrip(" -–—:")

    return title


def _coerce_datetime(value):
    if value is None or value == "":
        return None

    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value, tz=SAO_PAULO)
    else:
        text = str(value).strip()

        if not text:
            return None

        if text.isdigit():
            dt = datetime.fromtimestamp(int(text), tz=SAO_PAULO)
        else:
            try:
                dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
            except ValueError:
                for pattern in (
                    "%a, %d %b %Y %H:%M:%S %z",
                    "%a, %d %b %Y %H:%M:%S %Z",
                    "%a, %d %b %Y %H:%M:%S",
                    "%b %d, %Y %I:%M%p",
                    "%B %d, %Y %I:%M%p",
                    "%b %d, %Y",
                    "%B %d, %Y",
                ):
                    try:
                        dt = datetime.strptime(text, pattern)
                        break
                    except ValueError:
                        dt = None

                if dt is None:
                    return None

    if dt.tzinfo is None:
        return dt.replace(tzinfo=SAO_PAULO)

    return dt.astimezone(SAO_PAULO)


def format_datetime_sp(value, empty="Data desconhecida"):
    dt = _coerce_datetime(value)

    if dt is None:
        return empty

    return f"{dt:%d/%m/%Y}, às {dt:%H:%M}"


def format_date_sp(value, empty="Data desconhecida"):
    dt = _coerce_datetime(value)

    if dt is None:
        return empty

    return f"{dt:%d/%m/%Y}"

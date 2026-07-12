"""
Interpretar comentarios do perfil da Steam.
"""

from bs4 import BeautifulSoup


def _parse_comment(comment):
    comment_id = comment.get("id", "").replace("comment_", "")

    author = "Desconhecido"
    author_link = comment.find("a", class_="commentthread_author_link")

    if author_link:
        author = author_link.get_text(strip=True)

    avatar = None

    for img in comment.find_all("img"):
        src = img.get("src", "")

        if "avatars.akamai.steamstatic.com" not in src:
            continue

        avatar = src.replace(
            "avatars.akamai.steamstatic.com",
            "avatars.fastly.steamstatic.com",
        )

        if avatar.endswith(".jpg") and not avatar.endswith("_full.jpg"):
            avatar = avatar.replace(".jpg", "_full.jpg")

        break

    text = ""
    text_div = comment.find("div", class_="commentthread_comment_text")

    if text_div:
        text = text_div.get_text(strip=True)

    timestamp = 0
    timestamp_div = comment.find(
        "div",
        class_="commentthread_comment_timestamp",
        attrs={"data-timestamp": True},
    )

    if timestamp_div:
        try:
            timestamp = int(timestamp_div["data-timestamp"])
        except Exception:
            pass

    return {
        "id": comment_id,
        "author": author,
        "avatar": avatar,
        "text": text,
        "timestamp": timestamp,
    }


def parse_all(data):
    html = data.get("comments_html", "")

    if not html:
        raise RuntimeError("Nenhum comentario encontrado.")

    soup = BeautifulSoup(html, "html.parser")
    comments = soup.find_all("div", class_="commentthread_comment")

    if not comments:
        raise RuntimeError("Nao foi possivel localizar comentarios.")

    return [_parse_comment(comment) for comment in comments]


def parse(data):
    comments = parse_all(data)
    return comments[0]

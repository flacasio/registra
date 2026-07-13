from bs4 import BeautifulSoup
import hashlib


def _clean(text):
    return " ".join(str(text or "").split())


def _stable_id(user, date, text):
    seed = "|".join(
        part.lower()
        for part in (
            _clean(user),
            _clean(date),
            _clean(text),
        )
        if part
    )
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()


def _parse_item(li):

    shout = li.select_one(":scope > .shout-container > .shout")
    if shout is None:
        return None

    usuario = shout.select_one(".shout-user a")
    data = shout.select_one("time")
    corpo = shout.select_one(".shout-body")
    user = usuario.get_text(strip=True) if usuario else ""
    date = data["datetime"] if data and data.has_attr("datetime") else ""
    text = corpo.get_text(" ", strip=True) if corpo else ""

    avatar = (
        li.select_one(".shout-user-avatar img")
        or li.select_one(".avatar img")
    )

    item = {
        "id": _stable_id(user, date, text),
        "user": user,
        "date": date,
        "text": text,
        "avatar": avatar.get("src") if avatar else None,
        "replies": []
    }

    lista_respostas = li.select_one(":scope > ul.shout-list")

    if lista_respostas:

        for resposta in lista_respostas.select(":scope > li.shout-list-item"):

            reply = _parse_item(resposta)

            if reply:
                item["replies"].append(reply)

    return item


def parse(html):

    soup = BeautifulSoup(html, "html.parser")

    comentarios = []

    lista = soup.select_one("ul.shout-list")

    if lista is None:
        return comentarios

    for li in lista.select(":scope > li.shout-list-item"):

        comentario = _parse_item(li)

        if comentario:
            comentarios.append(comentario)

    return comentarios

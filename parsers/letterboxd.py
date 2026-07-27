"""
============================================================
Rezistro
Arquivo: parsers/letterboxd.py
Versão: 1.1
============================================================

Responsabilidade:
Interpretar o feed RSS do Letterboxd.

Recebe:
    BeautifulSoup (XML)

Retorna:
    dict
"""

import re

from bs4 import BeautifulSoup


RATING_SUFFIX = re.compile(r"\s+-\s+(?P<rating>★+(?:½)?)\s*$")


def _split_title_and_rating(value):
    title = value.strip()
    match = RATING_SUFFIX.search(title)

    if not match:
        return title, ""

    rating = match.group("rating")
    clean_title = title[:match.start()].rstrip()
    return clean_title, rating


def _parse_item(item):
    titulo = item.find("title")
    link = item.find("link")
    guid = item.find("guid")
    descricao = item.find("description")

    if titulo is None:
        raise RuntimeError("Título não encontrado.")

    if guid is None:
        raise RuntimeError("GUID não encontrado.")

    descricao_html = BeautifulSoup(
        descricao.text if descricao else "",
        "html.parser",
    )

    imagem = descricao_html.find("img")
    clean_title, rating = _split_title_and_rating(titulo.text)

    return {
        "id": guid.text.strip(),
        "tipo": "WATCH",
        "titulo": clean_title,
        "rating": rating,
        "url": link.text.strip() if link else "",
        "published": (
            item.find("pubDate").text.strip()
            if item.find("pubDate")
            else ""
        ),
        "poster": imagem.get("src") if imagem else None,
    }


def parse_all(soup):
    return [
        _parse_item(item)
        for item in soup.find_all("item")
    ]


def parse(soup):
    items = parse_all(soup)

    if not items:
        raise RuntimeError("Nenhuma atividade encontrada.")

    return items[0]

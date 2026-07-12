"""
============================================================
Rezistro
Arquivo: parsers/letterboxd.py
Versão: 1.0
============================================================

Responsabilidade:
Interpretar o feed RSS do Letterboxd.

Recebe:
    BeautifulSoup (XML)

Retorna:
    dict
"""

from bs4 import BeautifulSoup


def _parse_item(item):


    titulo = item.find("title")
    link = item.find("link")
    guid = item.find("guid")
    descricao = item.find("description")

    if titulo is None:

        raise RuntimeError(
            "Título não encontrado."
        )

    if guid is None:

        raise RuntimeError(
            "GUID não encontrado."
        )

    descricao_html = BeautifulSoup(

        descricao.text if descricao else "",

        "html.parser"

    )

    imagem = descricao_html.find("img")

    return {

        "id":
            guid.text.strip(),

        "tipo":
            "WATCH",

        "titulo":
            titulo.text.strip(),

        "url":
            link.text.strip()
            if link
            else "",

        "published":
            item.find("pubDate").text.strip()
            if item.find("pubDate")
            else "",

        "poster":
            imagem.get("src")
            if imagem
            else None

    }


def parse_all(soup):
    return [
        _parse_item(item)
        for item in soup.find_all("item")
    ]


def parse(soup):
    items = parse_all(soup)

    if not items:
        raise RuntimeError(
            "Nenhuma atividade encontrada."
        )

    return items[0]

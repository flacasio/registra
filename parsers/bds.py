"""
Interpretar atividades do Banco de Series.
"""

import re


def _posted_at(atividade):
    data_tag = (
        atividade.find("time")
        or atividade.find(attrs={"datetime": True})
        or atividade.find(class_=re.compile("data|date|time", re.I))
    )

    if not data_tag:
        return ""

    return (
        data_tag.get("datetime")
        or data_tag.get("title")
        or data_tag.get_text(" ", strip=True)
    )


def _parse_activity(atividade):
    imagem = atividade.find("img")
    links = atividade.find_all("a")
    nota = atividade.find("b")

    if imagem is None or len(links) < 2:
        return None

    match = re.search(
        r"serieid=(\d+)",
        links[0].get("href", "")
    )

    if not match:
        return None

    serie_id = match.group(1)
    raw = imagem.get("title", "")
    tipo = "RATE" if "Atribuiu nota" in raw else "WATCH"

    return {
        "id": (
            f"bds_{serie_id}_{links[1].text.strip()}_"
            f"{tipo}_{nota.text.strip() if nota else ''}"
        ),
        "tipo": tipo,
        "acao": "Avaliou episodio" if tipo == "RATE" else "Assistiu episodio",
        "serie": links[0].text.strip(),
        "episodio": links[1].text.strip(),
        "nota": nota.text.strip() if nota else None,
        "poster": f"https://bancodeseries.com.br/images/posters/{serie_id}.jpg",
        "posted_at": _posted_at(atividade),
    }


def parse_all(soup):
    perfil = soup.find("div", id="perfillastcheckins")

    if perfil is None:
        raise RuntimeError("Bloco 'perfillastcheckins' nao encontrado.")

    atividades = []

    for item in perfil.find_all("small"):
        activity = _parse_activity(item)

        if activity:
            atividades.append(activity)

    if not atividades:
        raise RuntimeError("Atividade nao encontrada.")

    return atividades


def parse(soup):
    return parse_all(soup)[0]

"""
============================================================
Rezistro
Arquivo: core/cache.py
Versão: 2.0
============================================================

Responsabilidade:
Armazenar o último estado conhecido
de cada módulo.
"""

import json
from pathlib import Path


CACHE_DIR = Path("cache")

CACHE_DIR.mkdir(
    exist_ok=True
)


# ==========================================================
# CAMINHO
# ==========================================================

def _file(module):

    return CACHE_DIR / f"{module}.json"


def cache_current(module):
    arquivo = _file(module)

    if not arquivo.exists():
        return ""

    return arquivo.read_text(
        encoding="utf-8"
    )


def cache_save(module, value):
    arquivo = _file(module)

    arquivo.write_text(
        str(value),
        encoding="utf-8"
    )


# ==========================================================
# EVENTO ÚNICO
# ==========================================================

def cache_changed(module, value):

    arquivo = _file(module)

    atual = str(value)

    if arquivo.exists():

        anterior = arquivo.read_text(
            encoding="utf-8"
        )

    else:

        anterior = ""

    if atual == anterior:

        return False

    arquivo.write_text(

        atual,

        encoding="utf-8"

    )

    return True


# ==========================================================
# LISTAS
# ==========================================================

def cache_diff(module, values):

    """
    Recebe uma lista de IDs.

    Retorna apenas os IDs
    que ainda não existiam.
    """

    arquivo = _file(module)

    atuais = [

        str(v)

        for v in values

    ]

    if arquivo.exists():

        texto_antigo = arquivo.read_text(

            encoding="utf-8"

        )

        try:

            antigos = json.loads(

                texto_antigo

            )

        except json.JSONDecodeError:

            antigos = [

                texto_antigo

            ] if texto_antigo else []

        if not isinstance(antigos, list):

            antigos = [

                str(antigos)

            ]

    else:

        antigos = []

    antigos = [

        str(v)

        for v in antigos

    ]

    novos = [

        v

        for v in atuais

        if v not in antigos

    ]

    arquivo.write_text(

        json.dumps(

            atuais,

            ensure_ascii=False,

            indent=4

        ),

        encoding="utf-8"

    )

    return novos

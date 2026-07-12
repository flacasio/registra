"""
Ponto de entrada do Rezistro.

Exemplos:
    python run.py
    python run.py lastfm_recent
    python run.py --list
"""

import argparse
import importlib
import traceback
from pathlib import Path

from core.console import (
    blank,
    error,
    header,
    info,
    separator,
    success,
    warning,
)


SOURCES_DIR = Path("sources")


def listar_modulos():
    if not SOURCES_DIR.exists():
        return []

    modulos = []

    for arquivo in SOURCES_DIR.glob("*.py"):
        if arquivo.stem.startswith("__"):
            continue

        modulos.append(arquivo.stem)

    return sorted(modulos)


def executar(nome):
    try:
        modulo = importlib.import_module(f"sources.{nome}")

        if not hasattr(modulo, "run"):
            warning(f"{nome} nao possui funcao run().")
            return False

        modulo.run()
        return True

    except Exception:
        error(f"Falha em '{nome}'")
        print()
        traceback.print_exc()
        return False


def selecionar_modulos(nome):
    modulos = listar_modulos()

    if not nome:
        return modulos

    if nome not in modulos:
        error(f"Modulo nao encontrado: {nome}")
        info("Use python run.py --list para ver os nomes disponiveis.")
        return []

    return [nome]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Executa os monitores do Rezistro."
    )
    parser.add_argument(
        "modulo",
        nargs="?",
        help="Nome de um modulo em sources. Exemplo: lastfm_recent",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Mostra os modulos disponiveis e sai.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    header("Rezistro")

    modulos = listar_modulos()

    if args.list:
        if not modulos:
            warning("Nenhum modulo encontrado.")
            return

        info("Modulos disponiveis:")

        for nome in modulos:
            print(f"- {nome}")

        return

    escolhidos = selecionar_modulos(args.modulo)

    if not escolhidos:
        warning("Nada para executar.")
        return

    info(f"{len(escolhidos)} modulo(s) selecionado(s).")
    blank()

    sucessos = 0
    falhas = 0

    for nome in escolhidos:
        separator()
        info(f"Executando: {nome}")

        if executar(nome):
            success(f"{nome} finalizado.")
            sucessos += 1
        else:
            falhas += 1

        blank()

    separator()
    print()
    print("Resumo")
    print(f"Sucesso : {sucessos}")
    print(f"Falhas  : {falhas}")
    print(f"Total   : {len(escolhidos)}")


if __name__ == "__main__":
    main()

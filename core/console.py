"""
Rezistro
core/console.py

Responsabilidade:
Padronizar todas as mensagens exibidas
no terminal.

Autor:
Renan + ChatGPT
"""

LINE = "=" * 60


# ==========================================================
# CABEÇALHO
# ==========================================================

def header(title):
    """
    Exibe o cabeçalho do módulo.
    """

    print()
    print(LINE)
    print(f"Rezistro • {title}")
    print(LINE)


# ==========================================================
# SEÇÃO
# ==========================================================

def section(title):
    """
    Exibe um título de seção.
    """

    print()
    print(f"[ {title} ]")


# ==========================================================
# INFO
# ==========================================================

def info(text):
    """
    Informação comum.
    """

    print(f"[INFO] {text}")


# ==========================================================
# SUCESSO
# ==========================================================

def success(text):
    """
    Operação concluída.
    """

    print(f"[ OK ] {text}")


# ==========================================================
# AVISO
# ==========================================================

def warning(text):
    """
    Aviso.
    """

    print(f"[WARN] {text}")


# ==========================================================
# ERRO
# ==========================================================

def error(text):
    """
    Erro.
    """

    print(f"[ERRO] {text}")


# ==========================================================
# LINHA
# ==========================================================

def separator():
    """
    Linha horizontal.
    """

    print("-" * 60)


# ==========================================================
# LINHA EM BRANCO
# ==========================================================

def blank():
    """
    Linha vazia.
    """

    print()


# ==========================================================
# TESTE
# ==========================================================

if __name__ == "__main__":

    header("Console")

    info("Mensagem de informação")

    success("Tudo funcionando")

    warning("Exemplo de aviso")

    error("Exemplo de erro")

    separator()

    print("Fim do teste.")

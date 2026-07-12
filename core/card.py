"""
============================================================
Rezistro
Arquivo: core/card.py
Versão: 1.0
============================================================

Responsabilidade:
Representar um card padrão do Rezistro.

Todos os módulos (BDS, Goodreads, Steam, etc.)
devem criar um objeto Card e enviá-lo para o
core.telegram.
"""

from core.text import display_text


class Card:

    def __init__(self):

        self.image = None

        self.title = ""

        self.lines = []

        self.id_ref = None

    # ======================================================
    # TÍTULO
    # ======================================================

    def set_title(self, title):

        self.title = display_text(title)

        return self

    # ======================================================
    # IMAGEM
    # ======================================================

    def set_image(self, image):

        self.image = image

        return self

    # ======================================================
    # UMA LINHA
    # ======================================================

    def add_line(self, text):

        if text:

            self.lines.append(display_text(text))

        return self

    # ======================================================
    # VÁRIAS LINHAS
    # ======================================================

    def add_lines(self, *texts):

        for text in texts:

            if text:

                self.lines.append(display_text(text))

        return self

    # ======================================================
    # ID INTERNO
    # ======================================================

    def set_id(self, value):

        self.id_ref = value

        return self

    # ======================================================
    # LEGENDA
    # ======================================================

    def to_caption(self):

        texto = self.title.strip()

        if self.lines:

            texto += "\n\n"

            texto += "\n".join(self.lines)

        return texto

    # ======================================================
    # DICIONÁRIO
    # ======================================================

    def to_dict(self):

        return {

            "image": self.image,

            "title": self.title,

            "lines": self.lines,

            "id_ref": self.id_ref

        }

    # ======================================================
    # DEBUG
    # ======================================================

    def __repr__(self):

        return (

            f"Card("

            f"title={self.title!r}, "

            f"lines={len(self.lines)}, "

            f"image={self.image!r}"

            f")"

        )

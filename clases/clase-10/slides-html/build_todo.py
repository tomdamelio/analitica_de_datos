"""
Junta TODAS las slides estaticas de la Clase 10 (las 50, incluido el Bloque 2
en su version estatica) en un solo HTML navegable.

Uso::

    python build_todo.py

Escribe `clase10_estatica_completa.html`.
"""

from comun import escribir
from interactivos import CSS_INTERACTIVOS
from _plotly_inline import PLOTLY_JS
import contenido_apertura
import contenido_bloque1
import contenido_bloque2
import contenido_bloque3
import contenido_bloque4
import contenido_bloque5
import contenido_bloque6
import contenido_cierre

TODAS = (contenido_apertura.SLIDES + contenido_bloque1.SLIDES + contenido_bloque2.SLIDES
        + contenido_bloque3.SLIDES + contenido_bloque4.SLIDES
        + contenido_bloque5.SLIDES + contenido_bloque6.SLIDES
        + contenido_cierre.SLIDES)

if __name__ == "__main__":
    print("total de slides:", len(TODAS))
    escribir("clase10_estatica_completa.html", TODAS,
            "Clase 10 — Reducción de dimensionalidad (PCA)",
            extra_css=CSS_INTERACTIVOS, extra_js=PLOTLY_JS)

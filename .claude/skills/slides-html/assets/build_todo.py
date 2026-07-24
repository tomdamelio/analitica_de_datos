"""
Junta TODOS los bloques de contenido en un solo HTML navegable (el deck final).

Uso::

    python build_todo.py

Escribe `deck_completo.html`. Correr esto DESPUES de cada tanda de cambios a cualquier
`contenido_*.py`, para tener siempre el deck combinado actualizado — pero mientras se itera
un bloque puntual, es mucho mas rapido correr `python contenido_bloqueN.py` solo (genera un
preview de nada mas que ese bloque).

AJUSTAR: la lista de imports y el orden de concatenacion segun los bloques reales del proyecto.
Si el deck usa KaTeX y/o Plotly, importar tambien CSS_INTERACTIVOS y el/los *_inline con las
librerias embebidas (generadas por scripts/embed_libs.py) y pasarlos a `escribir(...)`.
"""

from comun import escribir
from interactivos import CSS_INTERACTIVOS
# from _katex_inline import KATEX_CSS, KATEX_JS, KATEX_AUTORENDER_JS  # si hay formulas
# from _plotly_inline import PLOTLY_JS  # si hay widgets 3D/biplot

import contenido_apertura
import contenido_bloque1
import contenido_bloque2
# ... un import por bloque
import contenido_cierre

TODAS = (contenido_apertura.SLIDES + contenido_bloque1.SLIDES + contenido_bloque2.SLIDES
        # ... en el mismo orden que los imports
        + contenido_cierre.SLIDES)

if __name__ == "__main__":
    print("total de slides:", len(TODAS))
    escribir("deck_completo.html", TODAS, "Titulo del deck",
            extra_css=CSS_INTERACTIVOS,
            extra_js="")  # PLOTLY_JS si corresponde

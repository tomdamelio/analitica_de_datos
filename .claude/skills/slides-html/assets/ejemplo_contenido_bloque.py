"""
EJEMPLO de un archivo de contenido (un bloque tematico). Copiar este patron por cada bloque de
la clase/charla: `contenido_apertura.py`, `contenido_bloque1.py`, ..., `contenido_cierre.py`.

Cada uno importa de `comun` y `interactivos`, define B (numero de bloque) y C (su color), arma
una lista `SLIDES`, y se puede correr solo para previsualizar nada mas que este bloque:

    python ejemplo_contenido_bloque.py
"""

from comun import *
from interactivos import widget_formula_pasos, widget_comparador_metodos

B = 1                       # numero de este bloque (clave de COLOR_BLOQUE en comun.py)
C = COLOR_BLOQUE[B]
SLIDES = []

# --- portada del bloque -------------------------------------------------------------
SLIDES.append(portada_bloque(4, B, "Nombre del bloque",
                             "Una linea que resume de que se trata este bloque."))

# --- slide de texto/bullets simple ---------------------------------------------------
SLIDES.append(slide(5, B, "Un titulo que es la conclusion, no una etiqueta", f"""
    {bullets([
        f'Primer punto, con una palabra clave {alert("resaltada", B)} en el color del bloque.',
        'Segundo punto, con <strong>negrita</strong> para lo textualmente importante.',
        'Tercer punto.',
    ])}
    {caja("Por que importa", "El cuerpo de una caja destacada, con su propio color de borde.", C)}
    {nota("Una aclaracion chica al pie, no el mensaje principal de la slide.")}
"""))

# --- slide con una formula ESTATICA (sin revelado por pasos) -------------------------
SLIDES.append(slide(6, B, "Una ecuacion de referencia", f"""
    <p class="parrafo-libre">Texto de contexto antes de la formula:</p>
    {ecuacion(r"y = \beta_0 + \beta_1 x")}
    {bullets(['Explicacion de cada termino en una lista comun, si no hace falta revelado por pasos.'])}
"""))

# --- slide con una formula que se REVELA termino a termino (flecha derecha) ----------
SLIDES.append(slide(7, B, "Una formula que se explica de a una parte", f"""
    <p class="parrafo-libre">Introduccion breve antes de la formula:</p>
    {widget_formula_pasos(
        r"\htmlClass{grupo-a}{a} + \htmlClass{grupo-b}{b} = \htmlClass{grupo-c}{c}",
        [
            ("a", VERDE, f'$\\textcolor{{{VERDE}}}{{a}}$ es el primer termino, explicado aca.'),
            ("b", AZUL, f'$\\textcolor{{{AZUL}}}{{b}}$ es el segundo, en un color distinto.'),
            ("c", VIOLETA, f'$\\textcolor{{{VIOLETA}}}{{c}}$ es el resultado.'),
        ],
        id_="formula-ejemplo")}
""", contenido_clase="densa"))

# --- slide con un widget que compara metodos/vistas (requiere datos.py + Plotly no) --
# datos_comparador = { ... } # cargar del JSON precomputado por datos.py
# SLIDES.append(slide(8, B, "Comparando dos vistas de los mismos datos", f"""
#     {widget_comparador_metodos(C, datos_comparador, id_="comparador-ejemplo")}
#     {nota("Los mismos puntos, reacomodados: clickeá cada botón para ver la transición.")}
# """, contenido_clase="centrado"))

# --- slide de figura estatica ---------------------------------------------------------
# SLIDES.append(slide(9, B, "Un resultado en imagen",
#     figura(MI_FIGURA_B64, "descripcion alt", "pie de figura, fiel a los numeros de origen."),
#     contenido_clase="centrado-img"))

# --- puntero a notebook de practica (patron de curso) --------------------------------
SLIDES.append(slide_notebook(10, B, "A la notebook",
    "Que va a practicar el estudiante en esta notebook.",
    "Un segundo renglon opcional de contexto."))


if __name__ == "__main__":
    from interactivos import CSS_INTERACTIVOS
    # from _plotly_inline import PLOTLY_JS  # solo si este bloque usa widgets 3D/biplot
    escribir("preview_ejemplo.html", SLIDES, "Preview — bloque de ejemplo",
            extra_css=CSS_INTERACTIVOS, extra_js="")

"""Clase 10 - BLOQUE 4: "Cuánta información conservamos" (slides 27 a 35)."""

from comun import *
from interactivos import widget_formula_pasos

B = 4
C = COLOR_BLOQUE[B]
SLIDES = []

SLIDES.append(portada_bloque(27, B, "Cuánta información conservamos",
                             "Reconstruir, medir el error y decidir cuántas componentes."))

SLIDES.append(slide(28, B, "Reconstruir un dato desde sus componentes", f"""
    <p class="parrafo-libre">Si los scores se armaron combinando las variables, se puede hacer
      el <strong>camino inverso</strong>:</p>
    {widget_formula_pasos(
        r"\htmlClass{grupo-x}{x_{ij}} \approx "
        r"\sum_{m=1}^{\htmlClass{grupo-M}{M}} "
        r"\htmlClass{grupo-z}{z_{im}}\,\htmlClass{grupo-phi}{\phi_{jm}}",
        [
            ("x", VERDE, f'$\\textcolor{{{VERDE}}}{{x_{{ij}}}}$ es el dato original: la variable '
                         f'$j$ del estudiante $i$;'),
            ("M", AZUL, f'$\\textcolor{{{AZUL}}}{{M}}$ es cuántas componentes usamos. Si $M = p$, '
                        f'la reconstrucción es <strong>exacta</strong>;'),
            ("z", ROJO, f'$\\textcolor{{{ROJO}}}{{z_{{im}}}}$ es el <em>score</em> del estudiante '
                        f'$i$ en la componente $m$;'),
            ("phi", MARRON, f'$\\textcolor{{{MARRON}}}{{\\phi_{{jm}}}}$ es el <em>loading</em> de '
                            f'la variable $j$ en esa componente.'),
        ], id_="formula-reconstruccion")}
    {caja("Por qué importa",
          f"Con $M$ componentes, esta es {alert('la mejor aproximación posible', B)} en $M$ dimensiones. "
          "Ninguna otra combinación lineal reconstruye mejor. Eso es lo que hace de PCA una técnica "
          "de <strong>compresión</strong>, no un resumen más.", C, ancho="88%")}
""", contenido_clase="densa"))

SLIDES.append(slide(29, B, "El error cae rápido: pocas componentes bastan",
    figura(RECONSTRUCCION_B64, "Error de reconstrucción",
          f'Error cuadrático medio al reconstruir las ocho variables de los 4.424 estudiantes. Con '
          f'<strong>1</strong> componente es 0,46; con <strong>4</strong> baja a 0,07; con las '
          f'<strong>8</strong> es exactamente {alert("cero", B)}: usar todas es solo rotar los ejes.'),
    contenido_clase="centrado-img"))

SLIDES.append(slide(30, B, "La varianza total se reparte entre las componentes", f"""
    {bullets([
        'Con variables <strong>estandarizadas</strong>, cada una aporta 1 unidad de varianza: la '
        'varianza total es exactamente $p$ (acá, <strong>8</strong>).',
        'Cada componente explica una porción de ese total: su <strong>autovalor</strong>.',
        'La <strong>PVE</strong> de una componente es esa porción sobre el total. Sumando todas, '
        'siempre da 100%.',
    ])}
    {tabla(["Componente", "1", "2", "3", "4", "5", "6", "7", "8"], [
        ("PVE (%)", ["54,2", "17,3", "12,3", "9,5", "3,1", "2,1", "1,1", "0,4"]),
        ("Acumulada (%)", ["54,2", "71,5", "83,8", "93,3", "96,4", "98,5", "99,6", "100"]),
    ])}
"""))

SLIDES.append(slide(31, B, "El scree plot y el criterio del codo",
    figura(SCREE_B64, "Scree plot",
          f'Se busca el <strong>codo</strong>: el punto donde cada componente adicional deja de '
          f'aportar. Acá, {alert("3 componentes", B)} llegan al 80% de la varianza y '
          f'{alert("4", B)} superan el 90%.'),
    contenido_clase="centrado-img"))

SLIDES.append(slide(32, B, "La PVE es el $R^2$ de la aproximación", f"""
    {caja("Un gancho con lo que ya saben",
          "La proporción de varianza explicada por las primeras $M$ componentes se interpreta "
          "<strong>exactamente</strong> como el $R^2$ de la regresión lineal: qué fracción de la "
          "variabilidad total se logra explicar.", C, ancho="88%")}
    {bullets([
        'Con 2 componentes explicamos el <strong>71,5%</strong> de la variabilidad de las ocho variables.',
        f'Por eso el biplot en dos dimensiones es una representación {alert("fiel", B)} del dataset completo.',
        'Y por eso retener componentes es quedarse con la señal y descartar, sobre todo, ruido.',
    ])}
"""))

SLIDES.append(slide(33, B, "Máxima varianza y mínimo error son lo mismo", f"""
    {bullets([
        'La varianza total de los datos se reparte en <strong>dos partes</strong>: lo que capturan '
        'las primeras $M$ componentes, más el <strong>error</strong> de reconstruirlos con esas $M$.',
        'Como la varianza total es un número <strong>fijo</strong>, subir una es bajar la otra.',
    ])}
    {caja("La equivalencia, cerrada",
          f"<strong>Maximizar</strong> la varianza explicada por las primeras $M$ componentes es "
          f"{alert('exactamente lo mismo', B)} que <strong>minimizar</strong> el error de reconstrucción.",
          C, ancho="88%")}
    {nota("Es la razón por la que las dos definiciones del Bloque 2, máxima varianza y mínima "
         "distancia, describen el mismo objeto.")}
"""))

SLIDES.append(slide(34, B, "Cuántas retener: no hay respuesta única", f"""
    {bullets([
        'No existe un criterio objetivo y universal. En análisis no supervisado, la decisión es '
        'en parte un <strong>juicio</strong>.',
        'Se mira el <strong>codo</strong> del scree plot, o se fija un umbral de varianza acumulada '
        '(80% o 90%).',
        'Regla práctica: si las primeras componentes no muestran nada interesante, las siguientes '
        'tampoco suelen hacerlo.',
    ])}
    {caja("Cuando sí hay criterio objetivo",
          "Si las componentes se usan como <strong>predictores</strong> de un modelo posterior, el "
          "número se elige como cualquier hiperparámetro: por <strong>validación cruzada</strong>.",
          C, ancho="88%")}
"""))

SLIDES.append(slide_notebook(35, B, "A la notebook",
    "Reconstruir un dato con 1, 2 y todas las componentes, y ver caer el error.",
    "<strong>Ejercicio:</strong> cuántas componentes hacen falta para llegar al 90%."))

if __name__ == "__main__":
    from interactivos import CSS_INTERACTIVOS
    escribir("preview_bloque4.html", SLIDES, "Clase 10 — Bloque 4 (preview)",
            extra_css=CSS_INTERACTIVOS)

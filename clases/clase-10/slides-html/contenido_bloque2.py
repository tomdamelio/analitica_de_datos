"""
Clase 10 - BLOQUE 2: "Qué es una componente principal" (slides 10 a 20).

Version ESTATICA (HTML/CSS), para tener la clase completa en este formato
antes de decidir cuales pasan a interactivas. La version animada (Manim/video)
ya aprobada vive en `slides-beanim/bloque2.py` — esta es una alternativa, no
un reemplazo; se elige una u otra (o se arma el mashup) en el paso siguiente.
"""

from comun import *
from interactivos import widget_recta_girando, widget_plano_3d, widget_formula_pasos

B = 2
C = COLOR_BLOQUE[B]
SLIDES = []

SLIDES.append(portada_bloque(10, B, "Qué es una componente principal",
                             "De la intuición en dos dimensiones al caso general."))

SLIDES.append(slide(11, B, "En 2D: la dirección de máxima varianza",
    figura(PCA2D_B64, "PCA en 2D",
          f'Materias aprobadas en 1er y 2do semestre (estandarizadas). La recta negra es la '
          f'<strong>primera componente</strong>: la dirección a lo largo de la cual los puntos '
          f'varían más. Ella sola concentra el {alert("95,2%", B)} de la variabilidad de las dos variables.'),
    contenido_clase="centrado-img"))

SLIDES.append(slide(12, B, "…y a la vez la recta más cercana a los puntos", f"""
    {widget_recta_girando(C, id_="recta1")}
    {nota(f'Arrastrá el ángulo (o apretá "Girar"). Los <strong>segmentos rojos</strong> son los '
         f'errores de proyección: cuando la recta llega a la primera componente, esos errores '
         f'alcanzan su <strong>mínimo</strong> y, en ese mismo instante, las proyecciones quedan '
         f'{alert("lo más dispersas posible", B)}.')}
""", contenido_clase="centrado"))

SLIDES.append(slide(13, B, "Dos lecturas del mismo problema", f"""
    <div class="columnas">
      {caja("Máxima varianza",
            "La dirección a lo largo de la cual los datos proyectados tienen la "
            "<strong>mayor dispersión</strong> posible.", C)}
      {caja("Mínima distancia",
            "La recta que <strong>minimiza</strong> la suma de distancias al cuadrado entre "
            "cada punto y su proyección.", VERDE)}
    </div>
    {bullets([
        f'Las dos definiciones llevan a la {alert("misma solución matemática", B)}.',
        'No es casualidad: la varianza total es fija, así que todo lo que la proyección captura '
        'es exactamente lo que el error deja de perder.',
        'Volvemos sobre esto en el Bloque 4, ya con números.',
    ])}
"""))

SLIDES.append(slide(14, B, "En 3D: dos componentes definen un plano", f"""
    {widget_plano_3d(C, id_="plano1")}
    {nota('Arrastrá para rotar, hacé zoom con la rueda. Las <strong>dos primeras componentes</strong> '
         'generan el plano que mejor se apoya sobre la nube de tres variables académicas.')}
""", contenido_clase="centrado"))

SLIDES.append(slide(15, B, "Una componente es una combinación lineal", f"""
    <p class="parrafo-libre">Cada componente es una <strong>variable nueva</strong>, construida
      ponderando las originales:</p>
    {widget_formula_pasos(
        r"\htmlClass{grupo-z}{Z_m} = "
        r"\htmlClass{grupo-phi}{\phi_{1m}} \htmlClass{grupo-x}{X_1} + "
        r"\htmlClass{grupo-phi}{\phi_{2m}} \htmlClass{grupo-x}{X_2} + \cdots + "
        r"\htmlClass{grupo-phi}{\phi_{pm}} \htmlClass{grupo-x}{X_p}",
        [
            ("x", VERDE, f'$\\textcolor{{{VERDE}}}{{X_1,\\dots,X_p}}$ son las variables originales, '
                         f'ya centradas en media cero;'),
            ("phi", AZUL, f'los <em>loadings</em> $\\textcolor{{{AZUL}}}{{\\phi_{{jm}}}}$ son los '
                          f'<strong style="color:{AZUL}">pesos</strong>: cuánto aporta cada '
                          f'variable a la componente $m$;'),
            ("z", VIOLETA, f'los <em>scores</em> $\\textcolor{{{VIOLETA}}}{{Z_m}}$ son los '
                           f'<strong style="color:{VIOLETA}">valores</strong> resultantes: la '
                           f'posición de cada estudiante en esa nueva variable.'),
        ], id_="formula-lineal")}
    {nota('Los loadings describen <strong>variables</strong>; los scores describen '
         '<strong>observaciones</strong>. Es la distinción que hace legible un biplot.')}
""", contenido_clase="densa"))

SLIDES.append(slide(16, B, "Por qué los pesos se normalizan", f"""
    {bullets([
        'Se exige que la suma de los cuadrados de los pesos sea <strong>igual a 1</strong>.',
        f'Sin esa restricción el problema {alert("no tendría solución", B)}: agrandando los '
        f'pesos, la varianza crecería sin límite.',
        'Normalizar obliga a buscar una <strong>dirección</strong> en el espacio de las '
        'variables, no una magnitud arbitraria.',
    ])}
    {caja("Cómo se calcula en la práctica",
          "Los pesos salen de la <strong>descomposición en autovectores y autovalores</strong> de "
          "la matriz de covarianzas (o de correlaciones, si estandarizamos). Cada componente es "
          "un <strong>autovector</strong>; la varianza que explica es su <strong>autovalor</strong>. "
          "No hace falta resolverlo a mano: lo hace la función de PCA.", C, ancho="88%")}
"""))

SLIDES.append(slide(17, B, "Cada componente es ortogonal a las anteriores", f"""
    {bullets([
        f'La segunda componente se busca igual que la primera, maximizando varianza, pero con '
        f'una condición extra: ser {alert("ortogonal", B)} (no correlacionada) con la primera.',
        'Lo mismo para la tercera respecto de las dos anteriores, y así sucesivamente.',
        'Cada una captura <strong>información nueva</strong>, no una repetición de la anterior.',
        'En total hay como máximo $\\min(n-1,\\,p)$ componentes. Con nuestras 8 variables, '
        '<strong>8 componentes</strong>.',
    ])}
    {nota('Usar <em>todas</em> las componentes no pierde nada: es solo <strong>rotar</strong> el '
         'sistema de coordenadas. La compresión aparece cuando nos quedamos con algunas.')}
"""))

SLIDES.append(slide(18, B, "El score de un estudiante, término a término",
    figura(SCORE_TERMINO_B64, "Score término a término",
          f'Aporte de cada variable al score en PC1 de un estudiante concreto: su <strong>valor '
          f'estandarizado por el loading</strong> de esa variable. Las cuatro variables de '
          f'{alert("materias", B)} explican casi todo el score; la nota de admisión y la edad, '
          f'prácticamente nada.'),
    contenido_clase="centrado-img"))

SLIDES.append(slide(19, B, "Las componentes están definidas salvo el signo", f"""
    {caja("Un detalle que confunde",
          "Dos programas pueden devolver la <strong>misma componente con el signo invertido</strong>, "
          "y ambos son correctos.", ROJO, ancho="88%")}
    {bullets([
        'Un vector de pesos define una <strong>dirección</strong>, y una dirección se extiende '
        'hacia los dos lados.',
        'Dar vuelta el signo de los loadings y el de los scores a la vez deja '
        '<strong>todo igual</strong>.',
        'Lo que importa es la <strong>geometría relativa</strong>: qué variables van juntas y '
        'cuáles se oponen.',
        'En la práctica conviene <strong>orientar</strong> cada componente para que se lea bien, '
        'como hicimos al poner el éxito académico hacia la derecha.',
    ])}
"""))

SLIDES.append(slide_notebook(20, B, "A la notebook",
    "Calcular un score <strong>a mano</strong> y comprobar que coincide con el del algoritmo.",
    "También: rotar la recta y ver cómo cambia la varianza proyectada."))

if __name__ == "__main__":
    from interactivos import CSS_INTERACTIVOS
    from _plotly_inline import PLOTLY_JS
    escribir("preview_bloque2.html", SLIDES, "Clase 10 — Bloque 2 (preview estática)",
            extra_css=CSS_INTERACTIVOS, extra_js=PLOTLY_JS)

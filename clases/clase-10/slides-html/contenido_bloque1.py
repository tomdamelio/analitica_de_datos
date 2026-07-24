"""Clase 10 - BLOQUE 1: "Por qué reducir" (slides 4 a 9)."""

from comun import *

B = 1
SLIDES = []

SLIDES.append(portada_bloque(4, B, "Por qué reducir",
                             "Cuando hay demasiadas variables para mirarlas."))

SLIDES.append(slide(5, B, "Aprendizaje no supervisado: no hay qué predecir", f"""
    {bullets([
        'Hasta ahora tuvimos siempre una variable respuesta $Y$. Acá <strong>no la hay</strong>: '
        'solo un conjunto de features $X_1,\\dots,X_p$.',
        f'El objetivo cambia: ya no es predecir, es {alert("descubrir estructura", B)} en los datos.',
        'Por eso el análisis no supervisado casi siempre es parte de un <strong>análisis exploratorio</strong>.',
        'Y por eso mismo es más <strong>subjetivo</strong>: no hay una respuesta correcta contra la '
        'cual validar, ni test set que nos diga si acertamos.',
    ])}
    {nota("ISLP, Sección 12.1.")}
"""))

SLIDES.append(slide(6, B, "Agrupar clientes que nadie etiquetó", f"""
    {caja("Un caso cotidiano",
          "Un sitio de compras online quiere recomendarle a cada persona lo que le interesa. "
          "Agrupa a sus clientes según su <strong>historial de navegación y compra</strong>, sin "
          "que nadie haya dicho de antemano a qué grupo pertenece cada uno.", COLOR_BLOQUE[B], ancho="82%")}
    {bullets([
        'Nadie definió los grupos: <strong>emergen de los datos</strong>.',
        'Un buscador hace lo mismo con historiales de clics para decidir qué resultados mostrar.',
        'PCA ataca una versión de ese problema: cuando hay <strong>muchas variables correlacionadas</strong>, '
        'resumirlas en unas pocas que conserven casi toda la variabilidad.',
    ])}
"""))

SLIDES.append(slide(7, B, "Varias variables dicen casi lo mismo",
    figura(CORRELACIONES_B64, "Correlaciones",
          f'Correlaciones del bloque académico. Las materias <strong>aprobadas en 1er y 2do '
          f'semestre</strong> correlacionan <strong>0,90</strong>: quien aprueba mucho en un '
          f'semestre aprueba mucho en el otro. Hay {alert("redundancia", B)} para explotar.'),
    contenido_clase="centrado-img"))

SLIDES.append(slide(8, B, "Con 8 variables ya hay 28 gráficos posibles", f"""
    {bullets([
        'Para mirar las relaciones de a pares hacen falta $p(p-1)/2$ diagramas de dispersión.',
        f'Con nuestras <strong>8 variables</strong> son <strong>28</strong> gráficos. Con las '
        f'<strong>24</strong> columnas numéricas del dataset, {alert("276", B)}.',
        'Ninguno muestra la foto completa: cada uno contiene solo una fracción de la información.',
    ])}
    {caja("La pregunta que abre PCA",
          "¿Existe una representación de <strong>pocas dimensiones</strong> que capture la mayor "
          "parte posible de la variabilidad de los datos?", COLOR_BLOQUE[B], ancho="82%")}
"""))

SLIDES.append(slide(9, B, "De 4.500 adjetivos a cinco factores", f"""
    {bullets([
        'En 1936, Allport y Odbert listaron <strong>4.500 términos</strong> que describen '
        'diferencias de personalidad.',
        f'Con análisis factorial (el pariente cercano de PCA), esos términos se redujeron '
        f'primero a 16 y finalmente a {alert("cinco", B)}: el modelo <strong>Big Five</strong> (OCEAN).',
        'De Raad y Barelds (2008) aplicaron PCA a <strong>2.365 ítems</strong> del léxico holandés '
        'y recuperaron el Big Five más tres factores adicionales.',
    ])}
    {caja("El principio, en una línea",
          "Con $p$ enorme, unas pocas <strong>dimensiones compuestas</strong> pueden resumir una "
          "variedad inmensa. Es exactamente lo que vamos a hacer hoy, en menor escala.",
          COLOR_BLOQUE[B], ancho="82%")}
"""))

if __name__ == "__main__":
    escribir("preview_bloque1.html", SLIDES, "Clase 10 — Bloque 1 (preview)")

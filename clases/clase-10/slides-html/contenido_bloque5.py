"""Clase 10 - BLOQUE 5: "Decisiones prácticas y alcance" (slides 36 a 43)."""

from comun import *
from interactivos import widget_no_lineales

B = 5
C = COLOR_BLOQUE[B]
SLIDES = []

SLIDES.append(portada_bloque(36, B, "Decisiones prácticas y alcance",
                             "Estandarizar, métodos no lineales y casos aplicados."))

SLIDES.append(slide(37, B, "¿Qué pasa si no estandarizamos?", f"""
    {caja("Antes de mirar el resultado",
          "Vamos a correr PCA sobre las ocho variables <strong>sin estandarizar</strong>. ¿Qué "
          "variable creen que va a dominar la primera componente, y por qué?", C, ancho="88%")}
    {bullets([
        'La <strong>nota de admisión</strong> va de 0 a 200; las materias aprobadas, de 0 a 10.',
        'Sus varianzas: <strong>210</strong> frente a <strong>9,6</strong>.',
        f'Como PCA busca {alert("máxima varianza", B)}, sin estandarizar la escala de medición '
        f'decide el resultado.',
    ])}
"""))

SLIDES.append(slide(38, B, "Sin escalar, una variable secuestra PC1",
    figura(ESCALADO_B64, "Comparación con y sin escalado",
          f'Pesos de PC1 sin escalar (izquierda) y escalando (derecha). Sin estandarizar, PC1 es '
          f'<strong>casi solo la nota de admisión</strong>; estandarizando, reparte peso entre las '
          f'materias y se vuelve interpretable. {alert("Salvo unidad común, se estandariza siempre.", B)}'),
    contenido_clase="centrado-img"))

SLIDES.append(slide(39, B, "Más allá de PCA: t-SNE y UMAP", f"""
    {widget_no_lineales(C, id_="nolineales1")}
    {nota('Son los <strong>mismos estudiantes</strong> en los tres botones. PCA es '
         '<strong>lineal</strong>; al pasar a t-SNE o UMAP los mismos puntos se reacomodan y los '
         f'grupos aparecen {alert("mucho más separados", B)}, porque preservan la vecindad local.')}
""", contenido_clase="centrado"))

SLIDES.append(slide(40, B, "Lo que t-SNE y UMAP no garantizan", f"""
    {caja("Tres cuidados", "<ul class='bullets-caja'>"
          "<li><strong>No preservan distancias globales</strong>: la separación entre dos grupos "
          "lejanos en el dibujo no es interpretable.</li>"
          "<li><strong>Dependen de hiperparámetros</strong>: cambiar la <em>perplexity</em> o el "
          "número de vecinos cambia el gráfico.</li>"
          "<li><strong>Sus ejes no significan nada</strong>: no hay loadings que interpretar.</li>"
          "</ul>", C, ancho="90%")}
    {bullets([
        'No están en el capítulo 12 del libro: son un complemento moderno.',
        f'Regla: usalos para {alert("descubrir", B)} grupos, nunca para {alert("medir", B)} distancias.',
    ])}
"""))

SLIDES.append(slide(41, B, "PC1 como índice: el Nivel Socioeconómico", f"""
    {caja("Filmer y Pritchett (2001), <em>Demography</em>",
          "Para estimar la riqueza del hogar sin datos de gasto, construyeron un <strong>índice</strong> "
          "a partir de indicadores de <strong>posesión de bienes</strong> del hogar, usando PCA para "
          "derivar los ponderadores.", C, ancho="88%")}
    {bullets([
        'Los hogares se ordenan por su valor en <strong>PC1</strong> y se agrupan en '
        '<strong>quintiles</strong>, de más pobre a más rico.',
        'Vyas y Kumaranayake (2006) es la guía metodológica de referencia sobre cómo construirlo '
        'e interpretarlo.',
        '<strong>Punto de discusión:</strong> casi todos estos trabajos usan <em>solo</em> PC1. Hay '
        'literatura que propone combinar varias componentes, porque PC1 suele explicar una parte '
        'modesta de la varianza.',
    ])}
"""))

SLIDES.append(slide(42, B, "32 medidas de comportamiento, seis dimensiones", f"""
    {caja("Arguello y Crescenzi (2019)",
          "Analizaron con PCA hasta <strong>32 medidas de comportamiento</strong> por sesión "
          "(cantidad de búsquedas, clics, tiempos de permanencia, scrolls, movimientos del mouse) "
          "en estudios de búsqueda de información.", C, ancho="88%")}
    {bullets([
        'Objetivo: entender qué <strong>fenómenos latentes</strong> capturan esas medidas, y cómo '
        'influyen en las percepciones posteriores (carga de trabajo, dificultad, <em>engagement</em>).',
        f'Usaron la matriz de <strong>correlación</strong> y no la de covarianza, porque las medidas '
        f'están en escalas muy distintas: es {alert("el mismo argumento del escalado", B)} que vimos recién.',
        'Para elegir cuántas componentes: autovalor <strong>mayor a 1</strong>, y que cada componente '
        'tenga al menos <strong>dos variables</strong> con pesos altos.',
    ])}
"""))

SLIDES.append(slide(43, B, "Del componente al modelo", f"""
    {bullets([
        f'Aplicaron una <strong>rotación varimax</strong>: redistribuye los pesos para que cada '
        f'variable cargue fuerte en una sola componente. Facilita {alert("nombrarlas", B)}, y es '
        f'práctica estándar aplicada aunque el libro no la desarrolle.',
        'Así nombraron cada dimensión según qué medidas pesaban en ella, por ejemplo <em>abandono '
        'de búsquedas</em> o <em>ritmo de interacción</em>.',
        'Después usaron los <strong>scores</strong> de las componentes, en lugar de las 32 medidas '
        'originales, como predictores de un modelo de regresión.',
    ])}
    {caja("El resultado",
          "Seis componentes explicaron el <strong>76%</strong> de la varianza de las medidas de "
          "comportamiento. El circuito completo: comportamiento crudo &rarr; dimensiones "
          "interpretables &rarr; efectos sobre lo que la gente percibe.", C, ancho="88%")}
"""))

if __name__ == "__main__":
    from interactivos import CSS_INTERACTIVOS
    escribir("preview_bloque5.html", SLIDES, "Clase 10 — Bloque 5 (preview)",
            extra_css=CSS_INTERACTIVOS)

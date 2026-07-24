"""Clase 10 - BLOQUE 3: "Leer el biplot" (slides 21 a 26)."""

from comun import *
from interactivos import widget_biplot

B = 3
C = COLOR_BLOQUE[B]
SLIDES = []

SLIDES.append(portada_bloque(21, B, "Leer el resultado: el biplot",
                             "Observaciones y variables, en un mismo gráfico."))

SLIDES.append(slide(22, B, "El biplot: scores y loadings a la vez", f"""
    {widget_biplot(C, id_="biplot1")}
    {nota(f'Los <strong>puntos</strong> son estudiantes (scores, coloreados por desenlace — '
         f'clickeá la referencia para aislar un grupo) y las <strong>flechas</strong> son '
         f'variables (loadings). Pasá el mouse por el gráfico para ver los controles de '
         f'<strong>zoom</strong> y explorar la zona densa cerca del origen. Las dos primeras '
         f'componentes resumen el {alert("71,5%", B)} de la variabilidad de las ocho variables.')}
""", contenido_clase="centrado"))

SLIDES.append(slide(23, B, "PC1 resultó un eje de riesgo académico", f"""
    {caja("El hallazgo",
          "PCA <strong>nunca vio</strong> la etiqueta de deserción. Aun así, la primera componente "
          "separa a quienes abandonan de quienes se gradúan.", C, ancho="82%")}
    {bullets([
        'Score medio en PC1: <strong>+0,96</strong> entre quienes se gradúan, <strong>&minus;1,43</strong> '
        'entre quienes desertan.',
        f'PC1 sola explica el {alert("54,2%", B)} de la variabilidad de las ocho variables.',
        'Las variables de <strong>materias</strong> son las que definen ese eje; la nota de admisión '
        'casi no participa.',
    ])}
    {nota('Es el mismo tipo de lectura con la que el libro interpreta que la PC1 de '
         '<code>USArrests</code> mide criminalidad general.')}
"""))

SLIDES.append(slide(24, B, "Cómo se leen las flechas: dirección", f"""
    {bullets([
        'La <strong>dirección</strong> de una flecha dice qué mezcla de PC1 y PC2 representa a esa variable.',
        'Flecha casi <strong>horizontal</strong>: la variable carga sobre la primera componente. '
        'Casi <strong>vertical</strong>: sobre la segunda.',
        f'Es lo que permite ponerle {alert("nombre sustantivo", B)} a cada eje.',
    ])}
    {caja("En nuestro biplot",
          "Las seis variables de cursada apuntan hacia la <strong>derecha</strong>, con pesos del "
          "mismo signo y magnitud parecida: por eso el eje horizontal se lee como <strong>rendimiento "
          "académico</strong>. La edad de ingreso y la nota de admisión viven sobre el eje vertical.",
          C, ancho="82%")}
"""))

SLIDES.append(slide(25, B, "Ángulo y longitud: lo que agregan las flechas", f"""
    <div class="columnas">
      {caja("Ángulo entre flechas",
            "Aproxima la <strong>correlación</strong> entre las variables. Misma dirección: muy "
            "correlacionadas. Perpendiculares: sin correlación. Opuestas: correlación negativa.", C)}
      {caja("Longitud de la flecha",
            "Indica qué tan bien <strong>representada</strong> queda esa variable en el plano. "
            "Larga: el plano la captura bien. Corta: vive en las componentes que no estamos mirando.", C)}
    </div>
    {bullets([
        'Las flechas de <strong>inscriptas 1S y 2S</strong> son casi paralelas, y su correlación real '
        'es alta: el gráfico no miente.',
        f'La <strong>nota de admisión</strong> tiene la flecha más corta: sobre ella el biplot '
        f'{alert("no autoriza ninguna lectura", B)}.',
    ])}
"""))

SLIDES.append(slide(26, B, "Nombrar las componentes: un caso de consumo", f"""
    {caja("Lácteos locales (Apulia, Italia, 2022)",
          "Un experimento de elección online con <strong>543 encuestados</strong> sobre productos "
          "lácteos locales: calidad, sustentabilidad y disponibilidad.", C, ancho="82%")}
    {bullets([
        'Aplicaron PCA a las respuestas y quedaron <strong>cuatro componentes</strong>, que nombraron '
        'según qué ítems cargaban fuerte en cada una: sensibilidad a la calidad, "lo local es mejor", '
        '"lo local es sustentable" y demanda de mayor disponibilidad.',
        'Después relacionaron esas dimensiones con variables <strong>sociodemográficas</strong>.',
    ])}
    {nota(f'El flujo típico en Ciencias del Comportamiento: cuestionario con muchos ítems &rarr; PCA '
         f'&rarr; {alert("nombrar", B)} cada componente &rarr; relacionarla con otras variables.')}
"""))

if __name__ == "__main__":
    from interactivos import CSS_INTERACTIVOS
    from _plotly_inline import PLOTLY_JS
    escribir("preview_bloque3.html", SLIDES, "Clase 10 — Bloque 3 (preview)",
            extra_css=CSS_INTERACTIVOS, extra_js=PLOTLY_JS)

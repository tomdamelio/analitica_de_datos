"""Clase 10 - CIERRE (slides 48 a 50)."""

from comun import *

SLIDES = []

SLIDES.append(slide_notebook(48, None, "La práctica",
    f'Aplicar PCA <strong>+ clustering</strong> sobre el dataset de rotación de personal que ya '
    f'conocen, para descubrir {alert("perfiles latentes", None)} de empleados.'))

SLIDES.append(slide(49, None, "Los perfiles son hipótesis, no verdades",
    figura(PERFILES_B64, "Perfiles de clustering",
          f'Clusters sobre los primeros scores, y su tasa de rotación. El clustering '
          f'<strong>no es robusto</strong>: cambia con la estandarización, con cuántas componentes '
          f'se retienen y con $k$. Conviene repetirlo con distintas opciones y quedarse con lo que '
          f'{alert("persiste", None)}.'),
    contenido_clase="centrado-img"))

# Ultima slide de TODA la clase: sin logo arriba a la derecha, a pedido explicito.
SLIDES.append(slide(50, None, "Ya podés...", f"""
    {bullets([
        'Explicar por qué muchas variables correlacionadas se resumen en pocas dimensiones.',
        'Interpretar <strong>loadings</strong> y <strong>scores</strong>, y leer un <strong>biplot</strong> '
        'con sus tres criterios.',
        'Decidir cuándo <strong>estandarizar</strong> y cuántas componentes <strong>retener</strong>.',
        'Reconocer qué aportan y qué no los métodos no lineales, y qué asume PCA.',
    ])}
    {caja("El hallazgo de hoy, en una frase",
          f'Sin haber visto nunca la etiqueta de deserción, la <strong>primera componente</strong> de '
          f'ocho variables académicas resultó ser un {alert("eje de riesgo", None)} que separa a '
          f'quienes abandonan de quienes se gradúan.', NAVY, ancho="90%")}
    {nota('<strong>Lo que viene:</strong> representar textos en pocas dimensiones, con '
         '<em>embeddings</em> (Clases 11 y 12).')}
""", con_logo=False))

if __name__ == "__main__":
    escribir("preview_cierre.html", SLIDES, "Clase 10 — Cierre (preview)")

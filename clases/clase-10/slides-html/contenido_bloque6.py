"""Clase 10 - BLOQUE 6: "Supuestos y límites" (slides 44 a 47)."""

from comun import *

B = 6
C = COLOR_BLOQUE[B]
SLIDES = []

SLIDES.append(portada_bloque(44, B, "Supuestos y límites",
                             "Qué asume PCA, y cuándo conviene desconfiar."))

SLIDES.append(slide(45, B, "Qué asume PCA", f"""
    {bullets([
        'PCA se apoya en la matriz de <strong>covarianzas o correlaciones</strong> (de Pearson).',
        'Eso trae tres supuestos implícitos sobre las variables:'
        '<ul class="bullets-caja" style="margin-top:.4em">'
        '<li>que son <strong>continuas</strong>,</li>'
        '<li>que las relaciones entre ellas son <strong>lineales</strong>,</li>'
        f'<li>que las distancias entre valores consecutivos son {alert("equiespaciadas", B)}.</li>'
        '</ul>',
        'El tercero es el que más tensiona en Ciencias del Comportamiento: en una escala de '
        'acuerdo, ¿la distancia entre "en desacuerdo" y "neutral" es la misma que entre '
        '"neutral" y "de acuerdo"?',
    ])}
"""))

SLIDES.append(slide(46, B, "Escalas Likert: cuasi-continuas en la práctica", f"""
    {caja("La práctica estándar en psicometría",
          "Con escalas de <strong>5 o más puntos</strong> (idealmente 7) y una distribución no muy "
          "asimétrica, se aplica PCA directamente, tratando la variable ordinal como si fuera "
          "continua.", C, ancho="88%")}
    {bullets([
        'El sesgo que introduce suele ser <strong>chico y manejable</strong>.',
        'Así se analiza la enorme mayoría de los cuestionarios de personalidad, actitudes y clima laboral.',
        'Es exactamente lo que hicieron los estudios de Big Five que vimos al principio.',
    ])}
    {nota("Conviene igual <strong>declarar</strong> la decisión al reportar: es un supuesto que se "
         "asume, no un detalle técnico invisible.")}
"""))

SLIDES.append(slide(47, B, "Qué conviene evitar", f"""
    {caja("El límite claro",
          "Aplicar PCA con correlaciones de Pearson a variables <strong>nominales</strong>, es decir, "
          "sin ningún orden: tipo de contrato, carrera, provincia.", C, ancho="88%")}
    {bullets([
        f'Si no hay orden, {alert("no hay nada que preservar", B)}: los números que codifican las '
        f'categorías son etiquetas arbitrarias, y las correlaciones que se calculan sobre ellas no '
        f'significan nada.',
        'El chequeo previo más útil sigue siendo el más simple: <strong>mirar la matriz de '
        'correlaciones</strong>. Si es casi diagonal, no hay redundancia que explotar y PCA no va '
        'a ayudar.',
    ])}
"""))

if __name__ == "__main__":
    escribir("preview_bloque6.html", SLIDES, "Clase 10 — Bloque 6 (preview)")

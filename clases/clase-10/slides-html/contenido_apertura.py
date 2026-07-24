"""Clase 10 - APERTURA (slides 1 a 3): portada, pregunta guia, roadmap."""

from comun import *

SLIDES = []

# --- 1. Portada (sin logo arriba a la derecha: lleva el logo grande propio) --
SLIDES.append(f"""
<section class="slide" data-numero="1">
  <main class="contenido portada">
    <img class="logo-grande" src="{LOGO_COLOR_B64}" alt="UdeSA">
    <div class="caja-titulo-portada">
      <p class="tp-clase">Clase 10:</p>
      <p class="tp-nombre">Reducción de dimensionalidad (PCA)</p>
      <p class="tp-subtitulo">Analítica de Datos</p>
    </div>
    <p class="autor">Maestría en Ciencias del Comportamiento</p>
    <p class="fecha">Primavera 2026</p>
  </main>
</section>""")

# --- 2. Pregunta guia --------------------------------------------------------
SLIDES.append(slide(2, None, None, f"""
    <div class="pregunta-bloque">
      <p class="linea-grande">Medimos <strong>ocho cosas</strong> de cada estudiante.</p>
      <p class="linea-grande">¿Se pueden resumir en {alert("una sola", None)}?</p>
    </div>
    <hr class="divisor-fino">
    <div class="explicacion-bloque">
      <p class="linea-chica">Datos reales de <strong>4.424 estudiantes</strong> de educación superior: notas,
        materias inscriptas y aprobadas en dos semestres, nota de admisión y edad de ingreso.</p>
      <p class="linea-chica">Vamos a ver que la respuesta es <strong>sí</strong>, y que ese único número
        termina diciendo quién abandona.</p>
    </div>
""", contenido_clase="centrado"))

# --- 3. Roadmap --------------------------------------------------------------
SLIDES.append(slide(3, None, "De qué vamos a hablar hoy", f"""
    {caja("Objetivo",
          "Entender el <strong>análisis de componentes principales (PCA)</strong>: qué hace, "
          "cómo se lee, cuánta información conserva y dónde conviene usarlo en Ciencias del "
          "Comportamiento.", NAVY, ancho="78%")}
    {numerada([
        ("Por qué reducir.", "Muchas variables correlacionadas esconden pocas dimensiones."),
        ("Qué es una componente.", "De la intuición en 2D al caso de $p$ variables."),
        ("Leer el resultado.", "El biplot y cómo se interpretan sus flechas."),
        ("Cuánta información conservamos.", "Reconstrucción, varianza explicada y scree plot."),
        ("Decisiones y alcance.", "Estandarizar, métodos no lineales y casos aplicados."),
        ("Supuestos y límites.", "Qué asume PCA y cuándo no corresponde."),
    ])}
    {colab_linea()}
"""))

if __name__ == "__main__":
    escribir("preview_apertura.html", SLIDES, "Clase 10 — Apertura (preview)")

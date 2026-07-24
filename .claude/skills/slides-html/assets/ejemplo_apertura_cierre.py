"""
EJEMPLO de apertura (portada + intro) y cierre de un deck. Copiar este patron a
`contenido_apertura.py` y `contenido_cierre.py`. Correrlo solo con:

    python ejemplo_apertura_cierre.py

IMPORTANTE — la portada (slide 1) NO se arma con `slide()`: la primera slide de un deck
suele tener un tratamiento visual propio (logo grande a color, caja de titulo solida en el
color institucional) que no encaja en el esqueleto generico de header+main+footer que usan
todas las demas slides. Se arma el HTML de esa UNA slide a mano. El resto de la apertura
(pregunta guia, roadmap) SI usa `slide()` normalmente, con `bloque=None` — eso hace que
tome el color NAVY institucional en vez del color de un bloque tematico (no le pertenece a
ningun bloque en particular, es apertura).
"""

from comun import *

SLIDES = []

# --- 1. Portada: hecha a mano, no con slide() -----------------------------------------
SLIDES.append(f"""
<section class="slide" data-numero="1">
  <main class="contenido portada">
    <img class="logo-grande" src="{LOGO_COLOR_B64}" alt="logo">
    <div class="caja-titulo-portada">
      <p class="tp-clase">Titulo de la serie/curso:</p>
      <p class="tp-nombre">Titulo especifico de esta charla/clase</p>
      <p class="tp-subtitulo">Nombre del curso o contexto</p>
    </div>
    <p class="autor">Autor / equipo / institucion</p>
    <p class="fecha">Fecha o edicion</p>
  </main>
</section>""")

# --- 2. Pregunta guia / gancho inicial (usa slide(), bloque=None -> color NAVY) --------
SLIDES.append(slide(2, None, None, f"""
    <div class="pregunta-bloque">
      <p class="linea-grande">La pregunta o el gancho que enmarca toda la charla.</p>
      <p class="linea-grande">¿Y si {alert("esto", None)} fuera posible?</p>
    </div>
    <hr class="divisor-fino">
    <div class="explicacion-bloque">
      <p class="linea-chica">Contexto breve: de donde vienen los datos/el problema, y por que importa.</p>
      <p class="linea-chica">Una linea que adelanta hacia donde va la respuesta.</p>
    </div>
""", contenido_clase="centrado"))

# --- 3. Roadmap (agenda) ----------------------------------------------------------------
SLIDES.append(slide(3, None, "De qué vamos a hablar hoy", f"""
    {caja("Objetivo",
          "Una o dos oraciones que resumen la meta de toda la charla/clase.", NAVY, ancho="78%")}
    {numerada([
        ("Primer bloque.", "Una linea de que trata."),
        ("Segundo bloque.", "Idem."),
        ("Tercer bloque.", "Idem."),
    ])}
    {colab_linea()}
"""))


# ============================ CIERRE (en un proyecto real, otro archivo) ==================

# --- recap: que se llevan (usa slide() normal, bloque=None -> NAVY) --------------------
SLIDES.append(slide(48, None, "Ya podés...", f"""
    {bullets([
        'Primer logro concreto que el publico se lleva.',
        'Segundo logro.',
        'Tercer logro.',
    ])}
    {caja("El mensaje central, en una frase",
          f'La conclusion mas importante de toda la charla, {alert("resaltada", None)} en el '
          f'punto clave.', NAVY, ancho="90%")}
    {nota('<strong>Lo que viene:</strong> un adelanto de la proxima charla/clase, si aplica.')}
"""))

# --- ULTIMA slide de TODO el deck: con_logo=False si se quiere un cierre "limpio", sin
# ni siquiera el logo chico — es una preferencia de diseño (bookend simetrico con la
# portada, que tampoco lleva el logo chico), no una regla obligatoria. Ajustar a gusto.
SLIDES.append(slide(49, None, "Gracias", f"""
    {bullets(['Contacto, links, o lo que corresponda cerrar.'])}
""", con_logo=False))


if __name__ == "__main__":
    escribir("preview_apertura_cierre.html", SLIDES, "Preview — apertura y cierre")

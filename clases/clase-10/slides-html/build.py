"""
Generador del deck HTML/CSS "beanim-friendly" para las slides ESTATICAS de la
Clase 10 (PCA). Replica exactamente el diseno ya aprobado en `slides-beanim/`
(colores por bloque, titulo en negrita, pie de pagina gris con circulitos,
escudo arriba a la derecha) pero SIN pasar por Manim: HTML + CSS + KaTeX.

Por que existe este archivo (aparte de slides-beanim/):
- Una slide de puro texto no necesita compilar LaTeX -> SVG -> video de Manim
  para mostrar un fade-in: HTML/CSS lo hace instantaneo y sin los bugs que
  pisamos en el pipeline de Manim (limite de ruta de Windows, condicion de
  carrera de manim-slides al revertir video).
- El "marco" (logo, titulo, pie) es el MISMO HTML/CSS pase lo que pase en el
  contenido: si mas adelante una slide de este deck pasa a ser interactiva,
  se le agrega un <video> de Manim (solo el contenido, sin marco) adentro del
  mismo marco HTML — nunca hay dos motores dibujando el mismo elemento.

Uso::

    python build.py

Escribe `preview_bloque1.html` al lado de este archivo.
"""

import json
from pathlib import Path
from _assets_b64 import LOGO_B64, COLAB_B64, CORRELACIONES_B64, LOGO_COLOR_B64
from _katex_inline import KATEX_CSS, KATEX_JS, KATEX_AUTORENDER_JS

AQUI = Path(__file__).resolve().parent

# ---------------------------------------------------------------- paleta ----
# Identica a slides-beanim/udesa.py
NAVY = "#00529B"
AZUL = "#3182BD"
NARANJA = "#E6550D"
VERDE = "#31A354"
VIOLETA = "#756BB1"
ROJO = "#CB181D"
MARRON = "#8C6D31"
GRIS = "#636363"
GRIS_CLARO = "#969696"
TINTA = "#122535"

COLOR_BLOQUE = {1: AZUL, 2: NARANJA, 3: VERDE, 4: VIOLETA, 5: ROJO, 6: MARRON}
COLAB_URL = ("https://colab.research.google.com/github/tomdamelio/analitica_de_datos"
             "/blob/main/clases/clase-10/notebooks/clase10_python.ipynb")

# Mismo mapa que SECCIONES en udesa.py (limites reales de slides/clase10.tex)
SECCIONES = [
    {"inicio": 1, "fin": 3, "nombre": None},
    {"inicio": 4, "fin": 9, "nombre": "Por qué reducir"},
    {"inicio": 10, "fin": 20, "nombre": "Qué es una componente"},
    {"inicio": 21, "fin": 26, "nombre": "Leer el biplot"},
    {"inicio": 27, "fin": 35, "nombre": "Cuánta información"},
    {"inicio": 36, "fin": 43, "nombre": "Decisiones y alcance"},
    {"inicio": 44, "fin": 47, "nombre": "Supuestos y límites"},
    {"inicio": 48, "fin": 50, "nombre": "Cierre"},
]


# =============================================================== helpers ====
def _color_bloque(bloque):
    return COLOR_BLOQUE.get(bloque, NAVY)


def slide_abre(numero, bloque=None, titulo=None, con_logo=True):
    """Header comun a toda slide: <section> + titulo + logo. Se cierra aparte."""
    color = _color_bloque(bloque)
    titulo_html = f'<h1 class="titulo" style="color:{color}">{titulo}</h1>' if titulo else ""
    logo_html = f'<img class="logo" src="{LOGO_B64}" alt="UdeSA">' if con_logo else ""
    pie_html = f'<div class="pie" data-numero="{numero}"></div>' if bloque is not None or numero > 3 else ""
    return f"""
<section class="slide" data-bloque="{bloque or ''}" data-numero="{numero}">
  <header class="chrome-top">{titulo_html}{logo_html}</header>
  <main class="contenido">"""


CIERRA_SLIDE = "</main>{pie}</section>"


def slide_cierra(numero):
    pie = f'<footer class="pie" data-numero="{numero}"></footer>' if numero > 3 else ""
    return f"</main>{pie}</section>"


def caja(titulo, cuerpo, color, ancho="62%"):
    return (f'<div class="caja" style="border-color:{color};max-width:{ancho}">'
           f'<div class="caja-titulo" style="color:{color}">{titulo}</div>'
           f'<div class="caja-cuerpo">{cuerpo}</div></div>')


def bullets(items):
    lis = "".join(f"<li>{it}</li>" for it in items)
    return f'<ul class="bullets">{lis}</ul>'


def nota(texto):
    return f'<p class="nota">{texto}</p>'


def alert(texto, bloque):
    return f'<span class="alert" style="color:{_color_bloque(bloque)}">{texto}</span>'


# =============================================================== slides =====
slides = []

# --- 1. Portada -------------------------------------------------------------
# Replica el titlepage real (ver clase-02/slides/clase02.pdf, pagina 1): logo a
# color grande arriba, caja NAVY solida con sombra y texto blanco, autor/fecha
# abajo en negro. Sin logo arriba a la derecha (esta slide no lo lleva).
slides.append(f"""
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

# --- 2. Pregunta guia -------------------------------------------------------
slides.append(f"""
<section class="slide" data-numero="2">
  <header class="chrome-top"><img class="logo" src="{LOGO_B64}" alt="UdeSA"></header>
  <main class="contenido centrado">
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
  </main>
</section>""")

# --- 3. Roadmap --------------------------------------------------------------
puntos_roadmap = [
    ("Por qué reducir.", "Muchas variables correlacionadas esconden pocas dimensiones."),
    ("Qué es una componente.", "De la intuición en 2D al caso de $p$ variables."),
    ("Leer el resultado.", "El biplot y cómo se interpretan sus flechas."),
    ("Cuánta información conservamos.", "Reconstrucción, varianza explicada y scree plot."),
    ("Decisiones y alcance.", "Estandarizar, métodos no lineales y casos aplicados."),
    ("Supuestos y límites.", "Qué asume PCA y cuándo no corresponde."),
]
lis_roadmap = "".join(
    f'<li><strong>{lead}</strong> {resto}</li>' for lead, resto in puntos_roadmap)
slides.append(f"""
<section class="slide" data-numero="3">
  <header class="chrome-top"><h1 class="titulo" style="color:{NAVY}">De qué vamos a hablar hoy</h1>
    <img class="logo" src="{LOGO_B64}" alt="UdeSA"></header>
  <main class="contenido">
    {caja("Objetivo", "Entender el <strong>análisis de componentes principales (PCA)</strong>: qué hace, cómo se lee, cuánta información conserva y dónde conviene usarlo en Ciencias del Comportamiento.", NAVY, ancho="78%")}
    <ol class="numerada">{lis_roadmap}</ol>
    <p class="colab-linea">Para la práctica vamos a
      <a class="colab-link" href="{COLAB_URL}" target="_blank" rel="noopener">
        <img class="colab-icono" src="{COLAB_B64}" alt="Colab"><strong>Colab</strong></a>.</p>
  </main>
</section>""")

# --- 4. Bloque1 portada ------------------------------------------------------
slides.append(f"""
<section class="slide" data-bloque="1" data-numero="4">
  <header class="chrome-top"><img class="logo" src="{LOGO_B64}" alt="UdeSA"></header>
  <main class="contenido centrado">
    <p class="bloque-etiqueta" style="color:{AZUL}">BLOQUE 1 DE 6</p>
    <p class="bloque-nombre">Por qué reducir</p>
    <p class="bloque-bajada">Cuando hay demasiadas variables para mirarlas.</p>
  </main>
  <footer class="pie" data-numero="4"></footer>
</section>""")

# --- 5. No supervisado --------------------------------------------------------
slides.append(f"""
<section class="slide" data-bloque="1" data-numero="5">
  <header class="chrome-top"><h1 class="titulo" style="color:{AZUL}">Aprendizaje no supervisado: no hay qué predecir</h1>
    <img class="logo" src="{LOGO_B64}" alt="UdeSA"></header>
  <main class="contenido">
    {bullets([
        f'Hasta ahora tuvimos siempre una variable respuesta $Y$. Acá <strong>no la hay</strong>: solo un conjunto de features $X_1,\\dots,X_p$.',
        f'El objetivo cambia: ya no es predecir, es {alert("descubrir estructura", 1)} en los datos.',
        'Por eso el análisis no supervisado casi siempre es parte de un <strong>análisis exploratorio</strong>.',
        'Y por eso mismo es más <strong>subjetivo</strong>: no hay una respuesta correcta contra la cual validar, ni test set que nos diga si acertamos.',
    ])}
    {nota("ISLP, Sección 12.1.")}
  </main>
  <footer class="pie" data-numero="5"></footer>
</section>""")

# --- 6. Agrupar clientes -------------------------------------------------------
slides.append(f"""
<section class="slide" data-bloque="1" data-numero="6">
  <header class="chrome-top"><h1 class="titulo" style="color:{AZUL}">Agrupar clientes que nadie etiquetó</h1>
    <img class="logo" src="{LOGO_B64}" alt="UdeSA"></header>
  <main class="contenido">
    {caja("Un caso cotidiano", "Un sitio de compras online quiere recomendarle a cada persona lo que le interesa. Agrupa a sus clientes según su <strong>historial de navegación y compra</strong>, sin que nadie haya dicho de antemano a qué grupo pertenece cada uno.", AZUL, ancho="82%")}
    {bullets([
        'Nadie definió los grupos: <strong>emergen de los datos</strong>.',
        'Un buscador hace lo mismo con historiales de clics para decidir qué resultados mostrar.',
        'PCA ataca una versión de ese problema: cuando hay <strong>muchas variables correlacionadas</strong>, resumirlas en unas pocas que conserven casi toda la variabilidad.',
    ])}
  </main>
  <footer class="pie" data-numero="6"></footer>
</section>""")

# --- 7. Correlaciones (imagen) --------------------------------------------------
slides.append(f"""
<section class="slide" data-bloque="1" data-numero="7">
  <header class="chrome-top"><h1 class="titulo" style="color:{AZUL}">Varias variables dicen casi lo mismo</h1>
    <img class="logo" src="{LOGO_B64}" alt="UdeSA"></header>
  <main class="contenido centrado-img">
    <img class="figura" src="{CORRELACIONES_B64}" alt="Correlaciones">
    {nota(f'Correlaciones del bloque académico. Las materias <strong>aprobadas en 1er y 2do semestre</strong> correlacionan <strong>0,90</strong>: quien aprueba mucho en un semestre aprueba mucho en el otro. Hay {alert("redundancia", 1)} para explotar.')}
  </main>
  <footer class="pie" data-numero="7"></footer>
</section>""")

# --- 8. 28 graficos ------------------------------------------------------------
slides.append(f"""
<section class="slide" data-bloque="1" data-numero="8">
  <header class="chrome-top"><h1 class="titulo" style="color:{AZUL}">Con 8 variables ya hay 28 gráficos posibles</h1>
    <img class="logo" src="{LOGO_B64}" alt="UdeSA"></header>
  <main class="contenido">
    {bullets([
        'Para mirar las relaciones de a pares hacen falta $p(p-1)/2$ diagramas de dispersión.',
        f'Con nuestras <strong>8 variables</strong> son <strong>28</strong> gráficos. Con las <strong>24</strong> columnas numéricas del dataset, {alert("276", 1)}.',
        'Ninguno muestra la foto completa: cada uno contiene solo una fracción de la información.',
    ])}
    {caja("La pregunta que abre PCA", "¿Existe una representación de <strong>pocas dimensiones</strong> que capture la mayor parte posible de la variabilidad de los datos?", AZUL, ancho="82%")}
  </main>
  <footer class="pie" data-numero="8"></footer>
</section>""")

# --- 9. Cinco factores -----------------------------------------------------------
slides.append(f"""
<section class="slide" data-bloque="1" data-numero="9">
  <header class="chrome-top"><h1 class="titulo" style="color:{AZUL}">De 4.500 adjetivos a cinco factores</h1>
    <img class="logo" src="{LOGO_B64}" alt="UdeSA"></header>
  <main class="contenido">
    {bullets([
        'En 1936, Allport y Odbert listaron <strong>4.500 términos</strong> que describen diferencias de personalidad.',
        f'Con análisis factorial (el pariente cercano de PCA), esos términos se redujeron primero a 16 y finalmente a {alert("cinco", 1)}: el modelo <strong>Big Five</strong> (OCEAN).',
        'De Raad y Barelds (2008) aplicaron PCA a <strong>2.365 ítems</strong> del léxico holandés y recuperaron el Big Five más tres factores adicionales.',
    ])}
    {caja("El principio, en una línea", "Con $p$ enorme, unas pocas <strong>dimensiones compuestas</strong> pueden resumir una variedad inmensa. Es exactamente lo que vamos a hacer hoy, en menor escala.", AZUL, ancho="82%")}
  </main>
  <footer class="pie" data-numero="9"></footer>
</section>""")

SLIDES_HTML = "\n".join(slides)

# =============================================================== CSS ========
CSS = f"""
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; height:100%; background:#2a2a2a;
             font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
body {{ display:flex; align-items:center; justify-content:center; }}

#deck {{ position:relative; width:96vw; max-width:1600px; aspect-ratio:16/9;
        background:white; box-shadow:0 8px 40px rgba(0,0,0,.5); overflow:hidden; }}

/* padding generoso: margen de seguridad para que, si el proyector del aula
   recorta un poco los bordes, no se pierda nada importante. */
.slide {{ position:absolute; inset:0; display:none; flex-direction:column;
         padding: 4.6% 4.8%; font-size:1.55vw; color:{TINTA}; }}
.slide.activa {{ display:flex; }}

.chrome-top {{ display:flex; align-items:center; justify-content:space-between;
              min-height:2.6em; }}
.titulo {{ font-size:1.7em; font-weight:700; margin:0; line-height:1.15; }}
/* margin-left:auto (no solo justify-content en el padre) para que el logo
   quede SIEMPRE pegado a la derecha, incluso cuando es el unico hijo del
   header (la portada de bloque no tiene <h1 class="titulo">, y sin esto
   flexbox lo manda a la izquierda por ser el unico item). */
.logo {{ height:2.6em; opacity:.55; margin-left:auto; }}

.contenido {{ flex:1; display:flex; flex-direction:column; justify-content:flex-start;
             gap:.7em; margin-top:1.35em; overflow:hidden; }}
.contenido.centrado {{ justify-content:center; align-items:center; text-align:center; gap:.9em; }}
.contenido.centrado-img {{ align-items:center; justify-content:center; text-align:center; }}

.pregunta-bloque {{ display:flex; flex-direction:column; gap:.5em; }}
.divisor-fino {{ width:38%; border:none; border-top:1.5px solid {GRIS_CLARO}; margin:1em 0; opacity:.6; }}
.explicacion-bloque {{ display:flex; flex-direction:column; gap:.55em; align-items:center; }}

.bullets {{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:.55em; }}
.bullets li {{ position:relative; padding-left:1.1em; font-size:1.05em; line-height:1.35; }}
.bullets li::before {{ content:"•"; position:absolute; left:0; color:{TINTA}; }}

.numerada {{ margin:0; padding-left:1.4em; display:flex; flex-direction:column; gap:.4em; }}
.numerada li {{ font-size:.92em; line-height:1.3; }}

.alert {{ font-weight:400; }}

.caja {{ border:2px solid; border-radius:14px; padding:.7em 1em; background:rgba(0,0,0,.02); }}
.caja-titulo {{ font-weight:700; font-size:1.05em; margin-bottom:.3em; }}
.caja-cuerpo {{ font-size:.95em; line-height:1.35; color:{TINTA}; }}

.nota {{ font-size:.72em; color:{GRIS}; line-height:1.3; margin:.4em 0 0; max-width:92%; }}

.figura {{ max-width:78%; max-height:62%; object-fit:contain; }}

.colab-icono {{ height:1.1em; vertical-align:middle; margin-right:.35em; }}
.colab-linea {{ font-size:.85em; color:{GRIS}; text-align:center; margin-top:auto; }}
.colab-link {{ color:{NAVY}; text-decoration:none; border-bottom:1.5px solid currentColor; }}
.colab-link:hover {{ opacity:.75; }}

/* portada: replica clase-02/slides/clase02.pdf pagina 1 — caja NAVY solida,
   texto blanco, sombra, esquinas redondeadas; autor/fecha afuera, en negro. */
.portada {{ align-items:center; justify-content:center; text-align:center; gap:.5em; }}
.logo-grande {{ height:8.4%; margin-bottom:.4em; }}
.caja-titulo-portada {{ background:{NAVY}; color:white; border-radius:16px;
    box-shadow:0 .35em .55em rgba(0,0,0,.35); padding:.9em 1.6em; max-width:74%; }}
.tp-clase {{ font-size:1.35em; margin:0; }}
.tp-nombre {{ font-size:1.35em; font-weight:700; margin:.15em 0 0; line-height:1.25; }}
.tp-subtitulo {{ font-size:1em; margin:.5em 0 0; opacity:.92; }}
.autor {{ font-size:.92em; font-weight:700; margin:.7em 0 0; color:{TINTA}; }}
.fecha {{ font-size:.8em; color:{GRIS}; margin:.15em 0 0; }}

.linea-grande {{ font-size:1.3em; margin:0; }}
.linea-chica {{ font-size:.82em; color:{GRIS}; max-width:78%; margin:.2em 0 0; line-height:1.35; }}

/* bloque portada: sin la linea separadora (se saco a pedido), titulo grande */
.bloque-etiqueta {{ font-size:.95em; font-weight:700; letter-spacing:.03em; margin:0 0 .5em; }}
.bloque-nombre {{ font-size:2.7em; font-weight:700; margin:0; color:{TINTA}; }}
.bloque-bajada {{ font-size:1.05em; color:{GRIS}; margin:.45em 0 0; }}

/* pie de pagina: identico a udesa.py _fila_circulos, CENTRADO en la slide.
   Tipografia explicita (no heredar nada de KaTeX ni de otro lado) para que
   se vea igual de "sans regular" que en la version Beamer. */
.pie {{ display:flex; gap:1.6em; justify-content:center; align-items:flex-start;
       margin-top:auto; padding-top:.6em;
       font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; }}
.pie .seccion {{ display:flex; flex-direction:column; gap:.3em; align-items:flex-start; }}
.pie .nombre-seccion {{ font-size:.48em; font-weight:400; color:{GRIS_CLARO};
    white-space:nowrap; letter-spacing:.01em; }}
.pie .seccion.actual .nombre-seccion {{ color:{GRIS}; font-weight:700; }}
.pie .circulos {{ display:flex; gap:.35em; }}
.pie .circulo {{ width:.42em; height:.42em; border-radius:50%; border:1.4px solid {GRIS_CLARO}; }}
.pie .seccion.actual .circulo {{ border-color:{GRIS}; }}
.pie .seccion.actual .circulo.pasado {{ background:{GRIS}; }}
"""

# =============================================================== JS =========
JS = f"""
const SECCIONES = {json.dumps(SECCIONES, ensure_ascii=False)};

function armarPie(el) {{
    const numero = parseInt(el.dataset.numero, 10);
    const actual = SECCIONES.find(s => s.nombre && numero >= s.inicio && numero <= s.fin);
    if (!actual) {{ el.style.display = 'none'; return; }}
    el.innerHTML = '';
    for (const s of SECCIONES) {{
        if (!s.nombre) continue;
        const esActual = s === actual;
        const div = document.createElement('div');
        div.className = 'seccion' + (esActual ? ' actual' : '');
        const nombre = document.createElement('div');
        nombre.className = 'nombre-seccion';
        nombre.textContent = s.nombre;
        const circulos = document.createElement('div');
        circulos.className = 'circulos';
        for (let i = s.inicio; i <= s.fin; i++) {{
            const c = document.createElement('div');
            c.className = 'circulo' + (esActual && i <= numero ? ' pasado' : '');
            circulos.appendChild(c);
        }}
        div.appendChild(nombre);
        div.appendChild(circulos);
        el.appendChild(div);
    }}
}}

document.querySelectorAll('.pie').forEach(armarPie);

const slides = document.querySelectorAll('.slide');
let idx = 0;
function mostrar(i) {{
    idx = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => s.classList.toggle('activa', k === idx));
    if (window.renderMathInElement) {{
        renderMathInElement(slides[idx], {{delimiters: [{{left:'$', right:'$', display:false}}]}});
    }}
}}
const params = new URLSearchParams(location.search);
mostrar(parseInt(params.get('slide') || '0', 10));
window.addEventListener('keydown', (e) => {{
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) {{ mostrar(idx + 1); e.preventDefault(); }}
    if (['ArrowLeft', 'PageUp'].includes(e.key)) {{ mostrar(idx - 1); e.preventDefault(); }}
}});
"""

# KaTeX 100% embebido (CSS con fuentes en base64 + JS inline): el deck no
# depende de internet ni de un CDN externo para renderizar las formulas.
HTML = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Clase 10 — Apertura + Bloque 1 (HTML estático, preview)</title>
<style>{KATEX_CSS}</style>
<style>{CSS}</style>
</head>
<body>
<div id="deck">
{SLIDES_HTML}
</div>
<script>{KATEX_JS}</script>
<script>{KATEX_AUTORENDER_JS}</script>
<script>{JS}</script>
</body>
</html>
"""

(AQUI / "preview_bloque1.html").write_text(HTML, encoding="utf-8")
print("escrito:", AQUI / "preview_bloque1.html", "-", len(HTML), "caracteres")

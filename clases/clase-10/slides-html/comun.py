"""
Piezas compartidas por TODOS los bloques del deck HTML estatico (Clase 10).

Cada bloque vive en su propio `contenido_bloqueN.py` (o `contenido_apertura.py`,
`contenido_cierre.py`) y expone una lista `SLIDES` de fragmentos HTML, armados
con los helpers de aca (`slide`, `caja`, `bullets`, etc.). `build_todo.py` los
junta todos en un solo archivo final; cada modulo de contenido tambien puede
correrse solo (con `python contenido_bloqueN.py`) para revisar un bloque a la vez.
"""

import json
from pathlib import Path
from _assets_b64 import (LOGO_B64, COLAB_B64, LOGO_COLOR_B64, CORRELACIONES_B64,
                         BIPLOT_B64, RECONSTRUCCION_B64, SCREE_B64, ESCALADO_B64,
                         NO_LINEALES_B64, PERFILES_B64, PCA2D_B64, ERRORES_TIRA_B64,
                         TRES_D_B64, SCORE_TERMINO_B64)
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

# Mapa global de secciones (identico a SECCIONES en slides-beanim/udesa.py):
# el pie de pagina necesita conocer los limites de TODA la clase, no solo del
# bloque que se este armando en este momento.
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


def slide(numero, bloque, titulo, contenido_html, con_logo=True, extra_clase="",
         contenido_clase=""):
    """
    Arma una <section class="slide"> completa: header (titulo + logo) + main
    (contenido) + pie. `con_logo=False` solo en la slide 1 y en la ultima de
    toda la clase (slide 50), a pedido explicito. `contenido_clase` agrega
    clases al <main> (p.ej. "centrado" o "centrado-img").
    """
    color = _color_bloque(bloque)
    titulo_html = f'<h1 class="titulo" style="color:{color}">{titulo}</h1>' if titulo else ""
    logo_html = f'<img class="logo" src="{LOGO_B64}" alt="UdeSA">' if con_logo else ""
    pie_html = f'<footer class="pie" data-numero="{numero}"></footer>' if numero > 3 else ""
    bloque_attr = bloque if bloque is not None else ""
    clase = f"slide {extra_clase}".strip()
    clase_main = f"contenido {contenido_clase}".strip()
    return f"""
<section class="{clase}" data-bloque="{bloque_attr}" data-numero="{numero}">
  <header class="chrome-top">{titulo_html}{logo_html}</header>
  <main class="{clase_main}">{contenido_html}</main>
  {pie_html}
</section>"""


def portada_bloque(numero, bloque, nombre_bloque, bajada, total=6, con_logo=True):
    """La slide divisoria de bloque (\"BLOQUE N DE 6\" + nombre + bajada)."""
    color = _color_bloque(bloque)
    contenido = (f'<p class="bloque-etiqueta" style="color:{color}">BLOQUE {bloque} DE {total}</p>'
                f'<p class="bloque-nombre">{nombre_bloque}</p>'
                f'<p class="bloque-bajada">{bajada}</p>')
    return slide(numero, bloque, None, contenido, con_logo=con_logo, contenido_clase="centrado")


def caja(titulo, cuerpo, color, ancho="62%"):
    return (f'<div class="caja" style="border-color:{color};max-width:{ancho}">'
           f'<div class="caja-titulo" style="color:{color}">{titulo}</div>'
           f'<div class="caja-cuerpo">{cuerpo}</div></div>')


def bullets(items):
    lis = "".join(f"<li>{it}</li>" for it in items)
    return f'<ul class="bullets">{lis}</ul>'


def numerada(items):
    """items: lista de (lead_bold, resto)."""
    lis = "".join(f'<li><strong>{lead}</strong> {resto}</li>' for lead, resto in items)
    return f'<ol class="numerada">{lis}</ol>'


def nota(texto):
    return f'<p class="nota">{texto}</p>'


def alert(texto, bloque):
    return f'<span class="alert" style="color:{_color_bloque(bloque)}">{texto}</span>'


def ecuacion(formula):
    """Ecuacion centrada, en modo display (usa los delimitadores $$...$$)."""
    return f'<p class="ecuacion">$${formula}$$</p>'


def tabla(encabezados, filas):
    """
    `encabezados`: lista de strings (primera celda vacia si la 1er columna de
    `filas` ya trae su propio titulo). `filas`: lista de (titulo_fila, [valores]).
    """
    th = "".join(f"<th>{h}</th>" for h in encabezados)
    trs = ""
    for titulo_fila, valores in filas:
        tds = "".join(f"<td>{v}</td>" for v in valores)
        trs += f"<tr><th>{titulo_fila}</th>{tds}</tr>"
    return f'<table class="tabla-pve"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


def figura(src_b64, alt, pie_texto=""):
    pie_html = nota(pie_texto) if pie_texto else ""
    return f'<img class="figura" src="{src_b64}" alt="{alt}">{pie_html}'


def colab_linea(texto_previo="Para la práctica vamos a"):
    return (f'<p class="colab-linea">{texto_previo}'
           f'<a class="colab-link" href="{COLAB_URL}" target="_blank" rel="noopener">'
           f'<img class="colab-icono" src="{COLAB_B64}" alt="Colab"><strong>Colab</strong></a>.</p>')


def slide_notebook(numero, bloque, encabezado, texto1="", texto2=""):
    """
    La slide "a la notebook" (bumper con el logo grande de Colab). El logo Y
    el encabezado son un link real a `COLAB_URL` (antes faltaba: se veia el
    icono pero no llevaba a ningun lado).
    """
    partes = [f'<a class="nb-link" href="{COLAB_URL}" target="_blank" rel="noopener">'
             f'<img class="colab-grande" src="{COLAB_B64}" alt="Colab">'
             f'<p class="nb-encabezado">{encabezado}</p></a>']
    if texto1:
        partes.append(f'<p class="nb-texto1">{texto1}</p>')
    if texto2:
        partes.append(f'<p class="nb-texto2">{texto2}</p>')
    contenido = "".join(partes)
    return slide(numero, bloque, None, contenido, contenido_clase="centrado")


# =============================================================== CSS ========
def armar_css():
    return f"""
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; height:100%; background:#2a2a2a;
             font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
body {{ display:flex; align-items:center; justify-content:center; }}

/* ancho limitado tanto por el viewport horizontal como por el vertical: si la
   ventana es mas "corta" que ancha (barra de direcciones, pestanas, etc. le
   restan alto pero no ancho), un deck dimensionado solo con vw se pasa de
   la altura disponible y queda cortado arriba/abajo. */
#deck {{ position:relative; width:min(96vw, calc(96vh * 16 / 9)); max-width:1600px;
        aspect-ratio:16/9; background:white; box-shadow:0 8px 40px rgba(0,0,0,.5);
        overflow:hidden; }}

/* padding generoso: margen de seguridad para que, si el proyector del aula
   recorta un poco los bordes, no se pierda nada importante. */
/* mismo min(vw, vh*16/9) que #deck, escalado por 1.55/96: si no, el font-size
   queda atado al viewport y se desproporciona apenas el alto (no el ancho) es
   quien termina limitando el tamano del deck. */
.slide {{ position:absolute; inset:0; display:none; flex-direction:column;
         padding: 4.6% 4.8%; font-size:min(1.55vw, calc(1.55vh * 16 / 9), 24.8px); color:{TINTA}; }}
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
/* para slides con mucho contenido (ecuacion + varios bullets + caja): achica
   todo proporcionalmente en vez de dejar que se corte contra el pie. */
.contenido.densa {{ font-size:.8em; gap:.45em; }}

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
.bullets-caja {{ list-style:none; margin:.3em 0 0; padding:0; display:flex;
    flex-direction:column; gap:.4em; }}
.bullets-caja li {{ position:relative; padding-left:1.1em; }}
.bullets-caja li::before {{ content:"•"; position:absolute; left:0; }}

.nota {{ font-size:.72em; color:{GRIS}; line-height:1.3; margin:.4em 0 0; max-width:92%; }}

.figura {{ max-width:78%; max-height:62%; object-fit:contain; display:block; margin:0 auto; }}

.colab-icono {{ height:1.1em; vertical-align:middle; margin-right:.35em; }}
.colab-linea {{ font-size:.85em; color:{GRIS}; text-align:center; margin-top:auto; }}
.colab-link {{ color:{NAVY}; text-decoration:none; border-bottom:1.5px solid currentColor; }}
.colab-link:hover {{ opacity:.75; }}

.nb-link {{ display:flex; flex-direction:column; align-items:center; text-decoration:none;
    cursor:pointer; }}
.nb-link:hover .nb-encabezado {{ opacity:.75; }}
.colab-grande {{ height:14%; margin-bottom:.2em; }}
.nb-encabezado {{ font-size:1.7em; font-weight:700; margin:0; color:{TINTA}; }}
.nb-texto1 {{ font-size:1em; margin:.3em 0 0; max-width:70%; color:{TINTA}; }}
.nb-texto2 {{ font-size:.82em; margin:.2em 0 0; max-width:70%; color:{GRIS}; }}

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

/* bloque portada: sin linea separadora, titulo grande */
.bloque-etiqueta {{ font-size:.95em; font-weight:700; letter-spacing:.03em; margin:0 0 .5em; }}
.bloque-nombre {{ font-size:2.7em; font-weight:700; margin:0; color:{TINTA}; }}
.bloque-bajada {{ font-size:1.05em; color:{GRIS}; margin:.45em 0 0; }}

.ecuacion {{ text-align:center; font-size:1.15em; margin:.4em 0; }}
.parrafo-libre {{ font-size:1.05em; line-height:1.4; margin:0; }}

/* tabla PVE (bloque 4) */
.tabla-pve {{ border-collapse:collapse; margin:.3em auto 0; font-size:.85em; }}
.tabla-pve th, .tabla-pve td {{ padding:.35em .7em; text-align:center; }}
.tabla-pve thead th {{ background:{VIOLETA}; color:white; font-weight:700; }}
.tabla-pve tbody th {{ text-align:left; font-weight:700; color:{TINTA}; }}
.tabla-pve tbody tr:nth-child(odd) {{ background:rgba(0,0,0,.03); }}

/* columnas (bloque 3, angulo/longitud) */
.columnas {{ display:flex; gap:1.2em; align-items:flex-start; justify-content:center; }}
.columnas .caja {{ flex:1; max-width:48% !important; }}

/* pie de pagina: identico a udesa.py _fila_circulos, CENTRADO en la slide.
   Tipografia explicita para que se vea igual de "sans regular" que en Beamer. */
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
def armar_js():
    return f"""
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
        renderMathInElement(slides[idx], {{delimiters: [
            {{left:'$$', right:'$$', display:true}},
            {{left:'$', right:'$', display:false}}]}});
    }}
}}
const params = new URLSearchParams(location.search);
mostrar(parseInt(params.get('slide') || '0', 10));
// Widgets como el de "formula por pasos" (ver widget_formula_pasos en
// interactivos.py) se registran en window.__fpAvanzar/__fpRetroceder para
// consumir la flecha ANTES de que cambie de diapositiva: mientras a ese
// widget le queden terminos por revelar (o por esconder, yendo para atras),
// la flecha revela/esconde un termino en vez de avanzar de slide.
window.addEventListener('keydown', (e) => {{
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) {{
        const consumido = (window.__fpAvanzar || []).some(fn => fn(slides[idx]));
        if (!consumido) mostrar(idx + 1);
        e.preventDefault();
    }}
    if (['ArrowLeft', 'PageUp'].includes(e.key)) {{
        const consumido = (window.__fpRetroceder || []).some(fn => fn(slides[idx]));
        if (!consumido) mostrar(idx - 1);
        e.preventDefault();
    }}
}});
"""


def armar_html(titulo_pagina, slides_html_list, extra_css="", extra_js=""):
    """
    Junta CSS + JS + KaTeX embebido + las slides en un solo HTML autonomo.

    `extra_js` (p.ej. Plotly) se inyecta ANTES que las slides, no al final: los
    widgets de las propias slides (su `<script>` inline) corren en cuanto el
    parser los encuentra, asi que cualquier libreria de la que dependan tiene
    que estar cargada antes del `<div id="deck">`, no despues.
    """
    slides_html = "\n".join(slides_html_list)
    css = armar_css()
    js = armar_js()
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{titulo_pagina}</title>
<style>{KATEX_CSS}</style>
<style>{css}</style>
<style>{extra_css}</style>
</head>
<body>
<script>{extra_js}</script>
<div id="deck">
{slides_html}
</div>
<script>{KATEX_JS}</script>
<script>{KATEX_AUTORENDER_JS}</script>
<script>{js}</script>
</body>
</html>
"""


def escribir(nombre_archivo, slides_html_list, titulo_pagina=None, extra_css="", extra_js=""):
    titulo_pagina = titulo_pagina or f"Clase 10 — {nombre_archivo}"
    html = armar_html(titulo_pagina, slides_html_list, extra_css=extra_css, extra_js=extra_js)
    destino = AQUI / nombre_archivo
    destino.write_text(html, encoding="utf-8")
    print("escrito:", destino, "-", len(html), "caracteres,", len(slides_html_list), "slides")
    return destino

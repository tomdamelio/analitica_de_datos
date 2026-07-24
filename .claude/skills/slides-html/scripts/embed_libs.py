"""
Descarga KaTeX y/o Plotly y los empaqueta como modulos Python embebibles offline
(`_katex_inline.py`, `_plotly_inline.py`) — para que el deck final sea un solo HTML sin
dependencias de CDN (funciona sin internet, robusto para el dia de la clase/charla).

USO (Claude: pedir permiso explicito al usuario ANTES de correr esto — decir el archivo, la
URL fuente y el tamano aproximado, y esperar confirmacion. Bajar SOLO lo que el deck realmente
necesita: KaTeX si hay formulas, Plotly si hay widgets 3D o tipo biplot; ninguno de los dos si
el deck es solo texto/figuras estaticas):

    python embed_libs.py katex    <carpeta_del_deck>
    python embed_libs.py plotly   <carpeta_del_deck>

Plotly tiene varios bundles; este script baja el partial "gl3d" (~1.7MB) que alcanza para
scatter3d/surface/scatter 2D con anotaciones (los widgets de este starter kit) sin pagar el
peso del bundle completo (~4.5MB, con chart types que no se usan aca).
"""

import sys
import urllib.request
from pathlib import Path

KATEX_VERSION = "0.16.9"
KATEX_CSS_URL = f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/katex.min.css"
KATEX_JS_URL = f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/katex.min.js"
KATEX_AUTORENDER_URL = (f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/contrib/"
                        "auto-render.min.js")
# El CSS de KaTeX referencia fuentes .woff2 por URL relativa; para embeber TODO offline
# (sin pedir esas fuentes a un CDN en el momento de abrir el deck) hace falta bajarlas e
# inlinearlas como data: URIs dentro del CSS. Ver `_inline_katex_fonts()` mas abajo.
KATEX_FONTS_BASE = f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/fonts/"

PLOTLY_VERSION = "2.35.2"
PLOTLY_JS_URL = f"https://cdn.plot.ly/plotly-gl3d-{PLOTLY_VERSION}.min.js"


def _bajar(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def _inline_katex_fonts(css_text):
    import base64
    import re

    def reemplazar(m):
        nombre_fuente = m.group(1)
        datos = _bajar(KATEX_FONTS_BASE + nombre_fuente)
        b64 = base64.b64encode(datos).decode()
        return f'url(data:font/woff2;base64,{b64})'

    return re.sub(r'url\(fonts/([^)]+\.woff2)\)', reemplazar, css_text)


def embeber_katex(carpeta):
    print(f"Bajando KaTeX {KATEX_VERSION} (CSS + JS + auto-render + fuentes woff2)...")
    css = _bajar(KATEX_CSS_URL).decode("utf-8")
    css = _inline_katex_fonts(css)
    js = _bajar(KATEX_JS_URL).decode("utf-8")
    autorender = _bajar(KATEX_AUTORENDER_URL).decode("utf-8")

    destino = Path(carpeta) / "_katex_inline.py"
    destino.write_text(
        "KATEX_CSS = " + repr(css) + "\n\n"
        "KATEX_JS = " + repr(js) + "\n\n"
        "KATEX_AUTORENDER_JS = " + repr(autorender) + "\n",
        encoding="utf-8",
    )
    print("escrito:", destino, "-", destino.stat().st_size, "bytes")


def embeber_plotly(carpeta):
    print(f"Bajando Plotly (bundle gl3d) {PLOTLY_VERSION} (~1.7MB)...")
    js = _bajar(PLOTLY_JS_URL).decode("utf-8")

    destino = Path(carpeta) / "_plotly_inline.py"
    destino.write_text("PLOTLY_JS = " + repr(js) + "\n", encoding="utf-8")
    print("escrito:", destino, "-", destino.stat().st_size, "bytes")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("katex", "plotly"):
        print(__doc__)
        sys.exit(1)
    libreria, carpeta = sys.argv[1], sys.argv[2]
    if libreria == "katex":
        embeber_katex(carpeta)
    else:
        embeber_plotly(carpeta)

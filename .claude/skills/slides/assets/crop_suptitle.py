"""Recorta una franja superior de una figura (para sacar el suptitle de matplotlib,
conservando los titulos de cada subplot). Guarda una copia presentacion-especifica.

Uso (con el interprete de Python del proyecto activo; venv/conda/micromamba o python a secas):
    python crop_suptitle.py <input.png> <top_px> <output.png>

Flujo recomendado (en el skill):
  1. Read(input.png) para estimar a que altura (top_px) empiezan los subplots/paneles.
  2. Correr este script.
  3. Read(output.png) para VERIFICAR: suptitle fuera + nada de los subplots cortado.
     Si quedo mal, ajustar top_px y volver a correr.

Variante "partir 2 paneles": en vez de recortar arriba, recortar por ancho:
    im.crop((0, 0, x_corte, h))  -> panel izquierdo ; (x_corte, 0, w, h) -> derecho
"""
import sys
from PIL import Image

if len(sys.argv) != 4:
    sys.exit("uso: python crop_suptitle.py <input.png> <top_px> <output.png>")
inp, top, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
im = Image.open(inp)
w, h = im.size
im.crop((0, top, w, h)).save(out)
print(f"ok: {out}  ({w}x{h}, top removido={top})")

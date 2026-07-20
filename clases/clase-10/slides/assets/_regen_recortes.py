# -*- coding: utf-8 -*-
"""Assets presentacion-especificos de la Clase 10.

Genera, a partir de las figuras originales de clases/clase-10/assets/figures/:
  1. las versiones *_notitle.png, sin el titulo embebido (el titular lo lleva la slide);
  2. gif_errores_tira.png, tres fotogramas del gif de la rotacion puestos en secuencia.

Las figuras originales NO se tocan. Correr desde clases/clase-10/slides/:
    python assets/_regen_recortes.py
"""
from pathlib import Path
from PIL import Image, ImageSequence, ImageChops
import numpy as np

SLIDES = Path(__file__).resolve().parent.parent
FIGS = SLIDES.parent / "assets" / "figures"

# Figuras cuyo titulo de matplotlib/plotly hay que recortar
CON_TITULO = ["clase10_correlaciones", "clase10_pca2d", "clase10_biplot",
              "clase10_score_termino", "clase10_reconstruccion", "clase10_no_lineales", "clase10_3d"]

# Recortes que necesitan un corte manual, porque el titulo queda pegado al plot
# y no hay una fila blanca que separe las dos bandas (bbox_inches="tight").
MANUAL = {"clase10_correlaciones": 32, "clase10_score_termino": 46}


def filas_con_tinta(im):
    a = np.array(im.convert("RGB"))
    return (a.min(axis=2) < 240).any(axis=1)


def recortar(nombre):
    im = Image.open(FIGS / (nombre + ".png")).convert("RGB")
    tinta = filas_con_tinta(im)
    i = int(np.argmax(tinta))                      # primera fila con contenido: arranca el titulo
    if nombre in MANUAL:
        corte = i + MANUAL[nombre]
    else:
        j = i
        while j < len(tinta) and tinta[j]:
            j += 1                                  # fin de la banda del titulo
        corte = max(0, j - 2)
    salida = SLIDES / (nombre + "_notitle.png")
    im.crop((0, corte, im.width, im.height)).save(salida)
    return salida


def recortar_margenes(ruta):
    im = Image.open(ruta).convert("RGB")
    fondo = Image.new("RGB", im.size, (255, 255, 255))
    bbox = ImageChops.difference(im, fondo).convert("L").point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox:
        im.crop(bbox).save(ruta)


def tira_del_gif(n_frames=3, ancho_util=0.72):
    g = Image.open(FIGS / "PCA-errors.gif")
    frames = [f.convert("RGB") for f in ImageSequence.Iterator(g)]
    idx = [int(k * len(frames) / n_frames) for k in range(n_frames)]
    sel = [frames[k].crop((0, 0, int(frames[k].width * ancho_util), frames[k].height)) for k in idx]
    w, h = sel[0].size
    tira = Image.new("RGB", (w * len(sel), h), "white")
    for n, f in enumerate(sel):
        tira.paste(f, (n * w, 0))
    tira.save(SLIDES / "gif_errores_tira.png")


if __name__ == "__main__":
    for nombre in CON_TITULO:
        salida = recortar(nombre)
        print("recortado ->", salida.name)
    recortar_margenes(SLIDES / "clase10_3d_notitle.png")   # plotly exporta con mucho margen blanco
    tira_del_gif()
    print("tira del gif -> gif_errores_tira.png")

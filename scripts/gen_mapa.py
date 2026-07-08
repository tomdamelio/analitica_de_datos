#!/usr/bin/env python
"""Genera _mapa_programa.qmd (el mapa del curso de la pagina Programa) enlazando
automaticamente cada clase que YA tiene pagina propia en clases/clase-NN/index.qmd.

Se corre en el workflow de publicacion ANTES de `quarto render` (Quarto expande los
includes al armar el proyecto, antes de cualquier pre-render), asi que en produccion
el mapa siempre refleja las clases existentes. Al agregar una clase en fases
siguientes, correr `python scripts/gen_mapa.py` para actualizar la copia versionada
(o dejar que el CI lo regenere en el deploy).
"""
import os
from pathlib import Path

ROOT = Path(os.environ.get("QUARTO_PROJECT_DIR", "."))

# Estructura del recorrido: (clase-css, encabezado, [(num_clase, titulo_corto), ...])
ETAPAS = [
    ("hito", "Inicio",
        [(1, "Presentación e introducción al machine learning")]),
    ("eje-1", "Eje I: Procesamiento y visualización de datos",
        [(2, "Análisis exploratorio y procesamiento"),
         (3, "Visualización y reportes reproducibles")]),
    ("eje-2", "Eje II: Aprendizaje supervisado",
        [(4, "Introducción al aprendizaje supervisado"),
         (5, "Regresión lineal y regularización"),
         (6, "Clasificación"),
         (7, "Árboles de decisión y Random Forest"),
         (8, "Series temporales")]),
    ("eje-3", "Eje III: Aprendizaje no supervisado",
        [(9, "Clustering (K-means y jerárquico)"),
         (10, "Reducción de dimensionalidad (PCA)")]),
    ("eje-4", "Eje IV: Procesamiento de lenguaje natural (NLP)",
        [(11, "Embeddings, sentimiento y clasificación"),
         (12, "Aplicaciones avanzadas y RAG")]),
    ("hito", "Evaluación",
        [(13, "Examen final escrito"),
         (14, "Defensa del trabajo práctico integrador")]),
]

ARIA = ("Recorrido del semestre: la Clase 1 de introducción, luego los cuatro "
        "ejes de la materia con sus clases, y al final la evaluación en las "
        "clases 13 y 14.")


def clase_li(num, titulo):
    inner = f"<b>Clase {num}</b> {titulo}"
    if (ROOT / f"clases/clase-{num:02d}/index.qmd").exists():
        return f'<li><a href="clases/clase-{num:02d}/index.html">{inner}</a></li>'
    return f"<li>{inner}</li>"


def main():
    out = [f'<div class="mapa-curso" role="img" aria-label="{ARIA}">', ""]
    for i, (css, cab, clases) in enumerate(ETAPAS):
        out.append(f'<div class="mapa-etapa mapa-{css}">')
        out.append(f'<div class="mapa-cab">{cab}</div>')
        out.append('<ul class="mapa-clases">')
        out += [clase_li(n, t) for n, t in clases]
        out.append("</ul>")
        out.append("</div>")
        out.append("")
        if i < len(ETAPAS) - 1:
            out.append('<div class="mapa-flecha">&rarr;</div>')
            out.append("")
    out.append("</div>")

    dest = ROOT / "_mapa_programa.qmd"
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")
    con_pagina = [n for _, _, cs in ETAPAS for n, _ in cs
                  if (ROOT / f"clases/clase-{n:02d}/index.qmd").exists()]
    print(f"[gen_mapa] {dest.name} generado. Clases con link: {con_pagina}")


if __name__ == "__main__":
    main()

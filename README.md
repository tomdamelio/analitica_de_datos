# Analítica de Datos — UdeSA

Material de la materia **Analítica de Datos** (Maestría en Ciencias del Comportamiento,
Universidad de San Andrés, primavera 2026). Sitio estático hecho con
[Quarto](https://quarto.org), publicado en GitHub Pages; notebooks ejecutables en
Google Colab (Python y R).

> **Contrato del repo:** ver [`CONVENTIONS.md`](CONVENTIONS.md). Estructura, nombres,
> anatomía de páginas/notebooks, bilingüismo y copyright se definen ahí.

## Estructura

```
_quarto.yml            # config del sitio (nav, tema, freeze)
_variables.yml         # ÚNICO lugar con <owner>/<repo>/<branch> para badges Colab
index.qmd              # home
programa.qmd           # programa de la materia
bibliografia.qmd       # lecturas — SOLO enlaces (nunca PDFs)
theme/                 # tokens.yml (paleta) + udesa.scss (tema)
clases/clase-NN/       # una carpeta por clase: index.qmd + notebooks/ + assets/
data/                  # datasets chicos + README.md con fuente y licencia
context/               # PRIVADO (gitignoreado): programa fuente, refs, branding
.github/workflows/     # build + deploy a GitHub Pages
```

## Cómo buildear localmente

Requisitos: [Quarto](https://quarto.org/docs/download/) ≥ 1.9, Python 3.12 con
`requirements.txt`, y (solo para re-ejecutar las notebooks R) R ≥ 4.5 con los paquetes
de `DESCRIPTION` e `IRkernel::installspec()`.

```bash
pip install -r requirements.txt
quarto render          # build completo a _site/
quarto preview         # servidor local con live reload
```

Con `freeze: auto`, el render usa los outputs congelados: no hace falta R/Python para
re-renderizar páginas que no cambiaron. Las notebooks se ejecutan **en el momento de
autoría** (quedan con outputs guardados); Quarto no las re-ejecuta.

## Publicación

Push a `main` dispara `.github/workflows/publish.yml` (render + deploy a GitHub Pages
+ sincronización del espejo de notebooks). Configurar una sola vez:

1. **Settings → Pages → Source: GitHub Actions**. El repo es privado, pero el sitio
   publicado es público.
2. **Espejo público de notebooks** (necesario porque Colab no abre notebooks de repos
   privados; los badges apuntan al espejo):
   - Crear el repo **público** `tomdamelio/analitica-de-datos-notebooks` (vacío).
   - Crear un fine-grained PAT con permiso *Contents: Read and write* **solo** sobre
     ese repo, y guardarlo en este repo como secret `NOTEBOOKS_MIRROR_TOKEN`.
   - El job `mirror-notebooks` copia las `.ipynb` (misma ruta) en cada push. Nunca
     copia `data/` ni `context/`.

## Cambiar owner/repo/rama (badges de Colab)

Editar **solo** `_variables.yml` (`colab-root`, `site-url`) y re-renderizar. Las
notebooks `.ipynb` llevan la URL resuelta en su celda de encabezado: si cambia el valor,
actualizar también esos badges (buscar `colab.research.google.com/github/` en
`clases/*/notebooks/`).

## Regla de copyright

El sitio **solo enlaza** bibliografía; nunca hostea PDFs de libros. El material de
referencia del equipo vive en `context/` (gitignoreado, fuera del build).

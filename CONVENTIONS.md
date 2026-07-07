# CONVENTIONS.md — Contrato del repositorio

> **Leé este archivo ANTES de generar cualquier material.** Define la estructura, los
> nombres, la anatomía de las páginas y las notebooks, el manejo de figuras y las
> reglas de bilingüismo. Las fases 2 (slides) y 3 (todas las clases) **heredan** estas
> convenciones: si una clase no las respeta, está mal. El objetivo es que las 14 clases
> sean indistinguibles en estructura y calidad.

---

## 1. Stack técnico

- **Sitio:** [Quarto](https://quarto.org) → HTML estático en **GitHub Pages**.
- **Notebooks:** `.ipynb` estándar (Jupyter), ejecutables en **Google Colab**.
- **Lenguajes:** Python (principal) **y** R (par validado), una notebook por lenguaje.
- **Slides (fase 2):** Beamer/LaTeX vía el skill `/slides` → PDF.
- **Ejecución/validación:** en el momento de autoría (dentro de Claude Code). Quarto
  publica outputs **congelados** (`freeze`), no re-ejecuta en CI.

## 2. Estructura de directorios (canónica)

```
/
├── _quarto.yml                 # config del sitio (nav, tema, freeze)
├── index.qmd                   # home de la materia
├── programa.qmd                # programa final (desde context/programa/)
├── bibliografia.qmd            # lecturas: SOLO enlaces, sin PDFs
├── theme/
│   ├── udesa.scss              # tema Quarto derivado del branding UdeSA
│   └── tokens.yml              # paleta y tipografía (fuente única de verdad)
├── clases/
│   └── clase-NN/               # NN con cero a la izquierda: 01, 02, ... 14
│       ├── index.qmd           # página de la clase
│       ├── notebooks/
│       │   ├── claseNN_python.ipynb
│       │   └── claseNN_r.ipynb
│       ├── slides/             # (fase 2) claseNN.pdf + fuentes .tex
│       └── assets/
│           └── figures/        # .png emitidos por las notebooks (alimentan slides)
├── data/
│   ├── README.md               # fuente + licencia de cada dataset (OBLIGATORIO)
│   └── <dataset>.csv           # datasets chicos, licencia abierta, versionados
├── context/                    # GITIGNOREADO — no forma parte del sitio
│   ├── programa/               # programa final (fuente)
│   ├── refs/                   # PDFs de libros para referencia de autoría
│   ├── brand/                  # logo y paleta UdeSA (assets de branding)
│   └── decisiones_equipo.md
├── requirements.txt            # dependencias Python (versionadas)
├── renv.lock  (o DESCRIPTION)  # dependencias R
├── CONVENTIONS.md              # este archivo
├── README.md                   # cómo buildear/publicar el repo
└── .github/workflows/          # build + deploy del sitio
```

## 3. Convenciones de nombres

- Carpetas de clase: `clase-NN` (dos dígitos). Notebooks: `claseNN_python.ipynb`,
  `claseNN_r.ipynb`. Slides: `claseNN.pdf`.
- Figuras: `claseNN_<slug-descriptivo>.png` (ej. `clase02_distribucion_edad.png`).
  Snake_case, sin espacios, sin acentos en nombres de archivo.
- IDs de dataset en `data/`: nombre corto, estable, documentado en `data/README.md`.

## 4. Anatomía de la página de clase (`clases/clase-NN/index.qmd`)

Frontmatter YAML + secciones en este orden fijo:

1. **Título** de la clase (idéntico al del programa).
2. **Objetivo(s)** — copiado/adaptado del programa.
3. **Contenidos** — bullets del programa.
4. **Notebooks** — tabla o lista con, para cada lenguaje: link a la versión
   renderizada + **badge "Open in Colab"** (ver §6). Python primero, R segundo.
5. **Slides** — link al PDF (placeholder en fase 1; se completa en fase 2).
6. **Lecturas obligatorias** y **complementarias** — con enlace (nunca PDF hosteado).
   Distinguir claramente material en Python vs. referencia en R.

La página **embebe la notebook Python renderizada** (para leer en el sitio) y **enlaza**
la de R; ambas se abren en Colab desde los badges.

## 5. Anatomía de las notebooks

Cada notebook (Python y R) tiene la misma columna vertebral:

1. **Celda de encabezado (markdown):** título de la clase, lenguaje, badge "Open in
   Colab", objetivos, y una línea de "qué vas a poder hacer al terminar".
2. **Setup:** imports/librerías, fijar **semilla** (`SEED = 42` o equivalente), cargar
   el dataset **desde una URL raw estable** (para que funcione en Colab sin archivos
   locales), configurar estilo de figuras (§6).
3. **Secciones de contenido:** cada concepto = markdown explicativo (en español) +
   celda(s) de código ejecutadas, con su output visible.
4. **Ejercicios (estilo neuromatch):** ver §7.
5. **Cierre:** recap de lo hecho + "para seguir" (opcional).

Reglas:
- Todo el código **debe ejecutarse sin errores** y quedar ejecutado (outputs visibles).
- Comentarios y prosa **en español**.
- Nada de rutas locales absolutas; datos por URL raw o `data/` relativo compatible Colab.
- Nada de instalar dependencias pesadas sin necesidad; si hace falta `pip install`/
  `install.packages`, va en una celda de setup claramente marcada y condicionada a Colab.

## 6. Figuras (puente notebook → slides)

- Cada figura relevante se **guarda como `.png`** en `clases/clase-NN/assets/figures/`
  con nombre según §3, además de mostrarse inline.
- Resolución y estilo consistentes (ej. `dpi=150`, estilo sobrio con la paleta de
  `theme/tokens.yml`). Definir un pequeño helper de guardado reutilizable.
- Motivo: en la fase 2, el skill `/slides` (plot-céntrico) apunta su `\graphicspath`
  a esa carpeta y usa **las figuras reales de la clase**. Los números de las slides
  salen de outputs verdaderos, nunca inventados.
- Badge "Open in Colab" — formato de URL:
  `https://colab.research.google.com/github/<owner>/<repo>/blob/<branch>/clases/clase-NN/notebooks/claseNN_python.ipynb`
  (idem `_r`). Parametrizar `<owner>/<repo>/<branch>` en un solo lugar.

## 7. Ejercicios y marcado de soluciones (para el stripping futuro)

Por ahora las notebooks se entregan **con soluciones**. Para que la versión "estudiante"
(sin soluciones) se genere después de forma **mecánica**, cada ejercicio sigue este
patrón:

- **Celda markdown de consigna:** qué se pide, con la pista necesaria.
- **Celda de código de solución:** con el código completo y ejecutado, y
  - **tag de celda** `solution` (en `cell.metadata.tags`), y
  - en `cell.metadata` una clave **`scaffold`** con el string de la versión "con huecos"
    (mismo código pero con `# TODO:` y las líneas clave reemplazadas por `___` o
    `# completar`).

Así, un script posterior genera la notebook de estudiante reemplazando el `source` de
cada celda `solution` por su `scaffold`, sin tocar nada más. **No** usar celdas
colapsables inline ni soluciones en el mismo bloque de texto: la separación por tags es
lo que hace el proceso reversible.

## 8. Bilingüismo Python ↔ R (regla de paridad)

- Cada clase tiene **dos notebooks** que cubren **el mismo dataset, los mismos pasos,
  las mismas figuras y las mismas conclusiones**.
- No es traducción literal: se usa el idiomatismo de cada lenguaje (pandas/matplotlib/
  scikit-learn del lado Python; tidyverse/ggplot2/tidymodels o equivalentes del lado R).
- Ambas versiones deben producir resultados **equivalentes** (mismos números salvo
  diferencias numéricas menores; mismas figuras conceptualmente).
- Ambas se **ejecutan y validan** antes de dar la clase por terminada.
- Las figuras de ambas se guardan en `assets/figures/` con sufijo de lenguaje si difieren
  (`..._py.png` / `..._r.png`); si son conceptualmente idénticas, se usa la de Python
  como la que alimenta las slides.

## 9. Datos

- Solo datasets **chicos y de licencia abierta**, versionados en `data/`.
- `data/README.md` documenta, por dataset: nombre, fuente/URL, **licencia**, breve
  descripción, y en qué clases se usa.
- **Carga en Colab con repo privado:** como el repositorio es privado, su URL "raw" no es
  pública y no sirve para cargar datos en Colab. Las notebooks cargan el CSV desde una
  **fuente pública y estable** (URL oficial del dataset, el sitio publicado en GitHub Pages,
  o un repo/gist público de datos), y se versiona además una copia en `data/` para la
  autoría/render. Nunca servir públicamente un dataset cuya licencia no lo permita.
- **Dataset "espina":** por defecto se reutiliza **un mismo dataset a lo largo de las
  clases 2-7 y 9-10** (EDA, viz, supervisado, no supervisado) para dar continuidad.
  Solo se usan datasets dedicados donde el tema lo exige: **clase 8** (serie temporal)
  y **clases 11-12** (corpus de texto para NLP).

## 10. Bibliografía (regla de copyright)

- La página `bibliografia.qmd` y las páginas de clase **solo enlazan** a las fuentes.
- **Nunca** se hostea en el sitio un PDF de un libro con copyright.
- Recursos gratuitos y oficiales (ISLP, McKinney, Wilke, FPP3, r4ds, ESL) se enlazan a
  su sitio oficial. Recursos comerciales (Knaflic; Rokach & Maimon) se citan y se
  enlazan a la editorial/DOI, sin material reproducido.

## 11. Branding UdeSA

- Fuente única de verdad: `theme/tokens.yml` (paleta + tipografía) y `theme/udesa.scss`.
- Derivar del branding oficial en `context/brand/`. Si no está disponible, usar un
  **navy sobrio** como placeholder y **dejarlo señalado** para que la cátedra confirme.
- El tema del sitio y (en fase 2) las slides deben compartir la misma paleta.

## 12. Reproducibilidad y calidad

- Semillas fijas en todo código con aleatoriedad.
- `requirements.txt` (Python) y `renv.lock`/`DESCRIPTION` (R) con versiones.
- `freeze: auto` en Quarto para no depender del entorno de CI al publicar.
- Antes de cerrar una clase: render local del sitio OK + ambas notebooks ejecutadas OK.

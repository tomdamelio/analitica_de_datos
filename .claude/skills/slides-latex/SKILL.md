---
name: slides-latex
description: Arma una presentacion Beamer plot-centrica (theme SimpleDarkBlue + Helvetica + paleta tab20c) a partir de un TEXTO dado y de contexto distribuido en varios archivos (figuras, datos, notas), de forma COLABORATIVA y slide por slide. Genera PDF/LaTeX estatico (paginas fijas, sin interaccion) — para un deck HTML interactivo (widgets, animaciones, navegador) usar en cambio la skill `slides-html`. Generica/standalone, sirve en cualquier proyecto. Triggers: /slides-latex, "armar diapositivas en latex/beamer", "presentacion en beamer", "pasar este texto a slides en pdf".
---

# Skill: slides-latex

Construye, **junto con el usuario y slide por slide**, una presentacion Beamer LaTeX a partir de:
1. un **texto fuente** (el mensaje, las conclusiones o el contenido que se quiere presentar), y
2. **contexto distribuido** en mas de un lugar (figuras `.png`, tablas/CSV, notas, scripts) que el
   usuario senala o que hay que ir a buscar.

El usuario marca el ritmo: vos presentas/armas una slide y PARAS; el usuario pide ajustes; cuando dice
"siguiente", avanzas.

Filosofia: **predominan los PLOTS, no el texto.** Titulos = el mensaje/conclusion. Leyendas cortas
solo cuando aclaran. Numeros siempre fieles a la fuente (CSV/tabla/texto), nunca inventados.

> Esta es la version **generica**. Si el proyecto tiene una variante especializada (p.ej.
> `research-session-slides`, atada a un pipeline o a convenciones de carpetas propias), usar esa
> cuando aplique; esta sirve para cualquier texto+contexto.

> **Relacion con `slides-html`:** misma filosofia colaborativa slide-por-slide, pero esta produce
> LaTeX/Beamer -> PDF (paginas fijas, ideal para imprimir o proyectar sin depender de un navegador).
> Si el usuario quiere **interaccion real** (widgets, animaciones, algo que corra en un browser),
> usar `slides-html` en su lugar.

---

## Cuando se usa

- Cuando el usuario invoca `/slides-latex` o pide armar una presentacion/deck en LaTeX/Beamer/PDF a
  partir de un texto y/o de material disperso (figuras + datos + notas).
- **Un deck autocontenido** por presentacion.

## Inputs que hay que establecer al arrancar

Si no estan dados, preguntar (breve) o inferir del contexto:
1. **Texto/mensaje fuente:** que se quiere comunicar (el argumento, las conclusiones, el orden).
2. **Material disponible:** donde viven las figuras (`.png`/`.pdf`) y los datos (CSV/npz/tablas) que
   van a ir al deck; pueden estar en varias carpetas.
3. **Carpeta de salida** del deck (por defecto `slides/` o `presentation/` en el cwd, o la que el
   usuario indique).
4. **Idioma** del deck (el template viene en castellano; cambiable a ingles en el preambulo).
5. **Portada:** titulo, autor, fecha (y subtitulo/afiliacion si corresponde).

## Que produce y donde

- `<salida>/<nombre>.tex` + `.pdf` (compilado con pdflatex/MiKTeX o cualquier TeX con beamer).
- `<salida>/assets/` = imagenes presentacion-especificas (recortes de suptitle, paneles
  regenerados). **Nunca se pisan las figuras originales** de las que se parte.

---

## Setup (una vez por deck)

1. Crear la carpeta de salida (`<salida>/`).
2. Copiar a esa carpeta los **4 `.sty`** del theme (`<skill>/assets/theme/`) y el **template**
   (`<skill>/assets/template.tex`) renombrado al deck.
3. **Copiar las figuras a la MISMA carpeta del deck** y referenciarlas por nombre pelado (el template
   ya usa `\graphicspath{{./}}`). Es lo robusto contra el bug de kpathsea (ver gotchas). Los recortes/
   regenerados presentacion-especificos tambien van ahi (no se pisan las figuras originales de origen).
4. **Color primario:** `\definecolor{primary}{HTML}{...}` con el color institucional.
5. **Logo (opcional):** dejar `logo-color.png` y `logo-white.png` en la carpeta; si no hay, borrar los
   `\includegraphics` de las plantillas de portada y frametitle.
6. **Notebooks (cursos):** ajustar `<owner>/<repo>/<branch>` en las URLs de Colab; dejar `colab_logo.png`.
7. Rellenar la portada (titulo, subtitulo, autor, fecha) y los bloques (`\section` + `\bloque{color}`).

---

## Estructura narrativa del deck

1. **Portada** (`[plain]`, sin footer) — logo institucional arriba, titulo / autor / fecha.
2. **Pregunta / mensaje** — la idea de fondo, grande y centrada; opcional una figura o preview.
3. **De que vamos a hablar** — roadmap con los N bloques; en un curso, cerrar con el enlace a la practica.
4. **Por cada bloque:** `\section{...}` + `\bloque{color}` + un **divisor plano** (etiqueta de color +
   nombre del bloque) + sus **slides de contenido**. En cursos, cerrar el bloque con un **puntero a la
   notebook** (logo Colab clickeable) que marca la TAREA practica, distinta del contenido teorico.
5. **Cierre** (`\navytheme`) — recap ("ya podes...") + el hallazgo en una frase + lo que viene.

Los bloques mapean a las secciones del texto fuente (en un curso, a los ejes/temas). Cada bloque =
un `\section` (alimenta la navegacion de circulos) con su color secundario.

> **Contenido vs practica (cursos):** las slides cubren el contenido TEORICO completo; la practica va
> en las notebooks. En las slides, a lo sumo, un puntero "a la notebook"; eso es tarea, no contenido.

---

## Tematizacion por bloque (un color por seccion)

Cada bloque toma un **color secundario tab20c distinto** para su **barra de titulo** (separacion
mental fuerte). El primario institucional queda para apertura y cierre. Macros del template:
- `\bloque{tabBlue}` antes del grupo de slides de un bloque: pinta la barra de titulo, las vinetas
  y `\alert` con ese color.
- `\navytheme` para apertura y cierre (barra en el color primario institucional).

Asignacion sugerida: Bloque 1 = `tabBlue`, 2 = `tabOrange`, 3 = `tabGreen`, 4 = `tabPurple`.
Patron por bloque: `\section{Nombre}` + `\bloque{C}` + **divisor plano** (etiqueta de color + nombre
del bloque, sin barra) + los frames de contenido. El `\section` alimenta la navegacion (abajo);
`\AtBeginSection{}` vacio evita que genere una slide.

## Navegacion de progreso (circulos por slide, en el footer)

Un **circulo por slide**, agrupados por bloque (`\section`), en el footer (via `\useoutertheme
[subsection=false]{miniframes}` + `\insertnavigation`). Reglas ya calibradas en el template:
- Solo el bloque **actual** aparece en color (nombre + sus circulos, el activo relleno); los demas,
  **gris hueco** (`mini frame` base = gris; `in current subsection` = color del bloque via `structure`).
- El footer **recien aparece con el primer** `\section` (`\ifnum\insertsectionnumber>0`); la apertura
  queda limpia. Sin numero de pagina.
- La **portada** va con `\begin{frame}[plain]` para que no tenga footer.

## Identidad institucional (primario + logo)

- `\definecolor{primary}{HTML}{...}` = color institucional (portada, apertura, cierre).
- Logo (opcional): dos PNG en la carpeta del deck, `logo-color.png` (portada, fondo blanco) y
  `logo-white.png` (barra de titulo, fondo de color). El template los coloca en la portada (arriba,
  chico) y arriba a la derecha de cada slide de contenido. Si no hay logo, borrar esos `\includegraphics`.
- Para hacer un logo en blanco desde un SVG a color: editar los `fill=...` a `#FFFFFF` y renderizar a
  PNG transparente (p.ej. `msedge --headless --screenshot --default-background-color=00000000`).

## Enlaces a notebooks (logo Colab clickeable)

En un deck de curso, los logos de Colab enlazan a la notebook Python del tema en Colab:
`\href{https://colab.research.google.com/github/<owner>/<repo>/blob/<branch>/<ruta>/<nb>_python.ipynb}{\includegraphics{colab_logo.png}}`.
**El `\href` va inline** (no dentro de un `\newcommand`): hyperref re-catcodea los `_` de la URL solo
si los lee directo; via macro pre-tokenizada, los `_` rompen. Las slides "A la notebook" (logo Colab
centrado) marcan la **tarea practica**, distinta del contenido teorico.

## Codigo en las slides (listings)

Para clases con codigo, `\usepackage{listings}` con el estilo del template (keywords en el primario,
strings en verde, comentarios en gris, fondo gris claro). El frame debe ser `[fragile]`. Comentarios y
strings del codigo **sin acentos** (inputenc utf8 + listings se llevan mal con acentos dentro del bloque).

---

## Principios de diseno plot-centrico

- **Una idea por slide; el plot manda.** El espacio es para la figura, no para el texto.
- **Titulo = titular** (la conclusion en una linea), con lo mas importante en `\textbf{...}`; incluir
  el numero clave cuando ese ES el punto. Ej: "Con control fuerte, el efecto COLAPSA a azar".
- **Leyenda** `{\footnotesize ...}` debajo, <=2 lineas, en lenguaje simple, fiel a los numeros.
- **Dos figuras** -> `columns[t]` con **una leyenda bajo cada imagen** (no una leyenda combinada).
- **Sacar los suptitles de matplotlib** conservando los titulos de cada subplot (ver recorte abajo).
  Sin esos titulos internos, la slide queda limpia.
- Resaltar palabras con `\alert{...}` (toma el color de la seccion) o `\textbf{...}`.

---

## Manejo de imagenes (las tecnicas clave)

**Reglas de path:** referenciar `assets/<x>.png` para recortes/regenerados (la carpeta del `.tex` es
el cwd); las figuras originales via su path relativo (resuelto por `\graphicspath`).
`\includegraphics[width=\linewidth,height=0.82\textheight,keepaspectratio]{...}` para que entre sin
desbordar (mas alto si no hay leyenda, ~0.72 si es two-col).

1. **Recortar suptitle** (lo mas frecuente): `assets/crop_suptitle.py <in> <top_px> <out>`.
   Flujo: `Read(in)` para estimar `top_px` -> correr -> `Read(out)` para VERIFICAR que el suptitle
   se fue y nada de los subplots quedo cortado; ajustar `top_px` si hace falta.
   Guardar como `assets/<stem>_notitle.png`.
2. **Partir una figura de 2 paneles** (quedarse con uno): recortar por ancho con PIL
   (`im.crop((0,0,x_corte,h))` izq / `(x_corte,0,w,h)` der). Verificar el corte visualmente.
3. **Regenerar un panel** (relabelar ejes/titulos, cambiar idioma, quitar un subplot): leer el **dato
   cacheado** de origen (CSV/npz; nunca reprocesar el dato crudo si hay un derivado) y replicar el
   plot con matplotlib, cambiando lo necesario. Si existe el script original que genero la figura,
   mirarlo para copiar colores/estilo. Guardar el script en `assets/_regen_*.py`.
4. Si una figura **no tiene suptitle separable** (un solo panel cuyo unico titulo es el de la figura,
   o un scatter con solo labels de eje), **no recortar**: usar el original.

---

## El loop colaborativo

1. **Inventario:** leer el texto fuente (mensaje/numeros) y listar el material disponible
   (`Glob` de las figuras `**/figures/*.png` o donde esten; los CSV/tablas asociados). Si `Glob`
   falla (p.ej. rutas con espacios/OneDrive en Windows), usar `find ... -name "*.png"` por Bash.
2. **Outline:** proponer el arbol topico -> slides (con la figura de cada una) y confirmarlo.
3. **Esqueleto:** copiar theme+template, ajustar `\graphicspath`, rellenar portada + mensaje + recap
   + roadmap; **compilar y mostrar** (renderizar las paginas con `Read` del PDF).
4. **Slide por slide:** armar una -> compilar -> renderizar la pagina con `Read` -> PARAR y esperar
   al usuario -> aplicar sus ajustes -> recompilar -> re-renderizar. **El ritmo lo marca el usuario.**
5. Aplicar los pedidos por-slide (titulos, leyendas, recortes, borrar/reordenar slides) y **siempre
   verificar el render** despues de cada cambio.

---

## Compilar y verificar

- Compilar: `pdflatex -interaction=nonstopmode <deck>.tex`, **dos veces** (la navegacion de circulos
  cuenta los frames por seccion via `.aux`, igual que un footer "k/N": la 1ra pasada aun no los tiene).
  En Windows/TinyTeX el `pdflatex` suele estar en `~/AppData/Roaming/TinyTeX/bin/windows/`; en MiKTeX,
  en `~/AppData/Local/Programs/MiKTeX/...` (o `pdflatex` en PATH).
- Chequear `grep -iE "error|not found|Output written"` del log; `grep "Overfull \\vbox"` para overflow.
- **Verificar SIEMPRE renderizando** la(s) pagina(s) con `Read(<deck>.pdf, pages=N)` (o convertir a PNG
  con `pymupdf`: `d[i].get_pixmap(matrix=Matrix(2,2)).save(...)`). Ojo con el **indice**: pagina k =
  indice k-1. La capa de texto del PDF pierde ligaduras/acentos: confiar en el render visual.
- Acentos en castellano: escapes `\'a`, `\~n`, `?`...?` para `¿` (template en utf8); en codigo/tablas,
  `babel` con `es-noshorthands` para que las comillas `"` no se rompan.

### Gotchas ya aprendidos (no repetir)

- **Imagenes por nombre pelado en la carpeta del deck.** kpathsea (Windows) a veces no encuentra una
  figura en `subcarpeta/` o con cierto nombre. Dejar TODAS las imagenes junto al `.tex` y referenciarlas
  sin ruta. Si una "no aparece" pese a existir, renombrarla (p.ej. `fig_x.png`) y recompilar.
- **Titulos de UNA linea.** La barra de titulo lleva el logo a la derecha; un titulo largo se va a dos
  lineas y se encima con el logo. Mantener el titular <= ~55 caracteres.
- **Portada sin footer.** `\begin{frame}[plain]\titlepage\end{frame}`.
- **`\href` inline** para URLs con `_` (ver seccion de enlaces): nunca dentro de `\newcommand`.
- **Recortar el suptitle** de las figuras que traen su titulo, para que el titular lo lleve la slide
  (ver mas abajo); no duplicar titulo-de-figura y frametitle.

---

## Scripts Python (recorte/regeneracion)

- Usar el **interprete de Python del proyecto activo** (venv/conda/micromamba segun el repo). Si hay
  un env especifico, detectarlo o preguntar; si no, `python` a secas. Ejemplo:
  `python crop_suptitle.py <in> <top_px> <out>`.
- En `python -c` usar **una sola linea** (algunos wrappers rompen los multilinea) o escribir un `.py`
  y correrlo.
- Los recortes/regenerados son **assets presentacion-especificos**: van a `<salida>/assets/`, no se
  tocan las figuras originales ni los scripts de los que se parte.
- `rm -rf` suele estar bloqueado en algunos entornos: dejar los temporales y avisar.

---

## Pedidos por-slide tipicos (vocabulario del usuario)

- "cambiar el titulo a ..." / "poner X en negrita" -> editar el `\begin{frame}{...}` / `\textbf`.
- "sacar el titulo del plot (dejar los de los subplots)" -> recortar suptitle.
- "borrar la leyenda de abajo" -> quitar el `{\footnotesize ...}` (y subir el `height` de la imagen).
- "que cada figura tenga su slide" -> partir un two-col en dos frames de una figura.
- "eliminar el subplot de la derecha" -> partir la figura por ancho (quedarse con el izquierdo).
- "eliminar las diapositivas X a Y" -> borrar esos `\begin{frame}..\end{frame}` (confirmar viendo el
  PDF antes, porque es destructivo) y recompilar.
- "agrandar la figura sin pasar el margen" -> subir width/height y verificar que no desborde.

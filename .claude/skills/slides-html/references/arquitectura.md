# Arquitectura del deck HTML

## Por que separar chrome de contenido

El "chrome" (titulo, logo, pie de pagina con el progreso) tiene que verse **identico** este la slide
en cuestion hecha de texto estatico o de un widget interactivo — es lo que hace que el deck se sienta
como una sola cosa coherente y no un collage de dos herramientas distintas. Por eso `slide()` en
`comun.py` siempre arma el mismo esqueleto HTML (header + main + footer) y lo que cambia entre una
slide estatica y una interactiva es solo el contenido de `<main>`: texto/bullets en un caso, el
`<div>` + `<script>` de un widget en el otro. Nunca hay dos "motores de dibujo" compitiendo por el
mismo pixel de chrome.

## Estructura de archivos

```
mi-clase/
├── comun.py                # chrome + helpers de contenido (ver "helpers" abajo)
├── interactivos.py         # los widgets (ver references/widgets.md)
├── datos.py                # precomputa TODOS los numeros reales a un JSON, una sola vez
├── datos_clase.json        # (generado por datos.py) — fuente de verdad para texto Y widgets
├── contenido_apertura.py   # una lista SLIDES; corrible solo con `python contenido_apertura.py`
├── contenido_bloque1.py    # idem, un archivo por bloque tematico
├── contenido_bloque2.py
├── ...
├── contenido_cierre.py
├── build_todo.py           # concatena TODOS los contenido_*.SLIDES en el HTML final
├── _katex_inline.py        # generado una vez por scripts/embed_libs.py
├── _plotly_inline.py       # idem (solo si hay widgets Plotly)
└── _assets_b64.py          # imagenes propias del deck (logo, figuras estaticas) en base64
```

Cada `contenido_bloqueN.py` es independiente y **corrible solo** (`python contenido_bloqueN.py`
escribe un `preview_bloqueN.html` con nada mas que ese bloque) — esto es clave para iterar rapido:
no hace falta regenerar los 50 slides para revisar un cambio en 3. `build_todo.py` es el paso final,
se corre despues de cada tanda de cambios para tener el deck completo actualizado.

## El HTML final: orden de scripts (no negociable)

`armar_html()` en `comun.py` arma el documento en este orden exacto:

```
<head>
  <style>KATEX_CSS</style>
  <style>css del chrome</style>
  <style>extra_css (CSS de los widgets)</style>
</head>
<body>
  <script>extra_js (p.ej. Plotly)</script>   <!-- ANTES del deck -->
  <div id="deck">
    ...todas las slides, cada una con su <script> inline si es un widget...
  </div>
  <script>KATEX_JS</script>                   <!-- DESPUES de las slides -->
  <script>KATEX_AUTORENDER_JS</script>
  <script>js de navegacion (mostrar/ocultar slides, teclado)</script>
</body>
```

Por que este orden y no "todo arriba" o "todo abajo":
- **Plotly va ANTES del deck** porque los widgets de Plotly llaman a `Plotly.newPlot(...)`
  sincronicamente dentro de su propio `<script>` inline (que esta DENTRO de `<div id="deck">`,
  osea aparece despues en el documento) — si Plotly no cargo todavia, esa llamada tira
  `ReferenceError: Plotly is not defined`.
- **KaTeX va DESPUES del deck**, no antes, porque KaTeX es pesado (CSS con fuentes woff2 embebidas)
  y cargarlo antes demoraria el primer paint de las slides sin necesidad — el renderizado de formulas
  ($...$ en texto normal) lo hace `renderMathInElement()` reactivamente cada vez que se muestra una
  slide (ver mas abajo), asi que no hace falta que este disponible desde el arranque.
- **Consecuencia importante:** si un widget llama `katex.render()` directamente (no via el
  auto-render de `$...$`, sino armando su propia formula con `\htmlClass` para colorear terminos —
  ver `widget_formula_pasos` en `references/widgets.md`), ese `<script>` corre ANTES de que el
  `<script>` de KaTeX (mas abajo en el documento) haya cargado la libreria. **No usar `setTimeout(fn,
  0)` para esperar** — es una carrera: a veces el resto del documento tarda lo suficiente en
  parsearse como para que gane, a veces no (paso en un deck real: funcionaba en un archivo grande con
  Plotly de por medio, y fallaba en un archivo mas chico sin Plotly, exactamente por esto). La forma
  correcta, garantizada por el spec de HTML, es:
  ```js
  function renderFormula() { katex.render(...); }
  if (window.katex) { renderFormula(); }
  else { document.addEventListener("DOMContentLoaded", renderFormula); }
  ```
  `DOMContentLoaded` solo dispara despues de que TODOS los `<script>` sincronicos del documento —
  incluido el de KaTeX, mas abajo — ya corrieron.

## El motor de navegacion (JS, ~30 lineas)

```js
const slides = document.querySelectorAll('.slide');
let idx = 0;
function mostrar(i) {
    idx = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => s.classList.toggle('activa', k === idx));
    renderMathInElement(slides[idx], {delimiters: [...]});  // re-renderiza $...$ de ESA slide
}
mostrar(parseInt(new URLSearchParams(location.search).get('slide') || '0', 10));  // ?slide=N para testing
window.addEventListener('keydown', (e) => {
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { /* avanzar, ver hook abajo */ }
    if (['ArrowLeft', 'PageUp'].includes(e.key)) { /* retroceder */ }
});
```

`.slide { display:none }` / `.slide.activa { display:flex }` — todas las slides existen en el DOM
todo el tiempo (nada se crea/destruye al navegar), solo se togglea visibilidad. Esto importa para
los widgets: su estado (ej. el angulo de una recta, cuantos terminos de una formula ya se revelaron)
**persiste** cuando el usuario navega para adelante/atras y vuelve — es el comportamiento esperado
(como los "fragments" de reveal.js), no hace falta resetear nada al volver a una slide.

### El hook de teclado para widgets que "pausan" el avance de slide

Cuando una slide tiene un widget que se revela paso a paso (la formula) y el usuario pidio
explicitamente que se controle con las MISMAS flechas de navegacion (no un boton aparte, para que
sea consistente con el resto del deck), el widget se registra en un array global:

```js
// dentro del widget:
(window.__fpAvanzar = window.__fpAvanzar || []).push(function(slideActivo) {
    if (slideActivo !== estaSlide || yaTermine) return false;  // no me toca: dejar pasar
    revelarSiguienteTermino();
    return true;  // consumido: NO cambiar de slide
});
```

Y el manejador global de teclado consulta ese array **antes** de llamar a `mostrar(idx+1)`:

```js
if (['ArrowRight', ...].includes(e.key)) {
    const consumido = (window.__fpAvanzar || []).some(fn => fn(slides[idx]));
    if (!consumido) mostrar(idx + 1);
}
```

Asi, mientras al widget le queden terminos por revelar, la flecha derecha revela el siguiente
termino; una vez que ya revelo todos, la siguiente flecha derecha cae al comportamiento normal y
avanza de diapositiva. Simetrico para la flecha izquierda (retroceder un termino / retroceder de
slide). Este patron es generico: cualquier widget futuro que quiera "capturar" la flecha antes de
que cambie de slide se registra igual, sin tocar el manejador global.

## Tamano del deck y por que `vw` solo no alcanza

```css
#deck { width:min(96vw, calc(96vh * 16 / 9)); max-width:1600px; aspect-ratio:16/9; }
.slide { font-size:min(1.55vw, calc(1.55vh * 16 / 9), 24.8px); }
```

Si el deck se dimensiona solo con `96vw` (96% del ancho de la ventana) y la ventana es mas "corta"
que ancha en proporcion (comun: un navegador normal con barra de direcciones/pestañas/marcadores le
resta alto a la ventana pero no ancho), el deck calculado por ancho puede terminar mas alto que el
espacio vertical disponible — se corta arriba y/o abajo. La formula `min(96vw, 96vh*16/9)` toma el
menor de "96% del ancho" y "lo que le corresponderia en ancho a 96% del alto, en proporcion 16:9",
garantizando que el deck entre siempre sin importar la forma de la ventana.

**El `font-size` tiene que escalar con la MISMA formula** (proporcionalmente: `1.55/96` es la misma
razon que `deck-width / viewport-width` cuando el ancho manda). Si el deck se dimensiona por alto (
ventana corta) pero el `font-size` sigue atado solo a `vw`, el texto queda desproporcionadamente
grande para el deck resultante, y todo el layout interno (que asume ciertas proporciones de texto vs
contenedor) se rompe — hubo un bug real donde los botones de un widget "desaparecian" porque el texto
se volvia tan grande que el layout colapsaba de formas inesperadas.

## `datos.py`: precomputo unico, fuente de verdad {#datos}

Cuando la clase usa un dataset real (no solo conceptos), **nunca se inventan numeros** en el texto
ni en los widgets. El patron:

1. `datos.py` se corre **una sola vez** (no en cada generacion del deck) con el interprete de Python
   que tenga pandas/sklearn/lo que haga falta (puede ser distinto del que corre el resto del deck,
   que no necesita esas librerias pesadas).
2. Calcula TODO lo que el deck va a necesitar (promedios, resultados de un modelo, coordenadas de
   puntos para los widgets, curvas precomputadas para sliders) y lo vuelca a un **JSON unico**.
3. `interactivos.py` y `contenido_bloqueN.py` leen de ese JSON — nunca recalculan ni tocan el dataset
   crudo directamente. Si dos widgets distintos necesitan estar basados en "los mismos estudiantes"
   (p.ej. un biplot y un comparador de metodos), usar el MISMO subsample/indices en `datos.py` para
   que sea literalmente la misma gente en ambos widgets — es un detalle que el usuario nota y valora.
4. Si el calculo es pesado (t-SNE, UMAP, un modelo que tarda), subsamplear para no pagar ese costo
   en cada widget, pero mantener la metodologia identica a cualquier notebook/analisis previo del
   curso (mismas variables, mismo escalado, mismo seed) para que los numeros sean consistentes con
   lo que el estudiante ya vio.

Ejemplo de forma del JSON (una seccion por widget/necesidad, no un blob plano):
```json
{
  "dos_d": {"puntos": [[x,y],...], "target": ["A","B",...], "pc1": [vx,vy], "pve": [95.2, 4.8]},
  "rotacion": {"angulos": [...], "varianza": [...], "error": [...]},
  "biplot": {"scores": [[x,y],...], "loadings_pc1": [...], "loadings_pc2": [...], "etiquetas": [...]}
}
```

## Helpers de contenido (`comun.py`)

| Helper | Que arma |
|---|---|
| `slide(numero, bloque, titulo, contenido_html, contenido_clase=...)` | el esqueleto de una slide completa |
| `portada_bloque(numero, bloque, nombre, bajada)` | la divisoria entre bloques tematicos |
| `caja(titulo, cuerpo, color, ancho=...)` | un recuadro destacado con borde de color |
| `bullets(items)` / `numerada(items)` | listas con vineta / numeradas |
| `nota(texto)` | texto chico gris al pie de una slide (aclaraciones, no el mensaje principal) |
| `alert(texto, bloque)` | resalta una palabra/frase en el color del bloque actual |
| `ecuacion(formula)` | una formula estatica centrada (usa `$$...$$`, sin interaccion) |
| `tabla(encabezados, filas)` | una tabla simple |
| `figura(src_b64, alt, pie_texto)` | una imagen con su nota al pie |
| `colab_linea(...)` / `slide_notebook(...)` | puntero a una notebook de practica (patron de curso) |

`contenido_clase` en `slide()` acepta clases utilitarias ya definidas en el CSS: `"centrado"` (todo
centrado vertical y horizontalmente, para slides con un widget o poco texto), `"centrado-img"` (para
una figura grande), `"densa"` (achica fuente/espaciado cuando una slide tiene mucho contenido —
formula + varios bullets + una caja — para que no se corte contra el pie de pagina).

## Apertura y cierre: no son slides como las demas

La portada (slide 1 de todo el deck) casi siempre necesita un tratamiento visual propio — logo
institucional grande a todo color, una caja de titulo solida en el color primario, autor/fecha — que
no encaja en el esqueleto generico de `slide()` (header con logo chico + main + footer con
progreso). Por eso la portada **se arma a mano** como un fragmento HTML suelto, no llamando a
`slide()`. Ver `assets/ejemplo_apertura_cierre.py` para el patron completo; en resumen:

```python
SLIDES.append(f"""
<section class="slide" data-numero="1">
  <main class="contenido portada">
    <img class="logo-grande" src="{LOGO_COLOR_B64}" alt="logo">
    <div class="caja-titulo-portada">
      <p class="tp-clase">...</p>
      <p class="tp-nombre">...</p>
      <p class="tp-subtitulo">...</p>
    </div>
    <p class="autor">...</p>
    <p class="fecha">...</p>
  </main>
</section>""")
```

Notar: **dos variantes de logo distintas** (`LOGO_B64` chico para el resto de las slides,
`LOGO_COLOR_B64` grande para esta) — configurar las dos si el deck lleva marca institucional; es
facil setear una y olvidar la otra, y el resultado (logo en la portada pero ausente en el resto del
deck, o viceversa) pasa desapercibido hasta que alguien lo nota en el deck ya armado.

El resto de la apertura (pregunta guia, roadmap) y el cierre **si** usan `slide()` normalmente, pero
con `bloque=None` — eso hace que `_color_bloque(None)` devuelva NAVY (el color institucional) en vez
del color de un bloque tematico especifico, correcto porque esas slides no pertenecen a ningun
bloque. Es tambien comun que la ULTIMA slide de todo el deck pase `con_logo=False` (bookend simetrico
con la portada, que tampoco lleva el logo chico) — es una preferencia de diseño, no una regla; ajustar
segun lo que pida el usuario.
